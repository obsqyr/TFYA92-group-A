"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
#from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory
from asap3 import LennardJones
from read_settings import read_settings_file
import properties

def run_md():

    settings = read_settings_file()

    # Set up a crystal
    # Atomic structure should be read from some cif-file
    # Should this cif-file be an argument of run_md()? I.e. run_md("Atoms.cif")
    # atoms = ase.io.read("Atoms.cif", None)
    size = 6
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                                  symbol="Ar",
                                  latticeconstant = 5.256,
                                  size=(size, size, size),
                                  pbc=True)
    old_atoms = atoms

    # Method to calculate forces
    # Code to read in and implement correct LJ-parameters should be below
    # .....
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
    dyn.attach(traj.write, interval=1000)

    # Identity number (code?) to keep track of properties
    id = "0001"
    # Calculation and writing of properties
    properties.initialize_properties_file(atoms, id)
    dyn.attach(properties.calc_properties, 100, old_atoms, atoms, id)

    # Running the dynamics
    dyn.run(settings['max_steps'])

    return atoms

if __name__ == "__main__":
    run_md()
