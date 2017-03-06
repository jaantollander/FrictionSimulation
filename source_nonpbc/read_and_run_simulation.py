import datetime
import numpy as np
import time
import pickle
import friction_tools as ft
import extra_tools as et


def read_and_run_simulation(simulation_time=1000,
                            set_velocity=[0.50, 0.0, 0.0],
                            set_force=None,
                            set_interval=1,
                            root_path='/u/76/tolland1/unix/Desktop/',
                            set_folder_name='simulation_number'):
    """
    Run a simulation from initialised trajectory.

    :param simulation_time: Simulation time
    :param set_velocity: The velocity given to object.
    :param set_force: The force acting on the object. Default is None, which loads the force used in the initialising. If value is given it will be used instead of the force in the initialisement.
    :param set_interval: Interval for gathering data. (How often the gathered data is saved.)
    :param root_path: Root path for saving data.
    :param set_folder_name: The folder where the simulations is saved. If already exists, existing one is overwritten
    :return: Trajectory of the simulation saved in the folder defined.
    """

    # Initialise folder to root path
    folder_path = root_path + set_folder_name + '/'
    et.init_dir(path=folder_path)

    # load initialised simulation
    infile = open('initialise.pkl', 'rb')
    folder_load = pickle.load(file=infile)
    infile.close()

    infile = open(folder_load + 'simulation_config.pkl', 'rb')
    configs = pickle.load(file=infile)
    infile.close()

    [element_surf,
     dims_surf,
     element_obj,
     dims_obj,
     get_force,
     lennardjones_surf,
     lennardjones_obj,
     lennardjones_surfojb] = configs

    if set_force is None:
        set_force = get_force

    date_and_time = datetime.datetime.today()
    get_date = date_and_time.strftime('%d.%m.%Y')
    get_time = date_and_time.strftime('%H:%M:%S')
    output = open(folder_path + 'info.txt', 'w')
    info = 'Date: {0}\nTime: {1}\nSimulation time: {2}\nSurface: {3} {4}\nObject: {5} {6}\nForce: {7}\nVelocity: {8}'
    output.write(info.format(get_date,
                             get_time,
                             simulation_time,
                             element_surf,
                             dims_surf,
                             element_obj,
                             dims_obj,
                             set_force,
                             set_velocity))
    output.close()

    '''
    Simulation
    '''
    simulation = ft.FrictionSimulation()

    simulation.continue_from_trajectory(filename=folder_load + 'simulation.traj')

    # Fix positions of the bottom slab
    bottom_indices = simulation.get_indices_z_less_than(z_limit=-2 * dims_surf[2] + 0.1)
    simulation.fix_positions(indices=bottom_indices, xyz=[True, True, True])

    # For restricting thermostat
    indices_surf_unfixed = simulation.get_indices_z_more_than(z_limit=-2 * dims_surf[2])

    # Velocities
    indices_obj = simulation.get_indices_by_element(element=element_obj)
    velocities_obj = np.ones([len(indices_obj), 3], dtype='float')
    velocities_obj = velocities_obj * np.array(set_velocity)
    simulation.set_velocities(indices=indices_obj, velocity=velocities_obj)

    # Force
    if set_force is None:
        print 'Force is not set.'
    else:
        simulation.add_constant_force(indices=indices_obj, force=set_force)

    # Interacting lennard-jones forces between the particles.
    simulation.create_interaction([element_surf, element_surf],
                                  strength=lennardjones_surf[0],
                                  equilibrium_distance=lennardjones_surf[1])

    simulation.create_interaction([element_obj, element_obj],
                                  strength=lennardjones_obj[0],
                                  equilibrium_distance=lennardjones_obj[1])

    simulation.create_interaction([element_surf, element_obj],
                                  strength=lennardjones_surfojb[0],
                                  equilibrium_distance=lennardjones_surfojb[1])

    #
    simulation.list_atoms()

    #
    simulation.create_dynamics(dt=1.0,
                               temperature=300,
                               coupled_indices=indices_surf_unfixed,
                               strength=0.01)

    # Trajectory
    simulation.save_trajectory_during_simulation(interval=set_interval,
                                                 filename=folder_path + 'simulation.traj')
    # Energy and Temperature
    simulation.gather_energy_and_temperature_during_simulation(interval=set_interval,
                                                               filename=folder_path + 'energy.txt')
    # Work
    simulation.gather_total_work_during_simulation(interval=set_interval,
                                                   indices=indices_surf_unfixed,
                                                   filename=folder_path + 'work_tot_surf.txt')
    simulation.gather_total_work_during_simulation(interval=set_interval,
                                                   indices=indices_obj,
                                                   filename=folder_path + 'work_tot_obj.txt')

    # Average positions
    simulation.gather_average_position_during_simulation(interval=set_interval,
                                                         filename=folder_path + 'avr_positions_surf.txt',
                                                         indices=indices_surf_unfixed)
    simulation.gather_average_position_during_simulation(interval=set_interval,
                                                         filename=folder_path + 'avr_positions_obj.txt',
                                                         indices=indices_obj)

    # Velocities
    simulation.gather_velocities_during_simulation(interval=simulation_time,
                                                   filename=folder_path + 'velocities_surf.txt',
                                                   indices=indices_surf_unfixed)
    simulation.gather_velocities_during_simulation(interval=simulation_time,
                                                   filename=folder_path + 'velocities_obj.txt',
                                                   indices=indices_obj)

    # Print Stats during simulation
    simulation.print_stats_during_simulation(interval=5.0)

    # Time the simulation
    t0 = time.time()
    simulation.run_simulation(time=simulation_time)
    t1 = time.time()

    runtime = "{ti} s".format(ti=str(int(t1 - t0)))
    output = open(folder_path + 'info.txt', 'a')
    output.write('\nRuntime: {0}'.format(runtime))
    output.close()
    print 'Time taken {0}'.format(runtime)


    # Convert .traj to .xyz
    ft.trajectory_to_xyz(filename_in=folder_path + 'simulation.traj',
                         filename_out=folder_path + 'simulation.xyz')