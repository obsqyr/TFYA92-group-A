"""Demonstrates molecular dynamics with constant energy."""
#/home/linle336/anaconda3/lib/python3.8/site-packages/ase/io/formats.py

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
#from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory
from ase.calculators.kim.kim import KIM
from read_settings import read_settings_file


def calcenergy(a):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    t = ekin / (1.5 * units.kB)

    return epot, ekin, t


def run_md(atoms):

    # Use KIM for potentials from OpenKIM
    use_kim = True
    # Use settings files
    settings = read_settings_file()

#--------Provisional?--------

    # Use Asap for a huge performance increase if it is installed
    use_asap = True

    if use_asap:
        from asap3 import LennardJones
        size = 6
    else:
        from ase.calculators.lj import LennardJones
        size = 3
#----------------------------
    # Set up a crystal
    # Atomic structure should be read from some cif-file
    # Should this cif-file be an argument of run_md()? I.e. run_md("Atoms.cif")
    # atoms = ase.io.read("Atoms.cif", None)

#    print("TESTING WILLIAM...")
#    atoms = ase.io.read("nacl.cif", None)

#    mp_properties = read_mp_properties('testing_data_materials.json')
#    txt_str = mp_properties["cif"][0]
#    f = open("tmp_cif.cif", "w+")
#    f.write(txt_str)
#    f.close()

#    atoms = ase.io.read("tmp_cif.cif", None)

    print(atoms.get_chemical_formula())
#    print("################TTTTIIIS IS A TEST ")

    #atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    #                              symbol="Ar",
    #                              latticeconstant = 5.256,
    #                              size=(size, size, size),
    #                              pbc=True)



    # Describe the interatomic interactions with Lennard Jones
    if use_kim: # use KIM potentialß
        atoms.calc = KIM("LJ_ElliottAkerson_2015_Universal__MO_959249795837_003") #an example potential
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
