from ase.build import molecule
from ase.visualize import view
from ase.build import bulk
import md

ar_cube = bulk('Ar', 'fcc', a=5.26, cubic=True)
md.run_md(ar_cube, 'ar')
