from ase.build import molecule
from ase.visualize import view
from ase.build import bulk
import md
from read_settings import read_settings_file
import numpy as np
import copy

# http://www-ferp.ucsd.edu/LIB/PROPS/PANOS/cu.html
# properties of copper
atoms_l = []
#atoms_l.append(bulk('Ar', 'fcc', a=5.26, cubic=True))
atoms_l.append(bulk('Cu', 'fcc', a=3.6, cubic=True))
#atoms = bulk('Ar', 'fcc', a=5.26, cubic=True)
#atoms = bulk('Cu', 'fcc', a=3.6, cubic=True)

settings = read_settings_file('acc_test_setting.json')

atoms_list = []
for atoms in atoms_l: 
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
    try:
        md.run_md(a, a.get_chemical_symbols()[0] + str(i), 'acc_test_setting.json')
    except Exception as e:
        print("Run broke: " + str(e))
