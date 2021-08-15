import time
from mpu6050 import MPU6050
import math


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


mpu = MPU6050(0x69)

mpu.axoffset = 442
mpu.ayoffset = 1573
mpu.azoffset = 1225
mpu.gxoffset = -11
mpu.gyoffset = -39
mpu.gzoffset = 19

while True:
    a = mpu.acceleration
    g = mpu.gyro

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f g" % (a[0], a[1], a[2]))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (g[0], g[1], g[2]))
    print("Temperature: %.2f C" % mpu.temperature)
    print("x rotation: ", get_x_rotation(a[0], a[1], a[2]))
    print("y rotation: ", get_y_rotation(a[0], a[1], a[2]))
    print("")
    time.sleep(1)
