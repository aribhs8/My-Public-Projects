/*
  HMC5883L Triple Axis Digital Compass. Compass Example.
  Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-magnetometr-hmc5883l.html
  GIT: https://github.com/jarzebski/Arduino-HMC5883L
  Web: http://www.jarzebski.pl
  (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
#include "FastLED.h"
#include <HMC5883L.h>

// make definitions
#define NUM_LEDS 4                      // # of LEDS on led strip 
#define LED_TYPE WS2812B
#define DATA_PIN_LED 3                  // Pin 3 connected to LED strip

CRGB leds[NUM_LEDS];                    // initialize an LED array

HMC5883L compass;
int fixedHeadingDegrees;                // used to store heading value

void setup()
{
  Serial.begin(9600);
  FastLED.addLeds<LED_TYPE, DATA_PIN_LED, GRB>(leds, NUM_LEDS);

  // Initialize Initialize HMC5883L
  Serial.println("Initialize HMC5883L");
  while (!compass.begin())
  {
    Serial.println("Could not find a valid HMC5883L sensor, check wiring!");
    delay(500);
  }

  // Set measurement range
  compass.setRange(HMC5883L_RANGE_1_3GA);

  // Set measurement mode
  compass.setMeasurementMode(HMC5883L_CONTINOUS);

  // Set data rate
  compass.setDataRate(HMC5883L_DATARATE_30HZ);

  // Set number of samples averaged
  compass.setSamples(HMC5883L_SAMPLES_8);

  // Set calibration offset. See HMC5883L_calibration.ino
  compass.setOffset(0, 0);
}

void loop()
{
  Vector norm = compass.readNormalize();

  // Calculate heading
  float heading = atan2(norm.YAxis, norm.XAxis);

  // Set declination angle on your location and fix heading
  // You can find your declination on: http://magnetic-declination.com/
  // (+) Positive or (-) for negative
  // For Mississauga, ON / Canada declination angle is -10'15W (negative)
  // Formula: (deg + (min / 60.0)) / (180 / M_PI);
  float declinationAngle = (10.0 - (15.0 / 60.0)) / (180 / M_PI);
  heading -= declinationAngle;

  // Correct for heading < 0deg and heading > 360deg
  if (heading < 0)
  {
    heading += 2 * PI;
  }

  if (heading > 2 * PI)
  {
    heading -= 2 * PI;
  }

  // Convert to degrees
  float headingDegrees = heading * 180/M_PI; 

  // fix rotation speed of HC5883L module
  if (headingDegrees >= 1 && headingDegrees < 240) {
    fixedHeadingDegrees = map(headingDegrees*100, 0, 239*100, 0, 179*100) / 100.00;
  }
  else {
    if (headingDegrees > 240) {
      fixedHeadingDegrees = map(headingDegrees*100, 240*100, 360*100, 180*100, 360*100) / 100.00;
    }
  }

  int headValue = fixedHeadingDegrees / 71;
  int ledtoHeading = map(headValue, 0, 3, 3, 0);

  // clear the LED strip
  FastLED.clear();

  leds[ledtoHeading] = CRGB::Red;
  Serial.print(leds[ledtoHeading]);

  FastLED.setBrightness(50);
  FastLED.show();

  // Output
  Serial.print(" Heading = ");
  Serial.print(heading);
  Serial.print(" Degress = ");
  Serial.print(headingDegrees);
  Serial.println();

  delay(100);
}
