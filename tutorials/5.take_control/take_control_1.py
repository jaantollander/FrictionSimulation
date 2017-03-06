#! /usr/bin/env python

import friction_tools as ft

simu = ft.FrictionSimulation()

# create two slabs
simu.create_slab(element='Au',xy_cells=3,z_cells=2,top_z=0.0)
simu.create_slab(element='Ag',xy_cells=4,z_cells=2,bottom_z=5.0)

# create interactions
simu.create_interaction(['Au','Au'], 1.0, 2.375)
simu.create_interaction(['Ag','Ag'], 1.0, 1.781)
simu.create_interaction(['Au','Ag'], 0.1, 2.0)

au_indices = simu.get_indices_by_element('Au')
ag_indices = simu.get_indices_by_element('Ag')
bottom_indices = simu.get_indices_z_less_than(-3.5)
top_indices = simu.get_indices_z_more_than(8.0)

simu.create_dynamics(dt=1.0, temperature=300)
simu.save_trajectory_during_simulation(interval=50.0)
simu.print_stats_during_simulation(interval=50.0)

# time the simulation
import time
t0 = time.time()

# fix the bottom slab and make the top slab move down
simu.fix_velocities(top_indices, [0, 0, -0.005], [True,True,True])
simu.set_temperature(300)
simu.fix_positions(bottom_indices)

print "starting simulation, pushing down"
simu.run_simulation(time=500.0)

# make both slabs stationary
simu.remove_constraints()
simu.fix_positions(top_indices)
simu.fix_positions(bottom_indices)

print "continue simulation, hold still"
simu.run_simulation(time=500.0)

# make the top slab move up
simu.remove_constraints()
simu.fix_velocities(top_indices, [0, 0, 0.002], [True,True,True])
simu.fix_positions(bottom_indices)

print "continue simulation, pull up"
simu.run_simulation(time=3000.0)

ft.trajectory_to_xyz()