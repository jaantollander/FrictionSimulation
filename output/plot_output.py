import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import latexify


class GatherData:
    def __init__(self):
        self.fittings = []
        self.fittings_interval = [[], []]

    def append_fit(self, fit):
        self.fittings.append(fit)

    def append_fit_interval(self, interval):
        self.fittings_interval[0].append(interval[0])
        self.fittings_interval[1].append(interval[1])


data_gather = GatherData()


def plot_energy(plot_number, filename='energy.txt', path=''):
    y_energy = np.genfromtxt(fname=path + filename, dtype=float).T
    simulation_time = y_energy.shape[1] + 1
    x_time = np.arange(start=1, stop=simulation_time, step=1, dtype='int')

    # plt.figure()
    # Energies
    plt.subplot(4, 1, 1)
    plt.plot(x_time, y_energy[0], marker='', label=str(plot_number))
    plt.ylabel('Potential Energy')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplot(4, 1, 2)
    plt.plot(x_time, y_energy[1], marker='', label=str(plot_number))
    plt.ylabel('Kinetic Energy')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.subplot(4, 1, 3)
    plt.plot(x_time, y_energy[2], marker='', label=str(plot_number))
    plt.ylabel('Total Energy')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Temperature
    plt.subplot(4, 1, 4)
    plt.plot(x_time, y_energy[3], marker='', label=str(plot_number))
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def plot_work(plot_number, filenames, path=''):
    data = []
    time = []
    for filename in filenames:
        file = np.genfromtxt(fname=path + filename, dtype=float).T
        file = np.abs(file)
        data.append(file)
        simulation_time = file.size + 1
        time.append(np.arange(start=1, stop=simulation_time, step=1, dtype='int'))

    # plt.figure()
    for i in range(0, len(data)):
        plt.subplot(len(data), 1, i + 1)
        plt.plot(time[i], data[i], marker='', label=plot_number)
        plt.xlabel('Time')
        plt.ylabel(['Work_object', 'Work_surface'][i])
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def plot_positions(plot_number, filenames, path=''):
    data = []
    time = []
    for filename in filenames:
        open_file = np.genfromtxt(fname=path + filename, dtype=float).T
        data.append(open_file)
        simulation_time = open_file.shape[1] + 1
        time.append(np.arange(start=1, stop=simulation_time, step=1, dtype='int'))

    # plt.figure()
    plot_numbers = [[1, 3, 5], [2, 4, 6]]
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            plt.subplot(len(data[i]), len(data), plot_numbers[i][j])
            if i is 1:
                plt.plot(time[i], data[i][j])  # , label=str(plot_number))
            else:
                plt.plot(time[i], data[i][j])
            if j == len(data[i])-1:
                plt.xlabel('Time')
            plt.ylabel(['x', 'y', 'z'][j] + '-Position')
            plt.grid()
            # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def plot_velocities(fig, plot_number, filename, path=''):
    positions = np.genfromtxt(fname=path + filename, dtype='float').T
    velocities = np.diff(positions)
    dimensions = np.shape(velocities)
    timestep = np.arange(start=0, stop=dimensions[1], step=1, dtype='int') + 0.5

    for index in range(0, dimensions[0]):
        ax = fig.add_subplot(dimensions[0], 1, index + 1)
        ax.plot(timestep, velocities[index])  # , label=str(plot_number))

        if index is 0:
            fit_begin = 200
            fit_end = 800
            x = timestep[fit_begin:fit_end]
            y = velocities[index][fit_begin:fit_end]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            print 'slope: {0}\nintercept {1}\nr_value {2}\np_value {3}\nstd_err {4}'.format(slope, intercept, r_value,
                                                                                            p_value, std_err)

            df = fit_end - fit_begin - 2
            slope_interval = stats.t.interval(0.99, df, loc=slope, scale=std_err)
            print 'Confidence interval', slope_interval, '\n'

            data_gather.append_fit(slope)
            data_gather.append_fit_interval(slope_interval)

        if index == 2:
            plt.xlabel('Time')
        plt.ylabel(['x', 'y', 'z'][index] + '-Velocity')
        plt.grid()
        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def plot_forces():
    f_friction = data_gather.fittings
    f_friction_intervals = data_gather.fittings_interval
    f_normal = np.arange(start=1, stop=len(f_friction) + 1, dtype='float') * 0.005

    slope, intercept, r_value, p_value, std_err = stats.linregress(f_normal, f_friction)
    fit = np.array(f_normal, dtype='float') * slope + intercept

    degrees_of_freedom = len(f_normal) - 2
    cdf = 0.67
    slope_interval = stats.t.interval(cdf, degrees_of_freedom, loc=slope, scale=std_err)

    print 'Forces fitvalues'
    print 'slope: {0}\n' \
          'intercept {1}\n' \
          'r_value {2}\n' \
          'p_value {3}\n' \
          'std_err {4}\n' \
          '{cdf}-Confidence interval  {5}'.format(slope, intercept, r_value, p_value, std_err, slope_interval, cdf=cdf)

    plt.plot(f_normal,
             f_friction,
             marker='.',
             linestyle='-.',
             label=r'Frictious Force')

    plt.fill_between(f_normal,
                     f_friction_intervals[1],
                     f_friction_intervals[0],
                     alpha=0.5,
                     edgecolor='#CC4F1B',
                     facecolor='#FF9848')

    plt.plot(f_normal, fit, marker='.', linestyle='-.', label=r'Linear Fit')

    plt.xlabel(r'Normal Force')
    plt.ylabel(r'Frictious Force divided by mass (constant)')
    plt.legend(loc='best')
    plt.grid(True)


