#! /usr/bin/env python

import friction_tools as ft
import math
import numpy as np

simu = ft.FrictionSimulation()

simu.create_slab(element='Ag',xy_cells=4,z_cells=4,bottom_z=0.0)
simu.create_interaction(['Ag','Ag'], 1.0, 1.781)

# define the center and radius of a sphere
lattice_constant = 10.0 / 4.0
center = np.array([1.5, 1.5, 1.5])*lattice_constant
radius = 2*lattice_constant

# take a picture of the system
simu.take_snapshot(filename='initial.png')
simu.write_xyzfile(filename='initial.xyz')

# check all the atoms and remove those that are not
# inside the sphere we just defined.
# note that the loop goes over the atoms backwards
# because we delete atoms as we go, which affects
# the end of the list of atoms but not the beginning
for atom in reversed(simu.system):
    xyz = atom.position
    separation = xyz - center

    # calculate the distance between the atom and the
    # center of the sphere
    distance = math.sqrt(np.dot(separation, separation))
    if distance > radius:
        del simu.system[atom.index]

# take a picture of the system
simu.take_snapshot(filename='final.png')
simu.write_xyzfile(filename='final.xyz')