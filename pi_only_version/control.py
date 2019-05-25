#!/usr/bin/env python3
from gpiozero import PWMOutputDevice
from time import sleep
import ultrasonic
import time


#PIN CONFIGURATION
leftFORWARD = PWMOutputDevice(26)   #GPIO PIN 26 is connected to IN1
leftREVERSE = PWMOutputDevice(19)   #GPIO PIN 19 is connected to IN2
rightFORWARD = PWMOutputDevice(13)  #GPIO PIN 13 is connected to IN3
rightREVERSE = PWMOutputDevice(6)   #GPIO PIN 6 is connected to IN4
leftPWM = PWMOutputDevice(21, True, 0, 1000) #GPIO PIN 21 is connected to ENA on H Bridge for left motor
rightPWM = PWMOutputDevice(5, True, 0, 1000)  #GPIO PIN 5 is connected to ENB on H Bridge for right motor

def applyBRAKE():
	leftFORWARD.value = False
	leftREVERSE.value = False
	rightFORWARD.value = False
	rightREVERSE.value = False
	leftPWM.value = 0
	rightPWM.value = 0

def driveFORWARD():
	leftFORWARD.value = True
	leftREVERSE.value = False
	rightFORWARD.value = True
	rightREVERSE.value = False
	leftPWM.value = 1.0
	rightPWM.value = 1.0

def driveREVERSE():
	leftFORWARD.value = False
	leftREVERSE.value = True
	rightFORWARD.value = False
	rightREVERSE.value = True
	leftPWM.value = 1.0
	rightPWM.value = 1.0

def forwardLEFT():
	leftFORWARD.value = True
	leftREVERSE.value = False
	rightFORWARD.value = True
	rightREVERSE.value = False
	leftPWM.value = 0.2
	rightPWM.value = 0.8

def forwardRIGHT():
	leftFORWARD.value = True
	leftREVERSE.value = False
	rightFORWARD.value = True
	rightREVERSE.value = False
	leftPWM.value = 0.8
	rightPWM.value = 0.2

def reverseLEFT():
	leftFORWARD.value = False
	leftREVERSE.value = True
	rightFORWARD.value = False
	rightREVERSE.value = True
	leftPWM.value = 0.2
	rightPWM.value = 0.8

def reverseRIGHT():
	leftFORWARD.value = False
	leftREVERSE.value = True
	rightFORWARD.value = False
	rightREVERSE.value = True
	leftPWM.value = 0.8
	rightPWM.value = 0.2

def main():
	while True:
		dist = ultrasonic.distance()
		print ("Measured Distance = %.1f cm" % dist)
		#time.sleep(1)
		driveFORWARD()
		if (dist<50):
			applyBRAKE()
			

	#	applyBRAKE()
	#	driveFORWARD()
	#	driveREVERSE()
	#	forwardLEFT()
	#	forwardRIGHT()
	#	reverseLEFT()
	#	reverseRIGHT()
	#	applyBRAKE()
	#	sleep(4)




if __name__ == "__main__":
    main()

