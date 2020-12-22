from ase.build import molecule
from ase.visualize import view
from ase.build import bulk
import md

cu_cube = bulk('Cu', 'fcc', a=3.6, cubic=True)
cu_super = cu_cube*(5,5,5)
md.run_md(cu_super, str(0))
