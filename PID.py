class PID:
    """PID Controller"""

    def __init__(self, Kp, Ki, Kd, setpoint):
        """
        Initialize the PID controller with gains and setpoint
        :param Kp: Proportional gain
        :param Ki: Integral gain
        :param Kd: Derivative gain
        :param setpoint: Desired value
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.integral = 0
        self.last_error = 0

    def update(self, measured_value, dt):
        """
        Update the PID controller.
        :param measured_value: Current measured value
        :param dt: Time interval since last update
        :return: Control variable
        """
        error = self.setpoint - measured_value
        self.integral += error * dt
        derivative = (error - self.last_error) / dt

        # PID output
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # Update last error
        self.last_error = error

        return output