#! /usr/bin/env python

import friction_tools as ft

simu = ft.FrictionSimulation()

simu.create_atoms('Au', [[02, 0, 0], [0, 0, 1.7]])
simu.create_interaction(['Au', 'Au'], 1.0, 2.0)

simu.create_dynamics(dt=1.0)
simu.fix_positions([0])
simu.fix_velocities([1], [0, 0, 0.01])
simu.print_stats_during_simulation(interval=1.0)
simu.gather_energy_and_temperature_during_simulation(interval=1.0, filename='energy.txt')
simu.gather_average_position_during_simulation(interval=1.0, indices=[1], filename='separation.txt')
simu.gather_average_force_during_simulation(interval=1.0, indices=[1], filename='force.txt')
simu.run_simulation(time=150)