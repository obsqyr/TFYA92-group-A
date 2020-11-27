import ase.io
import math as m
import numpy as np
import ase.atoms
from read_settings import read_settings_file
from md import run_md
from properties import initialize_properties_file
from properties import calc_properties
import properties
from ase.lattice.cubic import FaceCenteredCubic

NACL = ase.io.read("nacl.cif", None)

#x = NACL.get_atomic_numbers()
#print (x)
#print (len(x))

#y = NACL.get_positions()
#print (y[3])
#print (y)
#print (len(y))


old_a = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol="Ar",
                          latticeconstant = 5.256,
                          size=(1, 1, 1),
                          pbc=True)

a = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          symbol="Ar",
                          latticeconstant = 5.256,
                          size=(1, 1, 1),
                          pbc=True)

a.set_positions([[0, 0, 10], [2.628, 2.628, 0], [2.628, 0, 2.628], [0, 2.628, 2.628]])


#a = run_md()

#msqdisp = properties.meansquaredisp(a, old_a)

#print(msqdisp)

atoms_old = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                            symbol="Ar",
                            latticeconstant = 5.256,
                            size=(3, 3, 3),
                            pbc=True)

#final_atoms = run_md()

#print(properties.meansquaredisp(atoms_old, final_atoms))

print(properties.ss(3.141529887453, 3))

print(NACL.info['spacegroup'])

print(len(set(NACL.get_chemical_symbols())))
