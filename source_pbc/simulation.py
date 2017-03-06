import init_with_pbc
import read_and_run_pbc


run_init = True
run_simu = True

# indexes = [0]
# forces = [[None]]

indexes = range(1, 25)
forces = [[0.0, 0.0, -0.005*z] for z in indexes]

# indexes = [1]
# forces = [[0.0, 0.0, -0.01]]

for index, force in zip(indexes, forces):
    if run_init:
        init_with_pbc.init_simulation(simulation_time=400,
                                      element_surf='Au',
                                      dims_surf=(3, 8),
                                      element_obj='C',
                                      dims_obj=(4, 4, 3),
                                      set_force=force,
                                      set_interval=10,
                                      root_path='/u/76/tolland1/unix/Desktop/',
                                      set_folder_name='initialise_pbc_{0}'.format(str(index)))

    if run_simu:
        read_and_run_pbc.read_and_run_simulation(simulation_time=1200,
                                                 set_velocity=[0.50, 0.0, 0.0],
                                                 set_force=None,
                                                 set_interval=1,
                                                 root_path='/u/76/tolland1/unix/Desktop/',
                                                 set_folder_name='simulation_pbc_{0}'.format(str(index)))
