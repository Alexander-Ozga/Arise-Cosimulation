class PowerModel:

    def __init__(self, init_power_in):
        self.power_in = init_power_in
        self.output = self.power_in

    # Simply amplifies the power input.
    def step(self):
        self.output = self.power_in * 50
