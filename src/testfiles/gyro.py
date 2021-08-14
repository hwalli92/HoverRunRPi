import time
import board
import adafruit_mpu6050
import math


def dist(a, b):
    return math.sqrt((a * a) + (b * b))


def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)


def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)


i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x69)

# while True:
print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
print("Temperature: %.2f C" % mpu.temperature)
print(
    "x rotation: ",
    get_x_rotation(mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]),
)
print(
    "y rotation: ",
    get_y_rotation(mpu.acceleration[0], mpu.acceleration[1], mpu.acceleration[2]),
)
print("")
# time.sleep(1)
