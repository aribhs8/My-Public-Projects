/*
 * led_array.c
 *
 * Created: 2020-11-19 2:50:48 PM
 *  Author: aribh
 */ 

// Todo: Make LEDs flash relatively quickly in edit mode
// Todo: If temp. is not set at desired temp. Make the LED that correspond to desired temp flash slowly

#include "led_array.h"

void initLeds()
{
	LED_DPORT = 0xff;		// Set all LEDs on PORT to output
	LED_PORT = 0x00;		// Turn off all LEDs on PORT
}

void turnOffLeds()
{
	LED_PORT = 0x00;
}

int ledStatus()
{
	if (LED_PORT != 0x00)
	{
		return 1;
	} 
	else {
		return 0; 
	}
}

void toggleLeds()
{
	LED_PORT ^= LED_PORT;
}

void turnOnALed(int pin)
{
	LED_PORT |= 1 << pin;
}

void incrementalLeds(float value, int start, float increment)
{
	if (value >= start)
	{
		LED_PORT = 0x1;
	}
	if (value >= start + increment)
	{
		LED_PORT = 0x3;
	}
	if (value >= start + increment*2)
	{
		LED_PORT = 0x7;
	}
	if (value >= start + increment*3)
	{
		LED_PORT = 0xf;
	}
	if (value >= (start + increment*4) - 1)
	{
		LED_PORT = 0x1f;
	}
}