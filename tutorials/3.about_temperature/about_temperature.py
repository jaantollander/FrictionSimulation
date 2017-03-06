#! /usr/bin/env python

import friction_tools as ft

simu = ft.FrictionSimulation()

simu.create_slab(element='Au',xy_cells=3,z_cells=2,top_z=0.0)
simu.create_atoms(element='Ag',positions=[[5, 5, 10]])
simu.create_interaction(['Au','Au'], strength=1.0, equilibrium_distance=2.39)
simu.create_interaction(['Au','Ag'], strength=0.1, equilibrium_distance=4.0)

au_indices = simu.get_indices_by_element('Au')
ag_indices = simu.get_indices_by_element('Ag')
bottom_indices = simu.get_indices_z_less_than(-3.5)

simu.set_velocities(indices=ag_indices, velocity=[0, 0, -0.5])

# the thermostat will be added here:
simu.create_dynamics(dt=1.0)

simu.save_trajectory_during_simulation(interval=10.0)
simu.print_stats_during_simulation(interval=50.0)
simu.gather_energy_and_temperature_during_simulation(interval=10.0)
simu.gather_average_position_during_simulation(interval=10.0,indices=au_indices,filename='au_position.txt')
simu.gather_average_position_during_simulation(interval=10.0,indices=ag_indices,filename='ag_position.txt')

constraint = 0
if constraint == 1:
    simu.fix_positions(au_indices)
elif constraint == 2:
    simu.fix_positions(bottom_indices)
elif constraint == 3:
    simu.duplicate_atoms(element='C',indices=bottom_indices)
    c_indices = simu.get_indices_by_element('C')
    simu.attach_with_springs(c_indices, bottom_indices, strength=1.0, cutoff=3.0)
    simu.fix_positions(c_indices)

import time
t0 = time.time()

print "starting simulation"
simu.run_simulation(time=5000.0) # increased the simulation time
print "finished simulation"

t1 = time.time()
print "time taken {ti} s".format(ti=str(int(t1-t0)))

ft.trajectory_to_xyz()