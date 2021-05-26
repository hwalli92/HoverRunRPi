import time
import threading
import liquidcrystal_i2c
import random

import battery_monitor

COLS = 20
ROWS = 4


class LCDScreen(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)

        self.serial = serial_port
        self.shutdown_flag = threading.Event()
        self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=ROWS)
        self.pi_battery = battery_monitor.BatteryMonitor()

    def run(self):
        self.lcd.printline(1, "Welcome".center(COLS))
        self.lcd.printline(2, "To HoverRun".center(COLS))
        time.sleep(1)
        self.lcd.clear()
        
        self.lcd.printline(0, "HoverRun".center(COLS))
        
        while not self.shutdown_flag.isSet():
            status = self.getHBStatus()
        
            self.clearLCDLine(1)
            self.lcd.printline(1, "Hoverbrd Battery: {}".format(status[7]))
            self.clearLCDLine(2)
            self.lcd.printline(2, "SPD: L:{} R:{}".format(status[1], status[3]))
            self.clearLCDLine(3)
            self.lcd.printline(3, "Steer: {}".format(status[5]))

            time.sleep(5)

        self.lcd.clear()
        self.lcd.printline(1, "Exiting".center(COLS))
        self.lcd.printline(2, "HoverRun".center(COLS))
        time.sleep(1)
        self.lcd.clear()

    def getHBStatus(self):
        self.serial.write("status")
        status = self.serial.read()
        print(status)

        values = [int(value) for value in status.replace(":", " ").split()]

        return values
        
    def clearLCDLine(self, line):          
        self.lcd.setCursor(0,line)
        for n in range(0,COLS):
            self.lcd.printstr(" ")
