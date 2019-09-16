import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servoPin = 18
GPIO.setup(servoPin, GPIO.OUT)

pwm = GPIO.PWM(servoPin, 80)
pwm.start(7)

while (1):
	for i in range(0, 120):
		DC = 1./12. * (i) + 2
		pwm.ChangeDutyCycle(DC)
		time.sleep(0.05)
	for i in range(120, 0, -1):
		DC = 1/12. * i + 2
		pwm.ChangeDutyCycle(DC)
		time.sleep(0.05)

pwm.stop()
GPIO.cleanup()
