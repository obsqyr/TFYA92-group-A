from ase.lattice.cubic import FaceCenteredCubic
from ase.calculators.kim.kim import KIM

atoms = FaceCenteredCubic(symbol='Ar', latticeconstant=5.25, size=(1,1,1))
calc = KIM('LJ_ElliottAkerson_2015_Universal__MO_959249795837_003')
atoms.calc = calc

energy = atoms.get_potential_energy()
print('Potential energy: {} eV'.format(energy))