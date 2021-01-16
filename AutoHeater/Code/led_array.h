/*
 * IncFile1.h
 *
 * Created: 2020-11-19 2:49:04 PM
 *  Author: aribh
 */ 


#ifndef INCFILE1_H_
#define INCFILE1_H_

#ifndef LED_PORT
/* prevent compiler error by supplying a default */
# warning "LED_PORT not defined for \"led_array.h\""
#include <avr/io.h>
#define LED_PORT PORTD
#endif

#ifndef LED_DPORT
# warning "LED_DPORT not defined for \"led_array.h\""
#include <avr/io.h>
#define LED_DPORT DDRD
#endif


// Prototypes
void initLeds(void);
void turnOffLeds(void);
int ledStatus(void);
void toggleLeds(void);
void turnOnALed(int pin);
void incrementalLeds(float value, int start, float increment);

#endif /* INCFILE1_H_ */