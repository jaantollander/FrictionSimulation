#! /usr/bin/env python

import friction_tools as ft

simu = ft.FrictionSimulation()

# load the end configuration of the previous simulation
simu.continue_from_trajectory()

# change all the atoms in the top slab to silver:
# - find the original top slab
high_indices = simu.get_indices_z_more_than(1)
# - copy the original top slab
simu.duplicate_atoms(element='Ag', indices=high_indices)
# - remove the original top slab
simu.remove_atoms(high_indices)

# replace the damaged bottom slab with a perfect one
# - find the original bottom slab
low_indices = simu.get_indices_z_less_than(1)
# - remove the original bottom slab
simu.remove_atoms(low_indices)
# - create a new slab
simu.create_slab(element='Au',xy_cells=3,z_cells=2,top_z=0.0)

# create interactions
simu.create_interaction(['Au','Au'], 1.0, 2.375)
simu.create_interaction(['Ag','Ag'], 1.0, 1.781)
simu.create_interaction(['Au','Ag'], 0.01, 2.5)

simu.set_temperature(300)
simu.create_dynamics(dt=1.0, temperature=300)

# fix the slabs
top_indices = simu.get_indices_z_more_than(11)
bottom_indices = simu.get_indices_z_less_than(-3.5)
simu.fix_positions(top_indices)
simu.fix_positions(bottom_indices)
simu.print_stats_during_simulation(interval=50.0)

# save the trajectory in a new file (so that we don't overwrite the old one)
simu.save_trajectory_during_simulation(interval=50.0, filename='test.traj')

# run for a while to let the system find a stable configuration
simu.run_simulation(time=2000.0)

# push the top slab down
simu.remove_constraints()
simu.fix_velocities(top_indices,[0,0,-0.002])
simu.fix_positions(bottom_indices)

threshold = 3.0

low_indices = simu.get_indices_z_less_than(threshold)
# approach the surface until the first silver atoms reach it
# this can be monitored, e.g., by counting the atoms below a certain
# threshold
while len(low_indices) == len(simu.get_indices_z_less_than(threshold)):
    simu.run_simulation(100.0)


# write the geometry file - remember to read the correct trajectory
ft.trajectory_to_xyz(filename_in='test.traj')