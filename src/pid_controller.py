import time
import threading
import math
from mpu6050 import MPU6050
from kalman import KalmanFilter
from simple_pid import PID


class PIDController(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        self.mpu = MPU6050(0x69)
        self.kalmanX = KalmanFilter()
        self.pid = PID(3, 0, 0, setpoint=5)

        self.serial = serial_port

        self.roll = 0
        self.gyro_roll = 0
        self.comp_roll = 0
        self.kalman_roll = 0
        self.pidvalue = 0

    def run(self):

        a = self.mpu.acceleration
        g = self.mpu.gyro

        self.roll = self.get_x_rotation(a[0], a[1], a[2])
        self.kalmanX.set_angle(self.roll)
        self.gyro_roll = self.roll
        self.comp_roll = self.roll

        timer = time.time()

        while not self.shutdown_flag.isSet():
            a = self.mpu.acceleration
            g = self.mpu.gyro

            dt = time.time() - timer
            timer = time.time()

            self.roll = self.get_x_rotation(a[0], a[1], a[2])
            self.kalman_roll = self.kalmanX.get_angle(self.roll, g[0], dt)

            self.gyro_roll = g[0] * dt
            self.comp_roll = 0.93 * (self.comp_roll + g[0] * dt) + 0.07 * self.roll

            print(
                "mpu {} {} {} {}".format(
                    self.roll, self.gyro_roll, self.kalman_roll, self.comp_roll
                )
            )
            self.pidvalue = self.pid(self.comp_roll)

            print("pid {}".format(self.pidvalue))

            # self.send_mpudata()

            time.sleep(2)

    def send_mpudata(self):
        msg = "pid {}".format(self.pidvalue)
        print(msg)
        self.serial.write(msg)

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self):
        radians = math.atan2(
            self.mpu.acceleration[0],
            self.dist(self.mpu.acceleration[1], self.mpu.acceleration[2]),
        )
        return -math.degrees(radians)

    def get_x_rotation(self):
        radians = math.atan2(
            self.mpu.acceleration[1],
            self.dist(self.mpu.acceleration[0], self.mpu.acceleration[2]),
        )
        return math.degrees(radians)
