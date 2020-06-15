from simple_pid import PID
import gyroscope
import motor

class Wheel:
    def __init__(self):
        self.motor = motor.Motor()
        self.gyro = gyroscope.Gyroscope()

    def turn(self, degrees):
        startAngle = self.gyro.getAverageYaw()
        p = PID(3,3,5,setpoint=degrees+startAngle)
        v = startAngle
        lastAngle = startAngle
        curAngle = startAngle
        while abs(curAngle - (degrees + startAngle)) > 1:
            control = pid(curAngle)
            d = (math.floor(control - curAngle + 360) % 360) - 180
            if d>0:
                self.motor.turnRightPWM(min(d,100))
            else:
                self.motor.turnLeftPWM(min(-d,100))
            curAngle = self.gyro.getAverageYaw()
