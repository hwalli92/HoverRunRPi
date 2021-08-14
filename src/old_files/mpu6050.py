import time
import threading
import board
import adafruit_mpu6050
import math
from simple-pid import PID

INTERVAL = 2
CFCONST = 0.98


class MPU6050(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c, address=0x69)
        self.pid = PID(3,0,0, setpoint=1)

        self.serial = serial_port

        self.pitch = 0
        self.gyrox = 0
        self.cfanglex = 0
        self.pidvalue = 0

    def run(self):

        while not self.shutdown_flag.isSet():
            start = time.clock()

            self.gyrox = self.mpu.gyro[0]
            self.pitch = self.get_x_rotation()
            self.cfanglex = (
                CFCONST * (self.gyrox * INTERVAL) + (1 - CFCONST) * self.pitch
            )

            print("mpu {} {} {}".format(self.gyrox, self.pitch, self.cfanglex))
            self.pidvalue = self.pid(self.cfanglex)
            
            print("pid {}".format(self.pidvalue))

            #self.send_mpudata()

            end = time.clock()

            if (end - start) < INTERVAL:
                time.sleep(INTERVAL - (end - start))

    def send_mpudata(self):
        msg = "mpu {} {} {}".format(self.gyrox, self.pitch, self.cfanglex)
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
