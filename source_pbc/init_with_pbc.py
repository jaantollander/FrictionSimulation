import time
import pickle
import datetime
import numpy as np
import friction_tools as ft
import extra_tools as et


def init_simulation(simulation_time=1000,
                    element_surf='Au',
                    dims_surf=(3, 8),
                    element_obj='C',
                    dims_obj=(3, 3, 3),
                    set_force=[0.0, 0.0, -0.01],
                    set_interval=10,
                    root_path='/u/76/tolland1/unix/Desktop/',
                    set_folder_name='initialise_number'):
    """
    Initialises a surface without periodic boundary conditions and a brick on top of the surface:

    :param simulation_time: Simulation time
    :param element_surf: Chemical symbol for the surface element.
    :param dims_surf: Dimensions in (xy-cells, z-size) format
    :param element_obj: Chemical symbol for the object element.
    :param dims_obj: Dimensions in (x, y, z) format
    :param set_force: Force acting on the object.
    :param set_interval: Interval for gathering data. (How often the gathered data is saved.)
    :param root_path: Root path for saving data.
    :param set_folder_name: The folder where the simulations is initialised. If already exists, existing one is overwritten
    :return: Trajectory of the initialised simulation saved in the folder defined.
    """

    # Lennard-Jones constants
    lennardjones_surf = [1.0, 2.39]
    lennardjones_obj = [2.0, 1.414]
    lennardjones_surfojb = [0.1, 1.414]

    '''
    Define the initialise folder and save it to initialise.pkl
    Save simulation details and sate to file
    '''
    folder_path = root_path + set_folder_name + '/'
    et.init_dir(path=folder_path)

    output = open('initialise.pkl', 'wb')
    pickle.dump(obj=folder_path, file=output)
    output.close()

    date_and_time = datetime.datetime.today()
    get_date = date_and_time.strftime('%d.%m.%Y')
    get_time = date_and_time.strftime('%H:%M:%S')
    output = open(folder_path + 'info.txt', 'w')
    info = 'Date: {0}\n' \
           'Time: {1}\n' \
           'Simulation time: {2}\n' \
           'Surface: {3} {4}\n' \
           'Object:  {5}  {6}\n' \
           'Force: {7}\n' \
           'Lennard-Jones Coefficients: [epsilon, sigma]\n' \
           'Surface:  {8}\n' \
           'Object:   {9}\n' \
           'Obj-Surf: {10}\n'
    output.write(info.format(get_date,
                             get_time,
                             simulation_time,
                             element_surf,
                             dims_surf,
                             element_obj,
                             dims_obj,
                             set_force,
                             lennardjones_surf,
                             lennardjones_obj,
                             lennardjones_surfojb))
    output.close()

    '''
    Simulation
    '''
    simulation = ft.FrictionSimulation()

    '''
    Surface with pbc.
    Bottom of the surface is fixed in its initial position.
    '''
    simulation.create_slab(element=element_surf, xy_cells=dims_surf[0], z_cells=dims_surf[1], top_z=0.0)

    # Fix positions of the bottom
    z_min = np.array([atom.z for atom in simulation.system if atom.symbol is element_surf], dtype='float')
    z_min = np.min(z_min)
    bottom_indices = [atom.index for atom in simulation.system if atom.z == z_min]
    simulation.fix_positions(indices=bottom_indices, xyz=[True, True, True])

    # For restricting thermostat
    indices_surf_unfixed = simulation.get_indices_z_more_than(z_limit=z_min)

    '''
    Object.
    '''
    positions_obj = et.brick(x_width=dims_obj[0],
                             y_width=dims_obj[1],
                             z_width=dims_obj[2],
                             x_pos=1,
                             y_pos=0,
                             z_pos=2)

    simulation.create_atoms(element=element_obj,
                            positions=positions_obj)

    indices_obj = simulation.get_indices_by_element(element=element_obj)

    # Force
    if set_force is None:
        print 'Force is not set.\nRemember to add a force when running the actual simulation'
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

    # Save configs
    configs = [element_surf,
               dims_surf,
               element_obj,
               dims_obj,
               set_force,
               lennardjones_surf,
               lennardjones_obj,
               lennardjones_surfojb,
               bottom_indices,
               indices_surf_unfixed]

    output = open(folder_path + 'simulation_config.pkl', 'wb')
    pickle.dump(obj=configs, file=output)
    output.close()

    # simulation.list_atoms()

    simulation.create_dynamics(dt=1.0,
                               temperature=300,
                               coupled_indices=indices_surf_unfixed,
                               strength=0.01)

    # Trajectory
    simulation.save_trajectory_during_simulation(interval=set_interval,
                                                 filename=folder_path + 'simulation.traj')

    simulation.print_stats_during_simulation(interval=5.0)

    # Time the simulation
    t0 = time.time()
    simulation.run_simulation(time=simulation_time)
    t1 = time.time()

    runtime = "{ti} s".format(ti=str(int(t1 - t0)))
    output = open(folder_path + 'info.txt', 'a')
    output.write('Runtime: {0}'.format(runtime))
    output.close()
    print 'Time taken {0}'.format(runtime)

    # Convert .traj to .xyz
    ft.trajectory_to_xyz(filename_in=folder_path + 'simulation.traj',
                         filename_out=folder_path + 'simulation.xyz')