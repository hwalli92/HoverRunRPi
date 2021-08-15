import time
from mpu6050 import MPU6050
from kalman import KalmanFilter
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
kalmanX = KalmanFilter()
kalmanY = KalmanFilter()

mpu.axoffset = 442
mpu.ayoffset = 1573
mpu.azoffset = 1225
mpu.gxoffset = -11
mpu.gyoffset = -39
mpu.gzoffset = 19

a = mpu.acceleration
g = mpu.gyro

roll = get_x_rotation(a[0], a[1], a[2])
pitch = get_y_rotation(a[0], a[1], a[2])

kalmanX.set_angle(roll)
kalmanY.set_angle(pitch)

gyro_roll = roll
gyro_pitch = pitch

comp_roll = roll
comp_pitch = pitch

timer = time.time()

while True:
    a = mpu.acceleration
    g = mpu.gyro

    dt = time.time() - timer
    timer = time.time()

    roll = get_x_rotation(a[0], a[1], a[2])
    pitch = get_y_rotation(a[0], a[1], a[2])

    kalman_roll = kalmanX.get_angle(roll, g[0], dt)
    kalman_pitch = kalmanY.get_angle(pitch, g[1], dt)

    gyro_roll = g[0] * dt
    gyro_pitch = g[1] * dt

    comp_roll = 0.93 * (comp_roll + g[0] * dt) + 0.07 * roll
    comp_pitch = 0.93 * (comp_pitch + g[1] * dt) + 0.07 * pitch

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f g" % (a[0], a[1], a[2]))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (g[0], g[1], g[2]))
    print("Temperature: %.2f C" % mpu.temperature)

    print("x rotation: %.2f" % (get_x_rotation(a[0], a[1], a[2])))
    print("y rotation: %.2f" % (get_y_rotation(a[0], a[1], a[2])))

    print("Gyro: Roll: %.2f, Pitch: %.2f" % (gyro_roll, gyro_pitch))
    print("Kalman: Roll: %.2f, Pitch: %.2f" % (kalman_roll, kalman_pitch))
    print("Comp: Roll: %.2f, Pitch: %.2f" % (comp_roll, comp_pitch))

    print("")

    time.sleep(1)
