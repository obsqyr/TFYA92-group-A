from ase.build import molecule
from ase.visualize import view
from ase.build import bulk
import md

cu_cube = bulk('Cu', 'fcc', a=3.6, cubic=True)
md.run_md(cu_cube, str(0))
