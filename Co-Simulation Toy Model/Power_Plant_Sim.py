import mosaik_api
import Power_Plant_Model
# This simulator has the input of an initial power input, but an attribute of the current input and output powers (from
# itself).
META = {
    'type': 'time-based',
    'models': {
        'PowerModel': {
            'public': True,
            'params': ['init_power_in'],
            'attrs': ['power_in', 'out_put']
        }
    }
}


class PowerSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'PowerPlant_'
        self.entities = {}
        self.time = 0

    def init(self, sid, time_resolution=1., eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError('PowerSim only supports time_resolution=1., but'
                             ' %s was set.' % time_resolution)
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, init_power_in):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            power_instance = Power_Plant_Model.PowerModel(init_power_in)
            eid = '%s%d' % (self.eid_prefix, i)
            self.entities[eid] = power_instance
            entities.append({'eid': eid, 'type': power_instance})
        return entities

    # Will take power input from the solar, make it the new power input, and then step time forward.
    def step(self, time, inputs, max_advance):
        self.time = time
        # Checks for a new power input, and then steps the model forward.
        for eid, model_instance in self.entities.items():
            if eid in inputs:
                attrs = inputs[eid]
                new_power_input = 0
                for attr, values in attrs.items():
                    new_power_input = sum(values.values())
                model_instance.power_in = new_power_input
            model_instance.step()
        return time + 1

    def get_data(self, outputs):
        # empty dictionary that will produce
        data = {}
        # Checks each of the output items, which are the output values that other simulators want. In our case it will
        # check for the eid of the power station and will give the current power output of the station.
        for eid, attrs in outputs.items():
            selected_model = self.entities[eid]
            data['time'] = self.time
            data['eid'] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ExampleModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)
                # Gets the output of the specific solar panel
                data[eid][attr] = getattr(selected_model, attr)
        # returns all data asked for by other simulators
        return data


def main():
    return mosaik_api.start_simulation(PowerSimulator())


if __name__ == '__main__':
    main()
