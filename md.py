"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory
from ase.calculators.kim.kim import KIM
from asap3 import LennardJones
import ase.io

def calcenergy(a):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    t = ekin / (1.5 * units.kB)

    return epot, ekin, t
    

def run_md():
    # Use KIM for potentials from OpenKIM
    use_kim = True
    
    # Use Asap for a huge performance increase if it is installed
    use_asap = True
    
    # Set up a crystal
    atoms = ase.io.read("nacl.cif") # read from .cif file
    
    # Describe the interatomic interactions with OpenKIM potential
    if use_kim: # use KIM potential
        atoms.calc = KIM("LJ_ElliottAkerson_2015_Universal__MO_959249795837_003")
    else: # otherwise, default to asap3 LennardJones
        atoms.calc = LennardJones([18], [0.010323], [3.40], rCut = 6.625, modified = True)
        
    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, 40 * units.kB)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 1 * units.fs)  # 5 fs time step.
    traj = Trajectory('ar.traj', 'w', atoms)
    dyn.attach(traj.write, interval=100)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot, ekin, t = calcenergy(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, t, epot + ekin))

    # Now run the dynamics
    dyn.attach(printenergy, interval=10)
    printenergy()
    dyn.run(2000)
    
if __name__ == "__main__":
    run_md()
