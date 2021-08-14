from time import sleep
import smbus


class MPU6050:

    PWR_MGMT_1 = 0x6B
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    GYRO_CONFIG = 0x1B
    ACCEL_CONFIG = 0x1C

    ACCEL_XOUT = 0x3B
    ACCEL_YOUT = 0x3D
    ACCEL_ZOUT = 0x3F

    GYRO_XOUT = 0x43
    GYRO_YOUT = 0x45
    GYRO_ZOUT = 0x47

    ACCEL_SCALE_MODIFIER_2G = 16384.0
    GYRO_SCALE_MODIFIER_250DEG = 131.0

    def __init__(self, devaddr, bus=1):
        self.mpuaddr = devaddr
        self.bus = smbus.SMBus(bus)

        self.bus.write_byte_data(
            self.mpuaddr, self.PWR_MGMT_1, 0x80
        )  # Wake Up and Reset Device

        sleep(0.1)

        self.bus.write_byte_data(
            self.mpuaddr, self.PWR_MGMT_1, 0x01
        )  # Set CLKSEL as PLL Gyro X Ref
        self.bus.write_byte_data(self.mpuaddr, self.SMPLRT_DIV, 0x07)  # Disable DLPF
        self.bus.write_byte_data(self.mpuaddr, self.CONFIG, 0x07)  # Sample Rate = 1 kHz
        self.bus.write_byte_data(
            self.mpuaddr, self.GYRO_CONFIG, 0x00
        )  # Set full scale range = 250 deg/s
        self.bus.write_byte_data(
            self.mpuaddr, self.ACCEL_CONFIG, 0x00
        )  # Set full scale range = 2g

    def read_word(self, memregister):

        high = self.bus.read_byte_data(self.mpuaddr, memregister)
        low = self.bus.read_byte_data(self.mpuaddr, memregister + 1)

        value = (high << 8) + low

        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value

    def get_gyro_data(self, raw=False):

        x = self.read_word(self.GYRO_XOUT)
        y = self.read_word(self.GYRO_YOUT)
        z = self.read_word(self.GYRO_ZOUT)

        scaler = self.GYRO_SCALE_MODIFIER_250DEG

        if raw is True:
            return [x, y, z]
        else:
            return [x, y, z] / scaler

    def get_accel_data(self, raw=False):

        x = self.read_word(self.ACCEL_XOUT)
        y = self.read_word(self.ACCEL_YOUT)
        z = self.read_word(self.ACCEL_ZOUT)

        scaler = self.ACCEL_SCALE_MODIFIER_2G

        if raw is True:
            return [x, y, z]
        else:
            return [x, y, z] / scaler


if __name__ == "__main__":

    mpu = MPU6050(0x69)

    print(mpu.get_gyro_data(raw=True))
    print(mpu.get_gyro_data())

    print(mpu.get_accel_data(raw=True))
    print(mpu.get_accel_data())
