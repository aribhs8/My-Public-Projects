/*
 * main.c
 *
 * Created: 2020-11-19 12:45:20 PM
 *  Author: aribh
 
 Todo: Fix problem where program launches in edit mode
 */ 

#define F_CPU 40000000UL
#define LED_PORT PORTD
#define LED_DPORT DDRD

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "led_array.h"

// prototypes
void setupADC();
void setupTimer();
void controlHeater();

int editMode = 0;
int repeatCount = 0;
float temperature;
float desiredTemperature = 22.5;

int main()
{
	setupADC();											// Setup and start ADC service
	
	sei();												// Start global interrupt service
	
	// Setup I/O pins
	initLeds();
	
	DDRB |= 1 << PINB0;									// Set heater to output
	DDRB &= ~(1 << PINB1);								// Set pushbutton to input
	PORTB &= ~(0 << PINB0);								// Turn off heater
	PORTB |= 1 << PINB1;								// Enable pull-up for button
	
	setupTimer();										// Timer code
	
	while (1)
	{
		// check for button press
		if (!(PINB & (1 << PINB1)))
		{
			while (!(PINB & (1 << PINB1)));				// wait for release
			turnOffLeds();
			editMode = !editMode;
			ADMUX = editMode ? 0x41 : 0x40;				// Toggle editMode
		}
		
		//controlHeater();
	}
}

void setupADC()
{
	ADMUX |= (1 << REFS0);
	ADCSRA |= (1 << ADEN | 1 << ADIE | 1 << ADPS2 | 1 << ADPS1);
	DIDR0 |= 1 << ADC0D;
	ADCSRA |= 1 << ADSC;
}

void setupTimer()
{
	TCCR1B = (1 << WGM12);
	OCR1A = 1953;
	TIMSK1 = (1 << OCIE1A);
	TCCR1B |= (1 << CS12 | 1 << CS10);
}

void controlHeater()
{
	if (temperature >= desiredTemperature - (int) desiredTemperature % 5)
	{
		if (TCNT0 > 3096)
		{
			/************************************************************************/
			/* If the recorded temperature is greater than the min value of the		*/
			/* desired temperature for more than 2 minutes, turn off the heater.	*/
			/************************************************************************/
			TCNT1 = 0;
			repeatCount++;
			if (repeatCount > 120)
			{
				PORTB |= 1 << PINB0;
			}
		}
		
	} else
	{
		// Turn the heater on
		PORTB &= ~(1 << PINB0);
		repeatCount = 0;
	}
}

/*
void controlHeater()
{
	if (temperature < desiredTemperature)
	{
		// if temperature reaches desired range
		if (temperature >= desiredTemperature - (int) desiredTemperature % 5)
		{
			// keep the heater on until a timer goes off (2 minutes)
			if (TCNT1 > 468750)
			{
				// might need another variable to repeat the count
				TCNT1 = 0;
				passedThreshold = 1;
				
				// turn the heater off
				PORTB &= ~(0 << PINB0);
			}
		}
		else
		{
			passedThreshold = 0;
		}
		
		if (passedThreshold == 0)
		{
			// turn the heater on
			PORTB |= 0 << PINB0;	
		}
		
	}
	else
	{
		// turn the heater off
		PORTB &= ~(0 << PINB0);	
	}
}
*/

ISR(ADC_vect)
{
	// maybe change types to uint8_t and uint16_t
	int low = ADCL;
	int reading = ADCH << 8 | low;
	
	switch (ADMUX)
	{
		case 0x40:
			// temperature sensor
			temperature = reading * 0.48828125;
			incrementalLeds(temperature, 5, 5);
			break;
		case 0x41:
			// potentiometer
			//desiredTemperature = reading/32.0;
			desiredTemperature = reading/34.0;
			break;
		default:
			break;
	}
	
	
	ADCSRA |= 1 << ADSC;
}

ISR(TIMER1_COMPA_vect)
{
	if (editMode)
	{
		if (ledStatus() == 0)
		{
			//incrementalLeds(desiredTemperature, 32/5.0, 32.0/5.0);
			incrementalLeds(desiredTemperature, 5, 5);
		}
		else
		{
			turnOffLeds();
		}
	}
	
	if (temperature >= desiredTemperature - (int) desiredTemperature % 5)
	{
		
		if (temperature - (desiredTemperature - (int) desiredTemperature % 5) > 5)
		{
			// Turn heater off immediately
			PORTB |= 1 << PINB0;
		} else
		{
			/************************************************************************/
			/* If the recorded temperature is greater than the min value of the		*/
			/* desired temperature for more than 2 minutes, turn off the heater.	*/
			/************************************************************************/
			repeatCount++;
			if (repeatCount >= 240)
			{
				PORTB |= 1 << PINB0;
			}
		}
	} else
	{
		// Turn the heater on
		PORTB &= ~(1 << PINB0);
		repeatCount = 0;
	}
}