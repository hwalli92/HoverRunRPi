import time
import threading
import liquidcrystal_i2c

import battery_monitor

COLS = 20
ROWS = 4


class LCDScreen(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)

        self.serial = serial_port
        self.shutdown_flag = threading.Event()
        # self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=ROWS)
        self.pi_battery = battery_monitor.BatteryMonitor()

    def run(self):
        # self.lcd.printline(1, "Welcome".center(COLS))
        # self.lcd.printline(2, "To HoverRun".center(COLS))
        # self.lcd.clear()

        while not self.shutdown_flag.isSet():
            print(self.getHBStatus())
            # self.lcd.printline(1, "HoverRun".center(COLS))
            # self.lcd.printline(
            #     2, "Batt-Pi:{}% HB:{}%".format(self.getPiBattery(), self.getHBBattery())
            # )
            # self.lcd.printline(1, "Speed: {}".format(self.getHBBattery()))
            # self.lcd.printline(2, "Steer: {}".format(self.getHBBattery()))

            time.sleep(5)

        # self.lcd.clear()
        # self.lcd.printline(1, "Exiting".center(COLS))
        # self.lcd.printline(1, "HoverRun".center(COLS))

    def getPiBattery(self):
        return self.pi_battery.get_power()

    def getHBStatus(self):
        self.serial.write("status")
        status = self.serial.read()

        return status
