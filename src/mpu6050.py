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
    GRAVITY = 9.80665

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

    @axoffset.setter
    def axoffset(self, offset):
        self.write_word(self.ACCEL_XOFF, offset)

    @property
    def ayoffset(self):
        return self.read_word(self.ACCEL_YOFF)

    @ayoffset.setter
    def ayoffset(self, offset):
        self.write_word(self.ACCEL_YOFF, offset)

    @property
    def azoffset(self):
        return self.read_word(self.ACCEL_ZOFF)

    @azoffset.setter
    def azoffset(self, offset):
        self.write_word(self.ACCEL_ZOFF, offset)

    @property
    def gxoffset(self):
        return self.read_word(self.GYRO_XOFF)

    @gxoffset.setter
    def gxoffset(self, offset):
        self.write_word(self.GYRO_XOFF, offset)

    @property
    def gyoffset(self):
        return self.read_word(self.GYRO_YOFF)

    @gyoffset.setter
    def gyoffset(self, offset):
        self.write_word(self.GYRO_YOFF, offset)

    @property
    def gzoffset(self):
        return self.read_word(self.GYRO_ZOFF)

    @gzoffset.setter
    def gzoffset(self, offset):
        self.write_word(self.GYRO_ZOFF, offset)

    @property
    def gyro_raw(self):

        x = self.read_word(self.GYRO_XOUT)
        y = self.read_word(self.GYRO_YOUT)
        z = self.read_word(self.GYRO_ZOUT)

        return [x, y, z]

    @property
    def gyro(self):

        raw = mpu.gyro_raw

        gx = raw[0] / self.GYRO_SCALE_MODIFIER_250DEG
        gy = raw[1] / self.GYRO_SCALE_MODIFIER_250DEG
        gz = raw[2] / self.GYRO_SCALE_MODIFIER_250DEG

        return [gx, gy, gz]

    @property
    def accel_raw(self):

        x = self.read_word(self.ACCEL_XOUT)
        y = self.read_word(self.ACCEL_YOUT)
        z = self.read_word(self.ACCEL_ZOUT)

        return [x, y, z]

    @property
    def acceleration(self):

        raw = mpu.accel_raw

        ax = (raw[0] / self.ACCEL_SCALE_MODIFIER_2G) * self.GRAVITY
        ay = (raw[1] / self.ACCEL_SCALE_MODIFIER_2G) * self.GRAVITY
        az = (raw[2] / self.ACCEL_SCALE_MODIFIER_2G) * self.GRAVITY

        return [ax, ay, az]


if __name__ == "__main__":

    mpu = MPU6050(0x69)

    print(mpu.gyro_raw)
    print(mpu.gyro)

    print(mpu.accel_raw)
    print(mpu.acceleration)
