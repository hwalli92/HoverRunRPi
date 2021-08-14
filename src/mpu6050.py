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
    ACCEL_XOFF = 0x06
    ACCEL_YOFF = 0x08
    ACCEL_ZOFF = 0x0A

    GYRO_XOUT = 0x43
    GYRO_YOUT = 0x45
    GYRO_ZOUT = 0x47
    GYRO_XOFF = 0x13
    GYRO_YOFF = 0x15
    GYRO_ZOFF = 0x17

    ACCEL_SCALE_MODIFIER_2G = 16384.0
    GYRO_SCALE_MODIFIER_250DEG = 131.0

    def __init__(self, devaddr, bus=1):
        self.mpuaddr = devaddr
        self.bus = smbus.SMBus(bus)

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

    def write_word(self, memregister, value):
        if value < 0:
            word = 65535 + 1 - (-value)
        else:
            word = value

        high = value >> 8
        low = value & 0xFF

        self.bus.write_byte_data(self.mpuaddr, memregister, high)
        self.bus.write_byte_data(self.mpuaddr, memregister + 1, low)

    @property
    def axoffset(self):
        return self.read_word(self.ACCEL_XOFF)

    @property
    def ayoffset(self):
        return self.read_word(self.ACCEL_YOFF)

    @property
    def azoffset(self):
        return self.read_word(self.ACCEL_ZOFF)

    @property
    def gxoffset(self):
        return self.read_word(self.GYRO_XOFF)

    @property
    def gyoffset(self):
        return self.read_word(self.GYRO_YOFF)

    @property
    def gzoffset(self):
        return self.read_word(self.GYRO_ZOFF)

    @axoffset.setter
    def axoffset(self, offset):
        self.write_word(self.ACCEL_XOFF, offset)

    @ayoffset.setter
    def ayoffset(self, offset):
        self.write_word(self.ACCEL_YOFF, offset)

    @azoffset.setter
    def azoffset(self, offset):
        self.write_word(self.ACCEL_ZOFF, offset)

    @gxoffset.setter
    def gxoffset(self, offset):
        self.write_word(self.GYRO_XOFF, offset)

    @gyoffset.setter
    def gyoffset(self, offset):
        self.write_word(self.GYRO_YOFF, offset)

    @gzoffset.setter
    def gzoffset(self, offset):
        self.write_word(self.GYRO_ZOFF, offset)

    def get_gyro_data(self, raw=False):

        x = self.read_word(self.GYRO_XOUT)
        y = self.read_word(self.GYRO_YOUT)
        z = self.read_word(self.GYRO_ZOUT)

        scaler = self.GYRO_SCALE_MODIFIER_250DEG

        if raw is True:
            return [x, y, z]
        else:
            return [x / scaler, y / scaler, z / scaler]

    def get_accel_data(self, raw=False):

        x = self.read_word(self.ACCEL_XOUT)
        y = self.read_word(self.ACCEL_YOUT)
        z = self.read_word(self.ACCEL_ZOUT)

        scaler = self.ACCEL_SCALE_MODIFIER_2G

        if raw is True:
            return [x, y, z]
        else:
            return [x / scaler, y / scaler, z / scaler]


if __name__ == "__main__":

    mpu = MPU6050(0x69)

    gyro_raw = mpu.get_gyro_data(raw=True)
    print(gyro_raw)
    print(mpu.get_gyro_data())

    print(mpu.get_accel_data(raw=True))
    print(mpu.get_accel_data())

    mpu.axoffset = mpu.get_accel_data(raw=True)[0]
    print(mpu.axoffset)
