# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
import matplotlib
from math import sqrt


spine_color = 'gray'


def latexify(fig_width=None, fig_height=None, columns=1):
    """
    Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    Width and max height in inches for IEEE journals taken from
    http://www.computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    :param fig_width: float, optional, inches
    :param fig_height: float,  optional, inches
    :param columns: {1, 2}
    """

    assert (columns in [1, 2])

    if fig_width is None:
        fig_width = 3.39 if columns == 1 else 6.9  # width in inches

    if fig_height is None:
        golden_mean = (sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
        fig_height = fig_width * golden_mean  # height in inches

    max_height_inches = 8.0
    if fig_height > max_height_inches:
        print("WARNING: fig_height too large:" + fig_height +
              "so will reduce to" + max_height_inches + "inches.")
        fig_height = max_height_inches

    params = {'backend': 'ps',
              'text.latex.preamble': ['\usepackage{gensymb}'],
              'axes.labelsize': 10,  # fontsize for x and y labels (was 10)
              'axes.titlesize': 10,
              'text.fontsize': 10,  # was 10
              'legend.fontsize': 10,  # was 10
              'xtick.labelsize': 10,
              'ytick.labelsize': 10,
              'text.usetex': True,
              'figure.figsize': [fig_width, fig_height],
              'font.family': 'serif'
              }

    matplotlib.rcParams.update(params)


def format_axes(ax):
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(spine_color)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=spine_color)

    return ax