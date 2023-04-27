import numpy as np


class SunModel:

    # simulates sunlight collected (not really but as a proof of concept)
    def __init__(self, init_val):
        self.val = init_val
        self.delta = .1
        self.x = 0

    # A sine wave is used to simulate the value collected by the solar panels.
    def step(self):
        self.x += self.delta
        holder = np.sin(self.x/4)
        if holder < 0:
            self.val = 0
        else:
            self.val = holder
