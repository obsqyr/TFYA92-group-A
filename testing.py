import ase.io
import math as m
import numpy as np
from read_settings import read_settings_file
from md import run_md
from properties import initialize_properties_file
from properties import calc_properties
from ase.lattice.cubic import FaceCenteredCubic

NACL = ase.io.read("nacl.cif", None)

#x = NACL.get_atomic_numbers()
#print (x)
#print (len(x))

#y = NACL.get_positions()
#print (y[3])
#print (y)
#print (len(y))

# Testing msd
old_a = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol="Ar",
                          latticeconstant = 5.256,
                          size=(6, 6, 6),
                          pbc=True)

a = run_md()

#msqdisp = meansquaredisp(a, old_a)

#print(msqdisp)

initialize_properties_file(old_a)
calc_properties(a, old_a)
