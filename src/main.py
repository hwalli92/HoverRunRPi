from threading import Thread
import time
import signal

import serial_comm
import motor_control
import lcd_screen
import mqtt
import pid_controller
import imu_sensor


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """

    pass


def service_shutdown(signum, frame):
    print("Caught signal %d" % signum)
    raise ServiceExit


def main():

    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    print("Starting main program")

    try:
        serial = serial_comm.SerialComm()
        mqtt_server = mqtt.MQTTServer(serial)

        # t1 = pid_controller.PIDController(serial)
        t1 = imu_sensor.IMUSensor(serial)
        t2 = motor_control.MotorControl(serial, mqtt_server)
        t3 = lcd_screen.LCDScreen(serial, mqtt_server)

        t1.start()
        t2.start()
        t3.start()

        while True:
            time.sleep(0.5)

    except ServiceExit:
        t1.shutdown_flag.set()
        t2.shutdown_flag.set()
        t3.shutdown_flag.set()

        t1.join()
        t2.join()
        t3.join()

    serial.close_serial()
    mqtt_server.disconnect()
    print("Exiting main program")


if __name__ == "__main__":
    main()
