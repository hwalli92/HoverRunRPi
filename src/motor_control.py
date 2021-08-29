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
    def __init__(self, serial_port, mqtt_server):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()

        self.remote = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)
        self.endpoint = self.remote[0][(0, 0)][0]
        if self.remote.is_kernel_driver_active(USB_IF) is True:
            self.remote.detach_kernel_driver(USB_IF)

        usb.util.claim_interface(self.remote, USB_IF)

        self.serial = serial_port
        self.mqtt = mqtt_server

        self.speed = 50
        self.steer = 0
        self.enable = 0
        self.remote_inputs = {
            BTN_UP: "up",
            BTN_DOWN: "down",
            BTN_LEFT: "left",
            BTN_RIGHT: "right",
            BTN_CTR: "center",
        }

    def run(self):
        while not self.shutdown_flag.isSet():
            self.read_remote()

            time.sleep(1)

        self.disable_motors()

    def read_remote(self):
        control = None

        try:
            control = self.remote.read(
                self.endpoint.bEndpointAddress,
                self.endpoint.wMaxPacketSize,
                USB_TIMEOUT,
            )
        except:
            pass

        if control != None and control[3] != 0:
            print(control)
            motor_control = getattr(self, self.remote_inputs.get(control[3]), lambda: "Invalid Input")
            return motor_control()
        else:
            return False

    def update_motors(self):
        if self.enable == 1:
            checksum = self.steer + (self.speed * 1000)
            msg = "move {} {} {}".format(self.steer, self.speed, checksum)
            self.serial.write(msg)

        return True

    def enable_motors(self):
        print("Starting Motors")
        checksum = self.steer + (self.speed * 1000)
        msg = "move {} {} {}".format(self.steer, self.speed, checksum)
        self.serial.write(msg)
        self.enable = 1

        return True

    def disable_motors(self):
        print("Stopping Motors")
        self.serial.write("stop")
        self.enable = 0

        return True

    def up(self):
        print("UP Button Pressed")
        self.speed += 50

        return self.update_motors()

    def down(self):
        print("DOWN Button Pressed")
        self.speed -= 50

        return self.update_motors()

    def left(self):
        print("LEFT Button Pressed")
        self.steer += 50

        return self.update_motors()

    def right(self):
        print("RIGHT Button Pressed")
        self.steer -= 50

        return self.update_motors()

    def center(self):
        print("CENTER Button Pressed")
        if self.enable == 0:
            return self.enable_motors()
        else:
            return self.disable_motors()
