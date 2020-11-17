import math
from ase import atoms

# This file contains functions to calculate material properties

def distance2(pos1, pos2):
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2

def distance(pos1, pos2):
    return math.sqrt(distance2(pos1, pos2))


def meansquaredisp(atoms, old_atoms):
    pos = atoms.get_positions()
    old_pos = old_atoms.get_positions()
    length = len(pos)

    if length != len(old_pos):
        raise TypeError("Numbers of atoms doesnt match.")
        sys.exit('ERROR')

    msd = 0.0000

    for atom in range(length):
        msd =+ distance2(pos[atom], old_pos[atom])

    return msd/length

def energies_and_temp(a):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    t = ekin / (1.5 * units.kB)

    return epot, ekin, etot, t

def initialize_properties_file(a):
    file = open("properties.txt", "a+")
    file.write("Unit cell composition: "+a.get_chemical_formula() + "\n")
    file.write("Material: "+a.get_chemical_formula(mode='hill', empirical=True) + "\n")
    file.write("Properties:\nepot ekin etot temp msd \n")
    epot, ekin, etot, temp = energies_and_temp(a)

    file.write(str(epot)+" "+str(ekin)+" "+str(etot)+" "+str(temp)+" 0")

    return

def calc_properties(a, a_old):
    epot, ekin, etot, temp = energies_and_temp(a)
    msd = meansquaredisp(a, a_old)

    file = open("properties.txt", "a")
    file.write(str(epot)+" "+str(ekin)+" "+str(etot)+" "+str(temp)+" "+str(msd)+"\n")

    return
