from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.05


class BatteryMonitor:
    def __init__(self):
        self.monitor = INA219(SHUNT_OHMS)
        self.monitor.configure()

    def get_power(self):
        return self.monitor.power
