#! /usr/bin/env python
import friction_tools as ft

# create the simulation containing two atoms
simu = ft.FrictionSimulation()
simu.create_atoms(element='C',positions=[[0, 0, 0],
                                         [6, 0, 0]])

# create an interaction between the two atoms
simu.create_interaction(['C','C'],strength=10.0,equilibrium_distance=5.0)

# give the atoms some initial velocities
vs = [[0.1, 0, 0],[-0.1, 0, 0]]
simu.set_velocities(indices=range(2), velocity=vs)

# tell that we want to run the simulation with default settings
simu.create_dynamics()

# tell that we want to record the movement of the atoms
simu.save_trajectory_during_simulation(interval=5)

# run the simulation for 1000 fs
print "starting simulation"
simu.run_simulation(time=1000.0)
print "finished simulation"

# after finishing, create an xyz-file for viewing what happened
ft.trajectory_to_xyz()
