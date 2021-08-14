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
        data = mpudev.get_raw_data()

        if i > 100:
            sumax += data[0]
            sumay += data[1]
            sumaz += data[2]
            sumgx += data[3]
            sumgy += data[4]
            sumgz += data[5]

        time.sleep(0.005)

    avgax = sumax / 1000
    avgay = sumax / 1000
    avgaz = sumax / 1000
    avggx = sumax / 1000
    avggy = sumax / 1000
    avggz = sumax / 1000

    print("Average Readings: ", avgax, avgay, avgaz, avggx, avggy, avggz)

    return (avgax, avgay, avgaz, avggx, avggy, avggz)


mpu = MPU6050(0x69)

print(
    "Old Offsets: aX = %5d, aY = %5d, aZ = %5d, gX = %5d, gY = %5d, gZ = %5d\n",
    (
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
    "New Offsets: aX = %5d, aY = %5d, aZ = %5d, gX = %5d, gY = %5d, gZ = %5d\n",
    (
        mpu.axoffset,
        mpu.ayoffset,
        mpu.azoffset,
        mpu.gxoffset,
        mpu.gyoffset,
        mpu.gzoffset,
    ),
)

data = mpu.get_raw_data()

ax = data[0] / accel_sensitivity
ay = data[1] / accel_sensitivity
az = data[2] / accel_sensitivity
gx = data[3] / gyro_sensitivity
gy = data[4] / gyro_sensitivity
gz = data[5] / gyro_sensitivity

print(
    "aX = %4.1f g, aY = %4.1f g, aZ = %4.1f g, gX = %6.1f °/s, gY = %6.1f °/s, gZ = %6.1f °/s\n",
    (ax, ay, az, gx, gy, gz),
)
