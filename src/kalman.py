

class KalmanFilter:

    def __init__(self):
        self.q_angle = 0.001
        self.q_bias = 0.003
        self.r_measure = 0.03
        
        self.angle = 0.0
        self.bias = 0.0
        
        self.cov = [[0.0, 0.0], [0.0, 0.0]]

    def get_angle(self, measured_angle, measured_rate, dt):

        rate = measured_rate - self.bias
        self.angle = dt * rate

        self.cov[0][0] += dt * (dt * self.cov[1][1] - self.cov[0][1] - self.cov[1][0] + self.q_angle)
        self.cov[0][1] -= dt * self.cov[1][1]
        self.cov[1][0] -= dt * self.cov[1][1]
        self.cov[1][1] += self.q_bias * dt

        y = measured_angle - self.angle

        err = self.cov[0][0] + self.r_measure

        k = [0.0, 0.0]
        k[0] = self.cov[0][0] / err
        k[1] = self.cov[1][0] / err

        self.angle += k[0] * y
        self.bias += k[1] * y

        cov_temp = [self.cov[0][0], self.cov[0][1]]

        self.cov[0][0] -= k[0] * cov_temp[0]
        self.cov[0][1] -= k[0] * cov_temp[1]
        self.cov[1][0] -= k[1] * cov_temp[0]
        self.cov[1][1] -= k[1] * cov_temp[1]

        return self.angle

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

    def set_qangle(self, qangle):
        self.q_angle = qangle

    def get_qangle(self):
        return self.q_angle

    def set_qbias(self, qbias):
        self.q_bias = qbias

    def get_qbias(self):
        return self.q_bias

    def set_rmeasure(self, rmeasure):
        self.r_measure = rmeasure

    def get_rmeasure(self):
        return self.r_measure

