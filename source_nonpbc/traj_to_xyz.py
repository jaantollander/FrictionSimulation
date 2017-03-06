import pickle
# import friction_tools as ft


# def xyz(folder_path='initialise3/'):
# ft.trajectory_to_xyz(filename_in=folder_path + 'simulation.traj',
#                          filename_out=folder_path + 'simulation.xyz')


def create_configs(folder_path='/u/76/tolland1/unix/Desktop/',
                   element_surf='Au',
                   dims_surf=(20, 8, 5),
                   element_obj='C',
                   dims_obj=(3, 3, 3),
                   set_force=[0.0, 0.0, 0.0],
                   lennardjones_surf=[1.0, 1.414],
                   lennardjones_obj=[1.0, 1.414],
                   lennardjones_surfojb=[0.1, 1.414]):
    configs = [element_surf,
               dims_surf,
               element_obj,
               dims_obj,
               set_force,
               lennardjones_surf,
               lennardjones_obj,
               lennardjones_surfojb]

    output = open(folder_path + 'simulation_config.pkl', 'wb')
    pickle.dump(obj=configs, file=output)
    output.close()


create_configs(folder_path='',
               element_surf='Au',
               dims_surf=(20, 8, 5),
               element_obj='C',
               dims_obj=(3, 3, 3),
               set_force=[0.0, 0.0, -0.04],
               lennardjones_surf=[1.0, 1.414],
               lennardjones_obj=[1.0, 1.414],
               lennardjones_surfojb=[0.1, 1.414])