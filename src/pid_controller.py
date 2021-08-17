import time
import threading
import math
from mpu6050 import MPU6050
from kalman import KalmanFilter
from pid import PID


class PIDController(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        self.mpu = MPU6050(0x69)
        self.kalmanX = KalmanFilter()
        self.pid = PID(8, 0, 0, setpoint=2)

        self.serial = serial_port

        self.roll = 0
        self.gyro_roll = 0
        self.comp_roll = 0
        self.kalman_roll = 0
        self.pidvalue = 0

    def run(self):

        a = self.mpu.acceleration
        g = self.mpu.gyro

        self.roll = self.get_x_rotation(a)
        self.kalmanX.set_angle(self.roll)
        self.gyro_roll = self.roll
        self.comp_roll = self.roll

        timer = time.time()

        while not self.shutdown_flag.isSet():
            a = self.mpu.acceleration
            g = self.mpu.gyro

            dt = time.time() - timer
            timer = time.time()

            self.roll = self.get_x_rotation(a)
            self.kalman_roll = self.kalmanX.get_angle(self.roll, g[0], dt)

            self.gyro_roll = g[0] * dt
            self.comp_roll = 0.93 * (self.comp_roll + g[0] * dt) + 0.07 * self.roll

            print(
                "mpu %.2f, %.2f, %.2f, %.2f"
                % (self.roll, self.gyro_roll, self.kalman_roll, self.comp_roll)
            )
            self.pidvalue = self.pid.pid_compute(self.kalman_roll)

            print("pid %.2f" % (self.pidvalue))

            self.send_pid()

            time.sleep(1)

        self.pidvalue = 0
        self.send_pid()

    def send_pid(self):
        msg = "pid %.2f" % (self.pidvalue)
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