def plot_all(list_of_paths,
             fig_path,
             show_work=True,
             show_energy=True,
             show_positions=True,
             show_velocities=True,
             save_fig=False,
             maximize_window=False):

    plt.rc('axes', color_cycle=[str(i) for i in np.linspace(1, 0.05, 24)])
    # ----
    # Work
    # ----
    if show_work:
        plt.figure(figsize=(10, 6))
        for index, folder_path in enumerate(list_of_paths):
            print 'Plotting work: ' + folder_path
            try:
                plot_work(plot_number=index, path=folder_path, filenames=['work_tot_obj.txt', 'work_tot_surf.txt'])
            except IOError:
                pass

        if maximize_window:
            fig_manager = plt.get_current_fig_manager()
            fig_manager.window.showMaximized()
        if save_fig:
            plt.savefig(fig_path + 'work.pdf')
        print ''
    else:
        pass

    # ---------------------
    # Energy & Temprerature
    # ---------------------
    if show_energy:
        plt.figure(figsize=(10, 6))
        for index, folder_path in enumerate(list_of_paths):
            print 'Plotting energys: ' + folder_path

            try:
                plot_energy(plot_number=index, path=folder_path, filename='energy.txt')
            except IOError:
                pass

        if maximize_window:
            fig_manager = plt.get_current_fig_manager()
            fig_manager.window.showMaximized()
        if save_fig:
            plt.savefig(fig_path + 'energy.pdf')
        print ''
    else:
        pass

    # ---------
    # Positions
    # ---------
    if show_positions:
        plt.figure(figsize=(10, 6))
        for index, folder_path in enumerate(list_of_paths):
            print 'Plotting positions: ' + folder_path

            try:
                plot_positions(plot_number=index,
                               path=folder_path,
                               filenames=['avr_positions_obj.txt', 'avr_positions_surf.txt'])
            except IOError:
                pass

        if maximize_window:
            fig_manager = plt.get_current_fig_manager()
            fig_manager.window.showMaximized()
        if save_fig:
            plt.savefig(fig_path + 'positions.pdf')
        print ''
    else:
        pass

    # ----------
    # Velocities
    # ----------
    if show_velocities:
        fig = plt.figure(figsize=(10, 6))
        for index, folder_path in enumerate(list_of_paths):
            print 'Plotting velocities: ' + folder_path

            try:
                plot_velocities(fig,
                                plot_number=index,
                                path=folder_path,
                                filename='avr_positions_obj.txt')
            except IOError:
                pass

        if maximize_window:
            fig_manager = plt.get_current_fig_manager()
            fig_manager.window.showMaximized()
        if save_fig:
            plt.savefig(fig_path + 'velocities.pdf')
        print ''
    else:
        pass

    plt.rc('axes', color_cycle=['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    # ----------------------------------
    # Frictiounous force vs Normal force
    # ----------------------------------
    plt.figure(figsize=(10, 6))
    print 'Plotting forces'
    try:
        plot_forces()
    except IOError:
        pass

    if maximize_window:
        fig_manager = plt.get_current_fig_manager()
        fig_manager.window.showMaximized()
    if save_fig:
        plt.savefig(fig_path + 'forces.pdf')

    # --------------------------------
    # Display the figure on the screen
    # --------------------------------
    plt.show()


# LaTeX Format
latexify.latexify()

# Paths for plotting
# paths = ['F:/friction_simulations/non_pbc/simulation_{0}/'.format(i) for i in range(0, 7)]
paths = ['F:/friction_simulations/pbc2/simulation_pbc_{0}/'.format(i) for i in range(1, 24)]
# paths = ['F:/friction_simulations/pbc3/simulation_pbc_{0}/'.format(i) for i in range(1,15)+range(16,20)]

plot_all(list_of_paths=paths,
         show_work=False,
         show_energy=False,
         show_positions=False,
         show_velocities=True,
         fig_path='F:/',
         save_fig=True)
