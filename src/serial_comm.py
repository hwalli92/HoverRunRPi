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

    def serial_write(self, msg):

        payload = msg + "\r\n"
        self.ser.write(msg.encode("utf-8"))

    def serial_response(self):
        data = ""
        while True:
            if ser.inWaiting() > 0:
                rcv = self.ser.read()
                if rcv.decode("utf-8") != "\r":
                    data += rcv.decode("utf-8")
                else:
                    return data
