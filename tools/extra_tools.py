import os
import shutil
import numpy as np


def init_dir(path='folder_path'):
    """
    :param path: Name for the directory.
    :return: Creates a new folder. If folder already exists older one is deleted.
    """

    try:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
    except OSError:
        pass


def brick(x_width=4, y_width=2, z_width=2, x_pos=0.0, y_pos=0.0, z_pos=0.0):
    """
    :param x_width: For x_width=4, width along x-axis will be 2*4, from 0 to 8.
    :param y_width: For y_width=2, width along y-axis will be 2*2
    :param z_width:
    :param x_pos:
    :param y_pos:
    :param z_pos:
    :return: numpy.array of positions for face-centered cubic
    """

    even = np.array(
        [[i, j, k] for i in range(0, x_width + 1) for j in range(0, y_width + 1) for k in
         range(0, z_width + 1)]) * 2

    odd_xy = np.array([[i, j, k] for i in range(0, x_width) for j in range(0, y_width) for k in
                       range(0, z_width + 1)]) * 2 + np.array([1, 1, 0], dtype='int')

    odd_xz = np.array([[i, j, k] for i in range(0, x_width) for j in range(0, y_width + 1) for k in
                       range(0, z_width)]) * 2 + np.array([1, 0, 1], dtype='int')

    odd_yz = np.array([[i, j, k] for i in range(0, x_width + 1) for j in range(0, y_width) for k in
                       range(0, z_width)]) * 2 + np.array([0, 1, 1], dtype='int')

    positions = np.concatenate((even, odd_xy, odd_xz, odd_yz)) + np.array([x_pos, y_pos, z_pos])
    return positions
