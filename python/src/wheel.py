from simple_pid import PID
import gyroscope
import motor
import math

class Wheel:
    def __init__(self):
        self.motor = motor.Motor()
        self.gyro = gyroscope.Gyroscope()

	def unwrap(self, previousAngle, currentAngle):
		if abs(previousAngle - currentAngle) > 180:
			while currentAngle > previousAngle:
				currentAngle -= 360
			while currentAngle < previousAngle:
				currentAngle += 360
		return currentAngle

    def turn(self, degrees):
        startAngle = self.gyro.getMedianYaw(0.3)
        print('startAngle ' + str(startAngle))
        endPoint = self.unwrap(startAngle,degrees+startAngle)
        print('endPoint ' + str(endPoint));
        p = PID(1,0,0,setpoint=endPoint)
        curAngle = startAngle
        while abs((curAngle - endPoint + 36000)%360) > 1:
            control = p(curAngle)
            print('control ' + str(control))
            d = ((control + 360 + 180) % 360) - 180
            print('d ' + str(d))
            if d>0:
                self.motor.turnRightPWM(max(20,min(math.floor(d),100)),0.4)
            else:
                self.motor.turnLeftPWM(max(20,min(math.floor(-d),100)),0.4)
            previousAngle = curAngle
			curAngle = self.gyro.getMedianYaw(0.3)
			curAngle = unwrap(previousAngle, curAngle)			
            print('curAngle ' + str(curAngle))
