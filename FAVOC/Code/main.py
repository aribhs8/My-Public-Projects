#!usr/bin/Python3

"""
Main program for FAVOC

Est 2019; Author: Arib Hussain
"""
# create FAVOC object

# import used modules
from __future__ import print_function
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils


class FAVOC:
    def __init__(self):
        # set GPIO mode to BCM and disable warnings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # DEFINE PINS
        # input
        self.power_buttonPin = 26
        self.osc_buttonPin = 12
        # output
        self.servoPin = 18
        self.fanPin = 5

        # setup GPIO pins
        GPIO.setup(self.power_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.osc_buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.servoPin, GPIO.OUT)
        GPIO.setup(self.fanPin, GPIO.OUT)

        # setup buttons
        GPIO.add_event_detect(self.power_buttonPin, GPIO.FALLING)
        GPIO.add_event_detect(self.osc_buttonPin, GPIO.FALLING)

        # setup servo motor
        self.pwm = GPIO.PWM(self.servoPin, 80.0)
        self.pwm.start(0)
        
        # setup camera
        self.setup_camera()
        

        # mode variables
        self.running = False
        self.oscillating = False
        
    def setup_camera(self):
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(320, 240))
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr",
                use_video_port=True)

    # CALLBACK METHODS
    def power(self):
        self.running = not self.running

    def rotate(self):
        print("pressed")
        if self.oscillating:
            if cv2.waitKey(1):
                cv2.destroyAllWindows()
        self.oscillating = not self.oscillating

    # MAIN LOOP
    def loop(self):
        # set motor angle to 0
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        # clean-up
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
        self.vs = PiVideoStream().start()
        try:
            while (True):
                # FAN CONTROL
                # turn fan on/off
                GPIO.output(self.fanPin, self.running)
                # check for fan button press
                if GPIO.event_detected(self.power_buttonPin):
                    self.power()

                 # OSCILLATION
                if GPIO.event_detected(self.osc_buttonPin):
                    self.rotate()

                # Check for oscillation
                if self.running:
                    if self.oscillating:
                        faces_detected, middle = self.record(cap=cap, cascade=face_cascade)
                        if len(faces_detected) > 0:
                            # get x-coordinate of face detected
                            for x,y,w,h in faces_detected:
                                x_coord = x+w
                                middle_min = middle - w
                                middle_max = middle + w
                            print('Middle Min: ' + str(middle_min))
                            print('Middle Max: ' + str(middle_max))
                            print('x-coord: ' + str(x_coord))
                            if x_coord > middle_max:
                                print('left')
                                print(middle)
                                print((round(abs((x_coord-middle)/372), 1)))
                                self.pwm.ChangeDutyCycle((round(abs((x_coord-middle)/50), 1)))
                            elif x_coord < middle_min :
                                self.pwm.ChangeDutyCycle((round(abs((x_coord+middle)/50), 1)))
        finally:
            GPIO.cleanup()
            self.pwm.stop()

    def record(self, cap, cascade):
        # create new openCV window
        frame = self.vs.read()
        frame = imutils.resize(frame, width=400)
        
        # convert live camera-video to gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # look for faces in the video
        faces = cascade.detectMultiScale(gray, 1.1, 5)
        self.num_faces = len(faces)
        
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,220), 3)
            
        # calculate center of frame (horizontal)
        height, width, chan = np.shape(frame)
        xMid = width/2 * 1.0
        
        # show openCV frames
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xff==ord('q'):
            return
            
        return faces, xMid
        

def main():
    favoc = FAVOC()
    favoc.loop()
    favoc.pwm.stop()
    GPIO.cleanup()

if __name__ == "__main__": main()
