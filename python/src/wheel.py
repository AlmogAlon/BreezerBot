from simple_pid import PID
import gyroscope
import motor
import math

class Wheel:
    def __init__(self):
        self.motor = motor.Motor()
        self.gyro = gyroscope.Gyroscope()

    def turn(self, degrees):
        startAngle = self.gyro.getMedianYaw(0.3)
        print('startAngle ' + str(startAngle))
        endPoint = ((degrees+startAngle+180+360)%360)-180
        print('endPoint ' + str(endPoint));
        p = PID(1,0,0,setpoint=endPoint)
        curAngle = startAngle
        while abs(curAngle - endPoint) > 1:
            control = p(curAngle)
            print('control ' + str(control))
            d = ((control + 360 + 180) % 360) - 180
            print('d ' + str(d))
            if d>0:
                self.motor.turnRightPWM(max(20,min(math.floor(d*4),100)),0.1)
            else:
                self.motor.turnLeftPWM(max(20,min(math.floor(-d*4),100)),0.1)
            curAngle = self.gyro.getMedianYaw(0.3)
            print('curAngle ' + str(curAngle))
