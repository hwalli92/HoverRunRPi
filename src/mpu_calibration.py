"""
    MPU6050 Calibration script

    Adapted from: https://github.com/WoolseyWorkshop/Article-Interfacing-An-MPU6050-Gyroscope-Accelerometer-Sensor-Module-To-A-Raspberry-Pi/tree/master/mpu6050_calibration
"""


import time
from mpu6050 import MPU6050

accuracy = 0.05
sample_size = 1000
accel_sensitivity = 16384.0
gyro_sensitivity = 131.0


def get_readings(mpudev):

    sumax = 0
    sumay = 0
    sumaz = 0
    sumgx = 0
    sumgy = 0
    sumgz = 0

    for i in range(0, (sample_size + 100)):
        a = mpu.accel_raw
        g = mpu.gyro_raw

        if i > 100:
            sumax += a[0]
            sumay += a[1]
            sumaz += a[2]
            sumgx += g[0]
            sumgy += g[1]
            sumgz += g[2]

        time.sleep(0.005)

    avgax = sumax / 1000
    avgay = sumay / 1000
    avgaz = sumaz / 1000
    avggx = sumgx / 1000
    avggy = sumgy / 1000
    avggz = sumgz / 1000

    print("Average Readings: ", avgax, avgay, avgaz, avggx, avggy, avggz)

    return (avgax, avgay, avgaz, avggx, avggy, avggz)


mpu = MPU6050(0x69)

print(
    "Old Offsets: aX = %5d, aY = %5d, aZ = %5d, gX = %5d, gY = %5d, gZ = %5d\n"
    % (
        mpu.axoffset,
        mpu.ayoffset,
        mpu.azoffset,
        mpu.gxoffset,
        mpu.gyoffset,
        mpu.gzoffset,
    ),
)

print("Zero Out Offsets")
mpu.axoffset = 0
mpu.ayoffset = 0
mpu.azoffset = 0
mpu.gxoffset = 0
mpu.gyoffset = 0
mpu.gzoffset = 0

offsetax = 0
offsetay = 0
offsetaz = 0
offsetgx = 0
offsetgy = 0
offsetgz = 0

print("Starting Calibration Process")

while True:
    mpu.axoffset = offsetax
    mpu.ayoffset = offsetay
    mpu.azoffset = offsetaz
    mpu.gxoffset = offsetgx
    mpu.gyoffset = offsetgy
    mpu.gzoffset = offsetgz

    avgax, avgay, avgaz, avggx, avggy, avggz = get_readings(mpu)

    if (
        abs(avgax) < int(accel_sensitivity * accuracy)
        and abs(avgay) < int(accel_sensitivity * accuracy)
        and abs(int(accel_sensitivity) - avgaz) < int(accel_sensitivity * accuracy)
        and abs(avggx) < int(gyro_sensitivity * accuracy)
        and abs(avggy) < int(gyro_sensitivity * accuracy)
        and abs(avggz) < int(gyro_sensitivity * accuracy)
    ):
        break

    offsetax -= int(float(avgax) / 8)
    offsetay -= int(float(avgay) / 8)
    offsetaz += int((accel_sensitivity - float(avgaz)) / 8)
    offsetgx -= int(float(avggx) / 4)
    offsetgy -= int(float(avggy) / 4)
    offsetgz -= int(float(avggz) / 4)

print(
    "New Offsets: aX = %5d, aY = %5d, aZ = %5d, gX = %5d, gY = %5d, gZ = %5d\n"
    % (
        mpu.axoffset,
        mpu.ayoffset,
        mpu.azoffset,
        mpu.gxoffset,
        mpu.gyoffset,
        mpu.gzoffset,
    ),
)

a = mpu.accel_raw
g = mpu.gyro_raw

ax = a[0] / accel_sensitivity
ay = a[1] / accel_sensitivity
az = a[2] / accel_sensitivity
gx = g[0] / gyro_sensitivity
gy = g[1] / gyro_sensitivity
gz = g[2] / gyro_sensitivity

print(
    "aX = %4.1f g, aY = %4.1f g, aZ = %4.1f g, gX = %6.1f °/s, gY = %6.1f °/s, gZ = %6.1f °/s\n"
    % (ax, ay, az, gx, gy, gz),
)
