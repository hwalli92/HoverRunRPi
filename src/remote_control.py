import usb.core
import usb.util

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

BTN_LEFT  = 79
BTN_RIGHT = 80
BTN_DOWN  = 81
BTN_UP    = 82
BTN_STOP  = 40 # Center Button
BTN_EXIT  = 41 # Back Button

USB_VENDOR  = 0x1915 # Andoer
USB_PRODUCT = 0x1047 # Universal Remote

class RemoteControl():
    
    def __init__(self):
        self.remote = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

        self.endpoint = self.remote[0][(0,0)][0]

        if self.remote.is_kernel_driver_active(USB_IF) is True:
          self.remote.detach_kernel_driver(USB_IF)

        usb.util.claim_interface(self.remote, USB_IF)
        
    def read_remote_input(self):
        control = None
        
        try:
          control = self.remote.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize, USB_TIMEOUT)
          print(control)
          
        except:
          pass
        
        if control != None:
            return self.parse_remote_input(control)
        else:
            return False
        
    def parse_remote_input(self, control):
        if BTN_DOWN in control:
            print("Down Button Pressed")
            return ["green/off", "down"]
        elif BTN_UP in control:
            print("UP Button Pressed")
            return ["green/on", "up"]
        elif BTN_LEFT in control:
            print("Left Button Pressed")
            return ["red/on", "left"]
        elif BTN_RIGHT in control:
            print("Right Button Pressed")
            return ["red/off", "right"]
        elif BTN_STOP in control:
            print("Stop Button Pressed")
            return ["all/off", "stop"]
        elif BTN_EXIT in control:
            print("Exit Button Pressed")
            return "exit"
        
