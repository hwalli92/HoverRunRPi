import time


class PID:
    def __init__(self, kp, ki, kd, setpoint):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.iterm = 0
        self.last_time = 0
        self.last_value = 0
        self.max_value = 500

    def pid_compute(self, current):

        this_time = time.time()
        dt = this_time - self.last_time
        self.last_time = this_time

        error = self.setpoint - current

        self.iterm += error * dt

        dterm = (self.last_value - current) / dt

        self.last_value = current

        pidvalue = (error * self.kp) + (self.iterm * self.ki) + (dterm * self.kd)

        if pidvalue > self.max_value:
            return self.max_value
        elif pidvalue < -self.max_value:
            return -self.max_value

        return pidvalue

    def set_kp(self, kp):

        self.kp = kp

    def set_ki(self, ki):

        self.ki = ki

    def set_kd(self, kd):

        self.kd = kd
