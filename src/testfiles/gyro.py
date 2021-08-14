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

# while True:
data = mpu.get_data()
print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f g" % (data[0:3]))
print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (data[3:6]))
# print("Temperature: %.2f C" % mpu.temperature)
# print(
#     "x rotation: ",
#     get_x_rotation(mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]),
# )
# print(
#     "y rotation: ",
#     get_y_rotation(mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]),
# )
# print("")
# time.sleep(1)
