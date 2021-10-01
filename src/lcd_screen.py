import time
import threading
import liquidcrystal_i2c
import random

COLS = 20
ROWS = 4


class LCDScreen(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)

        self.serial = serial_port
        self.shutdown_flag = threading.Event()
        self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=ROWS)

    def run(self):
        self.lcd.printline(1, "Welcome".center(COLS))
        self.lcd.printline(2, "To HoverRun".center(COLS))
        time.sleep(1)
        self.lcd.clear()

        while not self.shutdown_flag.isSet():
            status = self.getHBStatus()

            self.clearLCDLine(0)
            self.lcd.printline(0, "Hoverbrd Batt:{}V".format(status[9]))
            
            self.clearLCDLine(1)
            self.lcd.printline(
                1, "L:{} R:{} S:{}".format(status[1], status[3], status[5])
            )

            self.clearLCDLine(2)
            self.lcd.printline(
                2, "P:{}, R:{}".format(status[7], status[11])
            )
            
            self.clearLCDLine(3)
            self.lcd.printline(
                3, "{}, {}, {}".format(status[13], status[15], status[17])
            )

            time.sleep(3)

        self.lcd.clear()
        self.lcd.printline(1, "Exiting".center(COLS))
        self.lcd.printline(2, "HoverRun".center(COLS))
        time.sleep(1)
        self.lcd.clear()

    def getHBStatus(self):
        self.serial.write("status")
        status = self.serial.read()
        print(status)

        values = [value for value in status.replace(":", " ").split()]

        return values

    def clearLCDLine(self, line):
        self.lcd.setCursor(0, line)
        for n in range(0, COLS):
            self.lcd.printstr(" ")
