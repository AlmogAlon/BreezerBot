import RPi.GPIO as GPIO
from time import sleep

left_forward = 21
left_backwards = 26
right_forward = 20
right_backwards = 16

class Motor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(left_forward,GPIO.OUT)
        GPIO.setup(left_backwards,GPIO.OUT)
        GPIO.setup(right_forward,GPIO.OUT)
        GPIO.setup(right_backwards,GPIO.OUT)
    
    def moveForward(self):
        GPIO.output(left_backwards,GPIO.LOW)
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.HIGH)
        GPIO.output(right_forward,GPIO.HIGH)

    def moveBackwards(self):
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.HIGH)
        GPIO.output(right_backwards,GPIO.HIGH)
    
    def turnLeft(self):
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.HIGH)
        GPIO.output(left_backwards,GPIO.HIGH)
        sleep(0.1)
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)

    def turnRight(self):
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.HIGH)
        GPIO.output(right_backwards,GPIO.HIGH)
        sleep(0.1)
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)

    def stop(self):
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)

