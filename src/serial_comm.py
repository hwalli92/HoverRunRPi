import time
import serial


class SerialComm:
    def __init__(self):
        self.ser = serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=5.0,
        )
        
        self.ser.flush()

    def write(self, msg):
        payload = msg + "\n"
        self.ser.write(payload.encode("utf-8"))

    def read(self):
        data = ""
        while True:
            if self.ser.inWaiting() > 0:
                rcv = self.ser.read()
                if rcv.decode("utf-8") != "\n":
                    data += rcv.decode("utf-8")
                else:
                    return data

    def close_serial(self):
        self.ser.flush()
        self.ser.close()
