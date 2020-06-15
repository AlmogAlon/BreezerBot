__author__ = 'Geir Istad'
"""
MPU6050 Python I2C Class - MPU6050 example usage
Copyright (c) 2015 Geir Istad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from MPU6050 import MPU6050
import time,math

class Gyroscope:
    def __init__(self):
        i2c_bus = 1
        device_address = 0x68
        # The offsets are different for each device and should be changed
        # accordingly using a calibration procedure
        x_accel_offset = -5489
        y_accel_offset = -1441
        z_accel_offset = 1305
        x_gyro_offset = -2
        y_gyro_offset = -72
        z_gyro_offset = -5
        enable_debug_output = False

        self.mpu = MPU6050(i2c_bus, device_address, x_accel_offset, y_accel_offset,
              z_accel_offset, x_gyro_offset, y_gyro_offset, z_gyro_offset,
              enable_debug_output)

        self.mpu.dmp_initialize()
        self.mpu.set_DMP_enabled(True)

        self.packet_size = self.mpu.DMP_get_FIFO_packet_size()
        self.FIFO_count = self.mpu.get_FIFO_count()
        self.FIFO_buffer = [0]*64
        self.FIFO_count_list = list()

    def getSingleYaw(self):
        while True:
        #FIFO_count = mpu.get_FIFO_count()
            mpu_int_status = self.mpu.get_int_status()
            # If overflow is detected by status or fifo count we want to reset
            if (self.FIFO_count == 1024) or (mpu_int_status & 0x10):
                self.mpu.reset_FIFO()
            # Check if fifo data is ready
            elif (mpu_int_status & 0x02):
                # Wait until packet_size number of bytes are ready for reading, default
                # is 42 bytes
                #while FIFO_count < packet_size:
                #    FIFO_count = mpu.get_FIFO_count()
                self.FIFO_buffer = self.mpu.get_FIFO_bytes(self.packet_size)
                #accel = mpu.DMP_get_acceleration_int16(FIFO_buffer)
                quat = self.mpu.DMP_get_quaternion_int16(self.FIFO_buffer)
                grav = self.mpu.DMP_get_gravity(quat)
                if grav.x==0 or grav.y==0 or grav.z==0:
                    continue
                roll_pitch_yaw = self.mpu.DMP_get_euler_roll_pitch_yaw(quat, grav)
                return roll_pitch_yaw.z
    def getAverageYaw(self, t=0.1):
        startTime = time.time()
        y=[]
        while True:
            y.append(self.getSingleYaw())
            if time.time() - startTime >= t:
                break
        y.sort()
        x=max(1,len(y)/4)
        print(len(y))
        return sum(y[x:-x])/len(y[x:-x])
