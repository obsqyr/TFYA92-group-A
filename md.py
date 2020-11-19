"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
#from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory
from ase.calculators.kim.kim import KIM
from asap3 import LennardJones
import ase.io
from read_settings import read_settings_file

def calcenergy(a):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    t = ekin / (1.5 * units.kB)

    return epot, ekin, t


def run_md():
    # Read settings
    settings = read_settings_file()
    
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
    MaxwellBoltzmannDistribution(atoms, settings['temperature'] * units.kB)

    # Select integrator
    if settings['ensemble'] == "NVE":
        from ase.md.verlet import VelocityVerlet
        dyn = VelocityVerlet(atoms, settings['time_step'] * units.fs)

    elif settings['ensemble'] == "NVT":
        from ase.md.langevin import Langevin
        dyn = Langevin(atoms, settings['time_step'] * units.fs,
            settings['temperature'] * units.kB, settings['friction'])

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
    dyn.run(settings['max_steps'])

if __name__ == "__main__":
    run_md()
