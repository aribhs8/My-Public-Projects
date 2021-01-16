/*
 * TempTest.c
 *
 * Created: 2020-11-18 3:40:54 PM
 *  Author: aribh
 
#define F_CPU 40000000UL
#include <avr/io.h>
#include <avr/interrupt.h>

int main()
{
	// configure ADC
	setupADC();
	
	sei();						// Enable global interrupt service
	
	// setup LEDs
	DDRD |= 0x1f;				// Set LEDs to be outputs
	PORTD |= 0x00;				// Turn all LEDs off if on 
	
	while (1)
	{
		
	}
}

void setupADC()
{
	ADMUX = (1 << REFS0);
	ADCSRA = (1 << ADEN | 1 << ADIE | 1 << ADPS2 | 1 << ADPS1);
	DIDR0 = 1 << ADC0D;
	ADCSRA |= 1 << ADSC;
}

ISR(ADC_vect)
{
	float reading = ADC;
	float temperatureC = reading * 0.48828125;
	
	PORTD = 1 << PIND0;
	if (temperatureC >= 10)
	{
		PORTD |= 1 << PIND1;
	}
	if (temperatureC >= 15)
	{
		PORTD |= 1 << PIND2;
	}
	if (temperatureC >= 20)
	{
		PORTD |= 1 << PIND3;
	}
	if (temperatureC >= 25)
	{
		PORTD |= 1 << PIND4;
	}
	
	ADCSRA |= 1 << ADSC;
}
*/