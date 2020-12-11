#!/usr/bin/env python3
"""Demonstrates molecular dynamics with constant energy."""
from ase.lattice.cubic import FaceCenteredCubic
from asap3.md.velocitydistribution import MaxwellBoltzmannDistribution
#from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory
from ase.calculators.kim.kim import KIM
from asap3 import LennardJones
import ase.io
from read_settings import read_settings_file
import properties
import copy
import math


def run_md(atoms, id):
    """The function does Molecular Dyanamic simulation (MD) on a material, given by argument atoms.

    Parameters:
    atoms (obj): an atoms object defined by class in ase. This is the material which MD
    will run on.
    id (int): an identifying number for the material.

    Returns:
    obj:atoms object defined in ase, is returned.
    """

    # Read settings
    settings = read_settings_file()

    # Scale atoms object, cubic
    size = settings['supercell_size']
    atoms = atoms * size*(1,1,1)
    N = len(atoms.get_chemical_symbols())
    
    # Use KIM for potentials from OpenKIM
    use_kim = True

    # Use Asap for a huge performance increase if it is installed
    use_asap = True

    # Create a copy of the initial atoms object for future reference
    old_atoms = copy.deepcopy(atoms)

    # Describe the interatomic interactions with OpenKIM potential
    if use_kim: # use KIM potential
        atoms.calc = KIM("LJ_ElliottAkerson_2015_Universal__MO_959249795837_003")
    else: # otherwise, default to asap3 LennardJones
        atoms.calc = LennardJones([18], [0.010323], [3.40], rCut = 6.625, modified = True)

    # Set the momenta corresponding to temperature from settings file
    MaxwellBoltzmannDistribution(atoms, settings['temperature'] * units.kB)

    # Select integrator
    if settings['ensemble'] == "NVE":
        from ase.md.verlet import VelocityVerlet
        dyn = VelocityVerlet(atoms, settings['time_step'] * units.fs)

    elif settings['ensemble'] == "NVT":
        from ase.md.langevin import Langevin
        dyn = Langevin(atoms, settings['time_step'] * units.fs,
            settings['temperature'] * units.kB, settings['friction'])

    interval = settings['interval']

    traj = Trajectory('ar.traj', 'w', atoms)
    dyn.attach(traj.write, interval=interval)


    # Number of decimals for most calculated properties.
    decimals = settings['decimals']
    # Boolean indicating if the material is monoatomic.
    monoatomic = len(set(atoms.get_chemical_symbols())) == 1
    # Calculate nnd wherever possible

    # Calculation and writing of properties
    properties.initialize_properties_file(atoms, id, decimals,monoatomic)
    dyn.attach(properties.calc_properties, 100, old_atoms, atoms, id, decimals, monoatomic)

    # unnecessary, used for logging md runs
    # we should write some kind of logger for the MD
    def logger(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        epot = a.get_potential_energy() / len(a)
        ekin = a.get_kinetic_energy() / len(a)
        t = ekin / (1.5 * units.kB)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
              'Etot = %.3feV' % (epot, ekin, t, epot + ekin))

    # Running the dynamics
    dyn.attach(logger, interval=interval)
    #logger()
    #dyn.run(settings['max_steps'])
    # check for thermal equilibrium
    counter = 0
    equilibrium = False
    for i in range(round(settings['max_steps'] / settings['search_interval'])): # hyperparameter
        epot, ekin_pre, etot, t = properties.energies_and_temp(atoms)
        # kör steg som motsvarar säg 5 fs
        dyn.run(settings['search_interval']) # hyperparamter
        epot, ekin_post, etot, t = properties.energies_and_temp(atoms)
        print(abs(ekin_pre-ekin_post) / math.sqrt(N))
        print(counter)
        if (abs(ekin_pre-ekin_post) / math.sqrt(N)) < settings['tolerance']: 
            counter += 1
        else:
            counter = 0
        if counter > settings['threshold']: # hyperparameter
            print("reached equilibrium")
            equilibrium = True
            break

    if equilibrium:
        dyn.run(settings['max_steps'])
        properties.finalize_properties_file(atoms, id, decimals, monoatomic) 
    else:
        raise RuntimeError("MD did not find equilibrium")
    return atoms

if __name__ == "__main__":
    run_md()
