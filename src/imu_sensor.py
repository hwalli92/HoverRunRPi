import time
import threading
import math
from mpu6050 import MPU6050

CFCONST = 0.98


class IMUSensor(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        self.mpu = MPU6050(0x69)
        self.serial = serial_port

        self.roll = 0
        self.gyro_roll = 0
        self.comp_roll = 0

    def run(self):

        a = self.mpu.acceleration
        g = self.mpu.gyro

        self.roll = self.get_x_rotation(a)
        self.gyro_roll = self.roll
        self.comp_roll = self.roll

        timer = time.time()

        while not self.shutdown_flag.isSet():
            a = self.mpu.acceleration
            g = self.mpu.gyro

            dt = time.time() - timer
            timer = time.time()

            self.gyro_roll = g[0]
            self.roll = self.get_x_rotation(a)
            self.comp_roll = CFCONST * (self.gyro_roll * dt) + (1 - CFCONST) * self.roll
            # self.comp_roll = 0.93 * (self.comp_roll + self.gyro_roll * dt) + 0.07 * self.roll

            print("mpu {} {} {}".format(self.gyrox, self.pitch, self.cfanglex))

            self.send_mpudata()

            time.sleep(1)

    def send_mpudata(self):
        msg = "mpu {} {} {}".format(self.gyro_roll, self.roll, self.comp_roll)
        self.serial.write(msg)

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, acceleration):
        radians = math.atan2(
            acceleration[0], self.dist(acceleration[1], acceleration[2]),
        )
        return -math.degrees(radians)

    def get_x_rotation(self, acceleration):
        radians = math.atan2(
            acceleration[1], self.dist(acceleration[0], acceleration[2]),
        )
        return math.degrees(radians)
