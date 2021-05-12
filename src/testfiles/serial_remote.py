import usb.core
import usb.util
import time
import serial

USB_IF      = 0 # Interface
USB_TIMEOUT = 5 # Timeout in MS

BTN_LEFT  = 79
BTN_RIGHT = 80
BTN_DOWN  = 81
BTN_UP    = 82
BTN_STOP  = 40 # Center Button
BTN_RST   = 101 # Rest Button (3 lines)
BTN_EXIT  = 41 # Back Button

USB_VENDOR  = 0x1915 # Andoer
USB_PRODUCT = 0x1047 # Universal Remote

def serialResponse():
  data = ''
  while True:
    if ser.inWaiting() > 0:
      rcv = ser.read()
      if rcv.decode('utf-8') != '\r':
        data += rcv.decode('utf-8')
      else:
        return data

ser = serial.Serial(
		port="/dev/ttyAMA0",
		baudrate=115200,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout = 5.0
)

dev = usb.core.find(idVendor=USB_VENDOR, idProduct=USB_PRODUCT)

endpoint = dev[0][(0,0)][0]

if dev.is_kernel_driver_active(USB_IF) is True:
  dev.detach_kernel_driver(USB_IF)

usb.util.claim_interface(dev, USB_IF)

steer = 0
speed = 100

try:
  while True:
      control = None

      try:
        control = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, USB_TIMEOUT)
        print (control)
      except:
        pass
        
      if control != None:
        if BTN_DOWN in control:
            print("Down Button Pressed")
            speed -= 25
            ser.write(b'move %d %d %d\r'%(steer,speed,(steer+(speed*1000))))
            print(serialResponse())

        if BTN_UP in control:
            print("UP Button Pressed")
            speed += 25
            ser.write(b'move %d %d %d\r'%(steer,speed,(steer+(speed*1000))))
            print(serialResponse())

        if BTN_LEFT in control:
            print("Left Button Pressed")

        if BTN_RIGHT in control:
            print("Right Button Pressed")

        if BTN_STOP in control:
            print("Stop Button Pressed")
            ser.write(b'stop\r')
            print(serialResponse())
        
        if BTN_RST in control:
            print("Reset Button Pressed")
            speedL = 50
            speedR = 50
            ser.write(b'move %d %d %d\r'%(speedR,speedL,(speedR+speedL)*1000))
            print(serialResponse())
        
        if BTN_EXIT in control:
            print("Exit Button Pressed")
            ser.write(b'poweroff\r')
            print(serialResponse())
            ser.close()
            exit()

      time.sleep(1) # Let CTRL+C actually exit


except KeyboardInterrupt:
     print ("Exiting Program")

except:
     print ("Error Occurs, Exiting Program")

finally:
     ser.close()
     pass			
