import time
import threading
import board
import adafruit_mpu6050
import math


class MPU6050(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.mpu = adafruit_mpu6050.MPU6050(i2c, address=0x69)

        self.serial = serial_port

        self.pitch = 0

    def run(self):

        while not self.shutdown_flag.isSet():

            time.sleep(1)

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self):
        radians = math.atan2(
            self.mpu.acceleration[0],
            dist(self.mpu.acceleration[1], self.mpu.acceleration[2]),
        )
        return -math.degrees(radians)

    def get_x_rotation(self):
        radians = math.atan2(
            self.mpu.acceleration[1],
            dist(self.mpu.acceleration[0], self.mpu.acceleration[2]),
        )
        return math.degrees(radians)
