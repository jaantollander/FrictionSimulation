#! /usr/bin/env python

import friction_tools as ft

simu = ft.FrictionSimulation()

# create a thin glod slab - this will make the system
# periodic in x- and y-directions
simu.create_slab(element='Au',xy_cells=3,z_cells=2,top_z=0.0)

# create a single silver atom
simu.create_atoms(element='Ag',positions=[[5, 5, 10]])

# check the system
simu.list_atoms()

# stop here - remove 'quit()' to carry out the rest of the script
# quit()

# create interactions
simu.create_interaction(['Au','Au'], strength=1.0, equilibrium_distance=2.39)
simu.create_interaction(['Au','Ag'], strength=0.1, equilibrium_distance=4.0)

# list the indices of gold and silver atoms
au_indices = simu.get_indices_by_element('Au')
ag_indices = simu.get_indices_by_element('Ag')

# also list the atoms who are at the bottom of the gold slab
bottom_indices = simu.get_indices_z_less_than(-3.5)

# make the silver atom start with a high velocity towards the gold slab
simu.set_velocities(indices=ag_indices, velocity=[0, 0, -0.5])

# tell that we want to run the simulation with default settings
simu.create_dynamics(dt=1.0)

# tell that we want to collect information:
# - all positions
simu.save_trajectory_during_simulation(interval=10.0)
# - monitor the simulation by printing info to stdout
simu.print_stats_during_simulation(interval=50.0)
# - record energies in a file (default name 'energy.txt')
simu.gather_energy_and_temperature_during_simulation(interval=10.0)
# - record the x y z coordinates of the centre of mass of the Au slab
simu.gather_average_position_during_simulation(interval=10.0,indices=au_indices,filename='au_position.txt')
# - record the x y z coordinates of the Ag atom
simu.gather_average_position_during_simulation(interval=10.0,indices=ag_indices,filename='ag_position.txt')

# constrain the gold slab?
constraint = 0

if constraint == 1:
    # prevent the gold slab from moving
    simu.fix_positions(au_indices)
elif constraint == 2:
    # prevent the bottom of the gold slab from moving
    simu.fix_positions(bottom_indices)
elif constraint == 3:
    # create 'ghost' atoms at the bottom of the slab and attach the bottom to them
    simu.duplicate_atoms(element='C',indices=bottom_indices)
    c_indices = simu.get_indices_by_element('C')
    simu.attach_with_springs(c_indices, bottom_indices, strength=1.0, cutoff=3.0)
    simu.fix_positions(c_indices)

# time the simulation
import time
t0 = time.time()

print "starting simulation"
simu.run_simulation(time=2000.0)
print "finished simulation"

t1 = time.time()
print "time taken {ti} s".format(ti=str(int(t1-t0)))

ft.trajectory_to_xyz()
