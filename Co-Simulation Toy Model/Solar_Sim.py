import mosaik_api
import Solar_Model

META = {
    'type': 'time-based',
    'models': {
        'SolarModel': {
            'public': True,
            'params': ['init_val'],
            'attrs': ['x', 'val', 'delta']
        }
    }
}


class SolarSim(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Solar_'
        self.entities = {}
        self.time = 0

    def init(self, sid, time_resolution=1., eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError('Solar_sim only supports time_resolution=1., but'
                             ' %s was set.' % time_resolution)
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model, init_val):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            solar_instance = Solar_Model.SunModel(init_val)
            eid = '%s%d' % (self.eid_prefix, i)
            self.entities[eid] = solar_instance
            entities.append({'eid': eid, 'type': solar_instance})
        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        # Checking for update to the Solar Model (i.e. the sun changes position and the new power output is created)
        # The for loop goes through each instance of the entities that it has by eid. If it finds one that Mosaik
        # wants to advance via an if statement, it will use the step method from the model instance (since this model
        # doesn't have any inputs we can just call the method to essentially advance time forward for the solar panel
        # instance). It returns the time + 1 to update mosaik that it has advanced the time forward 1 by 1 step in time.
        for eid, model_instance in self.entities.items():
            if eid in inputs:
                model_instance.step()
        return time + 1

    def get_data(self, outputs):
        # empty dictionary that will produce
        data = {}
        # Checks each of the output items, which are the output values that other simulators want. In our case it will
        # check for the eid of each solar panel and is essentially requesting its power output (val).
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
    return mosaik_api.start_simulation(SolarSim)


if __name__ == '__main__':
    main()
