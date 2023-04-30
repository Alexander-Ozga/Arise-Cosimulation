import mosaik.util

# This holds the configuration of the mosaik simulation on the other machines (how to run them).
SIM_CONFIG = {
    'Solar_Sim': {
        'cmd': 'python Solar_Sim.py 10.130.161.192:8000',
        'cwd': 'Desktop/SolarMosaik/'
    },
    'Power_Plant_Sim': {
        'cmd': 'python Power_Plant_Sim.py 10.130.161.196:8000',
        'cwd': 'Desktop/PowerMosaik/'
    },
    'Collector_Sim': {
        'cmd': 'python Collector_Sim.py 10.130.161.193:8000',
        'cwd': 'Desktop/CollectorMosaik/'
    }
}

END = 30

# Create World
world = mosaik.World(SIM_CONFIG)

# Start Simulators
Solar = world.start('Solar_Sim', eid_prefix="solar_panel_")
PowerPlant = world.start('Power_Plant_Sim', eid_prfix="power_plant_")
Collector = world.start('Collector_Sim', eid_prefix="collector_")

# Create Entities
SolarModel = Solar.SolarModel.create(20)
PowerModel = PowerPlant.PowerModel(init_power_in=0)
Recorder = Collector.Recorder()

# Connect Entities
mosaik.util.connect_many_to_one(world, SolarModel, PowerModel, 'x', 'val' 'delta')
world.connect(PowerModel, Recorder, 'power_in', 'out_put')

# Start the simulation
world.run(until=END)
