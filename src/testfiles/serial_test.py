import serial
import time

port = serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1.0,
)
try:
    if port.isOpen():

        while True:
            command = input("Enter Command: \n")
            if command == "exit":
                port.close()
                exit()

            msg = command + "\r\n"

            port.write(msg.encode("utf-8"))

            data = ""
            while True:
                if port.inWaiting() > 0:
                    print("Receiving Data")
                    rcv = port.read()
                    if rcv.decode("utf-8") != "\r":
                        print(rcv.decode("utf-8"))
                        data += rcv.decode("utf-8")
                    else:
                        print(data)
                        break

except KeyboardInterrupt:
    print("Exiting Program")

except:
    print("Error Occurs, Exiting Program")

finally:
    port.close()
    pass
