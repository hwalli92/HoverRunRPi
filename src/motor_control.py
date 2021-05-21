import usb.core
import usb.util
import time
import threading

USB_IF = 0  # Interface
USB_TIMEOUT = 5  # Timeout in MS

BTN_LEFT = 79
BTN_RIGHT = 80
BTN_DOWN = 81
BTN_UP = 82
BTN_CTR = 40  # Center Button
BTN_EXIT = 41  # Back Button

USB_VENDOR = 0x1915  # Andoer
USB_PRODUCT = 0x1047  # Universal Remote


class MotorControl(threading.Thread):
    def __init__(self, serial_port):
        threading.Thread.__init__(self)
        self.remote = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
        self.endpoint = self.remote[0][(0, 0)][0]
        if self.remote.is_kernel_driver_active(USB_IF) is True:
            self.remote.detach_kernel_driver(USB_IF)

        usb.util.claim_interface(self.remote, USB_IF)

        self.serial = serial_port

        self.shutdown_flag = threading.Event()
        self.speed = 100
        self.steer = 0
        self.enable = 0

    def run(self):
        while not self.shutdown_flag.isSet():
            remote_input = self.read_remote_input()

            if remote_input:
                print(remote_input)

            time.sleep(1)

    def read_remote_input(self):
        control = None

        try:
            control = self.remote.read(
                self.endpoint.bEndpointAddress,
                self.endpoint.wMaxPacketSize,
                USB_TIMEOUT,
            )
        except:
            pass

        if control != None:
            self.parse_remote_input(control)
            return control
        else:
            return False

    def parse_remote_input(self, control):
        if BTN_DOWN in control:
            print("Down Button Pressed")
            self.speed -= 50
            return self.update_motors()
        elif BTN_UP in control:
            print("UP Button Pressed")
            self.speed += 50
            return self.update_motors()
        elif BTN_LEFT in control:
            print("Left Button Pressed")
            self.steer -= 50
            return self.update_motors()
        elif BTN_RIGHT in control:
            print("Right Button Pressed")
            self.steer += 50
            return self.update_motors()
        elif BTN_CTR in control:
            if self.enable == 0:
                self.enable = 1
                return self.enable_motors()
            else:
                self.enable = 0
                return self.disable_motors()

    def update_motors(self):
        checksum = self.steer + (self.speed * 1000)
        msg = "move {} {} {}".format(self.steer, self.speed, checksum)
        self.serial.write(msg)

        if self.enable == 0:
            self.enable = 1

        return True

    def enable_motors(self):
        self.serial.write("start")
        return True

    def disable_motors(self):
        self.serial.write("stop")
        return True
