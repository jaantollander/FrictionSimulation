#! /usr/bin/env python

import friction_tools as ft

simu = ft.FrictionSimulation()

simu.create_slab(element='Au',xy_cells=3,z_cells=2,top_z=0.0)

simu.create_interaction(['Au','Au'], strength=1.0, equilibrium_distance=2.375)

simu.create_dynamics()
simu.print_stats_during_simulation(interval=50.0)
simu.save_trajectory_during_simulation(interval=50.0)
simu.run_simulation(time=10000.0)

ft.trajectory_to_xyz()