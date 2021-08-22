import time


class PID:
    def __init__(self, kp, ki, kd, setpoint):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.iterm = 0
        self.last_time = None
        self.last_value = 0
        self.max_value = 150

    def pid_compute(self, current):

        now = time.time()
        dt = now - self.last_time if (self.last_time) else 1e-16
        self.last_time = now

        error = self.setpoint - current

        self.iterm += error * dt
        print(self.iterm)
        self.iterm = self.clamp(self.iterm)

        dterm = (self.last_value - current) / dt

        self.last_value = current

        pidvalue = (error * self.kp) + (self.iterm * self.ki) + (dterm * self.kd)
        print(pidvalue)
        pidvalue = self.clamp(pidvalue)

        return pidvalue

    def set_kp(self, kp):

        self.kp = kp

    def set_ki(self, ki):

        self.ki = ki

    def set_kd(self, kd):

        self.kd = kd

    def clamp(self, value):

        if value > self.max_value:
            return self.max_value
        elif value < -self.max_value:
            return -self.max_value

        return value
