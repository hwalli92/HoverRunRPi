import time
import board
import adafruit_mpu6050
import math


i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c, address=0x69)

offsetax = 0
offsetay = 0
offsetaz = 0
offsetgx = 0
offsetgy = 0
offsetgz = 0

accuracy = 0.05


def get_readings():
    sumax = 0
    sumay = 0
    sumaz = 0
    sumgx = 0
    sumgy = 0
    sumgz = 0

    for i in range(0, 1100):
        accel = mpu.acceleration
        gyro = mpu.gyro

        if i > 100:
            sumax += (accel[0] - offsetax)
            sumay += (accel[1] - offsetay)
            sumaz += (accel[2] - offsetaz)
            sumgx += (gyro[0] - offsetgx)
            sumgy += (gyro[1] - offsetgy)
            sumgz += (gyro[2] - offsetgz)

        time.sleep(0.005)

    avgax = sumax / 1000
    avgay = sumax / 1000
    avgaz = sumax / 1000
    avggx = sumax / 1000
    avggy = sumax / 1000
    avggz = sumax / 1000
    
    print("Average Readings: ", avgax, avgay, avgaz, avggx, avggy, avggz)
    
    return (avgax, avgay, avgaz, avggx, avggy, avggz)


while True:

    avgax, avgay, avgaz, avggx, avggy, avggz = get_readings()

    if (
        abs(avgax) < accuracy
        and abs(avgay) < accuracy
        and abs(avgaz) < accuracy
        and abs(avggx) < accuracy
        and abs(avggy) < accuracy
        and abs(avggz) < accuracy
    ):
        break

    offsetax += (avgax / 8)
    offsetay += (avgay / 8)
    offsetaz += (avgaz / 8)
    offsetgx += (avggx / 4)
    offsetgy += (avggy / 4)
    offsetgz += (avggz / 4)


print("Offsets: ", offsetax, offsetay, offsetaz, offsetgx, offsetgy, offsetgz)

print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration[0]-offsetax, mpu.acceleration[1]-offsetay, mpu.acceleration[2]-offsetaz))
print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro[0]-offsetgx, mpu.gyro[1]-offsetgy, mpu.gyro[2]-offsetgz))
