
class MotorControl:
    def __init__(self, ser):
        self.speed = 100
        self.steer = 0
        self.ser = ser

    def speed_up(self):
        self.speed += 50

    def speed_down(self):
        self.speed -= 50

    def steer_right(self):
        self.steer += 25

    def steer_left(self):
        self.steer -= 25
