import RPi.GPIO as GPIO
from time import sleep

left_forward = 21
left_backwards = 26
right_forward = 20
right_backwards = 16

class Motor:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(left_forward,GPIO.OUT)
        GPIO.setup(left_backwards,GPIO.OUT)
        GPIO.setup(right_forward,GPIO.OUT)
        GPIO.setup(right_backwards,GPIO.OUT)
        self.right_forward_pwm=GPIO.PWM(right_forward,100)
        self.right_backwards_pwm=GPIO.PWM(right_backwards,100)
        self.left_forward_pwm=GPIO.PWM(left_forward,100)
        self.left_backwards_pwm=GPIO.PWM(left_backwards,100)
        self.right_forward_pwm.start(0)
        self.right_backwards_pwm.start(0)
        self.left_forward_pwm.start(0)
        self.left_backwards_pwm.start(0)
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
    
    def turnLeft(self,t=0.1):
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.HIGH)
        GPIO.output(left_backwards,GPIO.HIGH)
        sleep(t)
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)

    def turnLeftPWM(self, p=100, t=0.1):
        self.right_forward_pwm.ChangeDutyCycle(p)
        self.left_backwards_pwm.ChangeDutyCycle(p)
        sleep(t)
        self.right_forward_pwm.ChangeDutyCycle(0)
        self.left_backwards_pwm.ChangeDutyCycle(0)
        
    def turnRight(self,t=0.1):
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.HIGH)
        GPIO.output(right_backwards,GPIO.HIGH)
        sleep(t)
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)

    def turnRightPWM(self, p=100, t=0.1):
        self.left_forward_pwm.ChangeDutyCycle(p)
        self.right_backwards_pwm.ChangeDutyCycle(p)
        sleep(t)
        self.left_forward_pwm.ChangeDutyCycle(0)
        self.right_backwards_pwm.ChangeDutyCycle(0)

    def stop(self):
        GPIO.output(right_backwards,GPIO.LOW)
        GPIO.output(left_forward,GPIO.LOW)
        GPIO.output(right_forward,GPIO.LOW)
        GPIO.output(left_backwards,GPIO.LOW)

