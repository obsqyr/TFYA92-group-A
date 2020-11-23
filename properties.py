import math
from ase import Atoms
from ase import units
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
        raise TypeError("Number of atoms doesnt match.")
        sys.exit('ERROR')

    msd = 0.0
    for atom in range(length):
        msd += distance2(pos[atom], old_pos[atom])

    return msd/length

def energies_and_temp(a):
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    t = ekin / (1.5 * units.kB)

    return epot, ekin, etot, t

def lattice_constants(a):
    # NOTE: Not lattice constats yet, just cell lengths.    ?????
    lc = list(a.get_cell_lengths_and_angles())
    return [lc[0], lc[1], lc[2]]

# Calculate internal pressure




# Initializes the "properties_id.txt" file
def initialize_properties_file(a, id, d):
    file=open("properties_"+id+".txt", "w+")
    file.write("Material ID: "+id+"\n")
    file.write("Unit cell composition: "+a.get_chemical_formula() + "\n")
    file.write("Material: "+a.get_chemical_formula(mode='hill', empirical=True) + "\n")
    file.write("Properties:\n")

    # Help function for formating
    def lj(str, k = d):
        return str.ljust(k+6)

    file.write(lj("Epot")+lj("Ekin")+lj("Etot")+lj("Temp",2)+lj("MSD"))
    file.write(lj("LC_a",3)+lj("LC_b",3)+lj("LC_c",3)+"\n")
    file.write(lj("eV/atom")+lj("eV/atom")+lj("eV/atom")+lj("K",2)+lj("Å^2"))
    file.write(lj("Å",3)+lj("Å",3)+lj("Å",3)+"\n")
    file.close()
    return

# Help function to calc_properties
def ss(value, decimals):
    tmp = str(round(value, decimals))
    return tmp.ljust(decimals + 6)

# Calculates prioperties and writes them in a file
def calc_properties(a_old, a, id, d):
    # d = number of decimals
    epot, ekin, etot, temp = energies_and_temp(a)
    msd =  meansquaredisp(a, a_old)
    lc = lattice_constants(a)
    file=open("properties_"+id+".txt", "a+")
    file.write(ss(epot, d)+ss(ekin, d)+ss(etot, d)+ss(temp, 2)+ss(msd, d))
    file.write(ss(lc[0], 3)+ss(lc[1], 3)+ss(lc[2], 3))

    file.write("\n")
    file.close()
    return
