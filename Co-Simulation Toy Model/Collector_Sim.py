import mosaik_api
import Collector_Model
# metadata for mosaik
META = {
    'type': 'time-based',
    'models': {
        'PowerModel': {
            'public': True,
            'params': [],
            'attrs': ['data']
        }
    }
}


# This class is the simulator for the collector model.
class CollectorSimulator(mosaik_api.Simulator):
    def __init__(self):
        super().__init__(META)
        self.eid_prefix = 'Collector_'
        self.entities = {}
        self.time = 0

    def init(self, sid, time_resolution=1., eid_prefix=None):
        if float(time_resolution) != 1.:
            raise ValueError('CollectorSim only supports time_resolution=1., but %s was set.' % time_resolution)
        if eid_prefix is not None:
            self.eid_prefix = eid_prefix
        return self.meta

    def create(self, num, model):
        next_eid = len(self.entities)
        entities = []

        for i in range(next_eid, next_eid + num):
            collector_instance = Collector_Model.Collector()
            eid = '%s%d' % (self.eid_prefix, i)
            self.entities[eid] = collector_instance
            entities.append({'eid': eid, 'type': collector_instance})
        return entities

    def step(self, time, inputs, max_advance):
        self.time = time
        # Checks for a new power input, and then steps the model forward.
        for eid, model_instance in self.entities.items():
            output_power = 0
            if eid in inputs:
                attrs = inputs[eid]
                for attr, values in attrs.items():
                    output_power = sum(values.values())
            model_instance.step(time, output_power)
        return time + 1

    def get_data(self, outputs):
        # empty dictionary that will produce
        data = {}
        # Checks each of the output items, which are the output values that other simulators want. In our case it will
        # not be checked, but if it did it will just get a power output and time pair.
        for eid, attrs in outputs.items():
            selected_model = self.entities[eid]
            data['time'] = self.time
            data['eid'] = {}
            for attr in attrs:
                if attr not in self.meta['models']['ExampleModel']['attrs']:
                    raise ValueError('Unknown output attribute: %s' % attr)
                data[eid][attr] = getattr(selected_model, attr)
        # returns all data asked for by other simulators
        return data


# This is how we start the simulator.
def main():
    return mosaik_api.start_simulation(CollectorSimulator())


if __name__ == '__main__':
    main()
