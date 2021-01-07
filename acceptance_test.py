from ase.build import molecule
from ase.visualize import view
from ase.build import bulk
import md
from read_settings import read_settings_file
import numpy as np
import copy

# http://www-ferp.ucsd.edu/LIB/PROPS/PANOS/cu.html
# properties of copper
atoms = bulk('Ar', 'fcc', a=5.26, cubic=True)
#ar_cube = bulk('Cu', 'fcc', a=3.6, cubic=True)

settings = read_settings_file('acc_test_setting.json')

atoms_list = []
if settings['vol_relax']:
    cell = np.array(atoms.get_cell())
    P = settings['LC_steps']
    for i in range(-P,1+P):
        atoms_v = copy.deepcopy(atoms)
        atoms_v.set_cell(cell*(1+i*settings['LC_mod']))
        atoms_list.append(atoms_v)
else:
    atoms_list.append(atoms)

print(atoms_list)

for i, a in enumerate(atoms_list):
    md.run_md(a, 'ar' + str(i), 'acc_test_setting.json')
