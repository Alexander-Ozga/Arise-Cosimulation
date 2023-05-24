import pandas as pd


# This class defines the model for the collector. It will essentially check the time and corresponding input, then add
# them to a dictionary. At the end it will be converted into a pandas data frame which will then be turned into a CSV.
class Collector:
    # Initializes its parameters in this section of the data.
    def __init__(self):
        self.df = None
        self.data = {'time': [], 'power_output': []}

    # The Step is just appending the data to the overall dictionary.
    def step(self, new_time, new_output):
        self.data['time'].append(new_time)
        self.data['power_output'].append(new_output)

    # Converts data to CSV
    def finalize(self):
        self.df = pd.DataFrame(self.data)
        self.df.to_csv("Example_Data_Collected")
