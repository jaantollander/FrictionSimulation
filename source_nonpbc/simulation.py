import init_simulation
import read_and_run_simulation


run_init = False
run_simu = True

indexes = ['0']
forces = [None]

for index, force in zip(indexes, forces):
    if run_init:
        init_simulation.init_simulation(simulation_time=1000,
                                        element_surf='Au',
                                        dims_surf=(20, 8, 5),
                                        element_obj='C',
                                        dims_obj=(3, 3, 3),
                                        set_force=force,
                                        set_interval=10,
                                        root_path='/u/76/tolland1/unix/Desktop/',
                                        set_folder_name='initialise_'+index)

    if run_simu:
        read_and_run_simulation.read_and_run_simulation(simulation_time=1000,
                                                        set_velocity=[0.50, 0.0, 0.0],
                                                        set_force=None,
                                                        set_interval=1,
                                                        root_path='/u/76/tolland1/unix/Desktop/',
                                                        set_folder_name='simulation_'+index)