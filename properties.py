#!/usr/bin/env python3

import math
from ase import Atoms
from ase import units
import numpy as np
# This file contains functions to calculate material properties

def specific_heat(temp_store, steps, N):
    """Calculates the specific heat for a material.
    Given by the formula: (E[T²] - E[T]²)/ E[T]² = 3*2^-1*N^-1*(1-3*N*Kb*2^-1*Cv^-1).
    Where Kb is boltzmansconstant, N is the total number of atoms, T is temperature and Cv the specific heat.
    E[A(t)] calculates the expectation value of A, which can in this case be seen as a time average for the
    phase variable A(t).

    Parameters:
    temp_store (list): The list over all intantaneous temperatures of a material once MD has been run.
    steps (int): The total number of sampled steps from 0 that the MD has run.
    N (int): The total number of atoms in the material.

    Returns:
    int: specific heat is returned (the SI-units J*Kg^-1*K^-1)
    """

    # Set M = (E[T²] - E[T]²)/ E[T]²
    ET = sum(temp_store)/steps
    ET2 = sum(np.array(temp_store)**2/steps
    M = (ET2 - ET**2)/ET**2
    Cv = -9*N*units.kB/(4*N*M-6)
    return Cv

def distance2(pos1, pos2):
    """Calculates the sqared distance between two atoms in 3D space"""
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2

def distance(pos1, pos2):
    return math.sqrt(distance2(pos1, pos2))


def meansquaredisp(atoms, old_atoms):
    """ Calculates the mean squared displacement

    Parameters:
    atoms (obj):atoms is an atom object from ase.
    old_atoms (obj):old_atoms is an atom object from the python library.

    Returns:
    int: The mean squared displacement.

   """
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
    """ Calculates the energies and temperature.

    Parameters:
    a (obj): a is an atoms object of class defined in ase.

    Returns:
    tuple: returns a tuple of potential energi, kinetic energy, total energy
            and time step t.

    """
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    t = ekin / (1.5 * units.kB)

    return epot, ekin, etot, t


def lattice_constants(a):
    # NOTE: Not lattice constats yet, just cell lengths.    ?????
    lc = list(a.get_cell_lengths_and_angles())
    return [lc[0], lc[1], lc[2]]

def volume_pressure(a):
    N = len(a.get_chemical_symbols())
    vol = a.get_volume()/N
    stress = a.get_stress()
    pressure = (stress[0] + stress[1] + stress[2])/3
    return vol, pressure

def debye_lindemann(a,msd,temp,nnd):
    debye = math.sqrt(3 * units._hbar**2 * temp / (units.kb * a.get_masses()[0] * msd))
    lindemann = math.sqrt(msd)/nnd
    return debye, lindemann
# Calculate internal pressure

def initialize_properties_file(a, id, d, ma):
    """Initializes a file over properties with correct titles and main structure
        for an material.

    Parameters:
    a (obj): a is an atoms object of class defined in ase. The material is made
            into an atoms object.
    id (int): a special number identifying the material system.
    d (int): a number for the formatting of file. Give a correct appending
            for strings.
    ma (bool): a boolean indicating if the material is monoatomic

    Returns:
    None
    """
    file=open("property_calculations/properties_"+id+".txt", "w+")

    file.write("Material ID: "+id+"\n")
    file.write("Unit cell composition: "+a.get_chemical_formula() + "\n")
    file.write("Material: "+a.get_chemical_formula(mode='hill', empirical=True) + "\n")
    file.write("Properties:\n")

    # Help function for formating
    def lj(str, k = d):
        return str.ljust(k+6)

    file.write(lj("Epot")+lj("Ekin")+lj("Etot")+lj("Temp",2)+lj("MSD"))
    file.write(lj("LC_a",3)+lj("LC_b",3)+lj("LC_c",3))
    file.write(lj("Volume")+lj("Pressure"))
    if ma:
        file.write(lj("DebyeT",2)+lj("Lindemann"))

    file.write("\n")
    file.write(lj("eV/atom")+lj("eV/atom")+lj("eV/atom")+lj("K",2)+lj("Å^2"))
    file.write(lj("Å",3)+lj("Å",3)+lj("Å",3))
    file.write(lj("Å^3/atom")+lj("Pa"))
    # Check if pressure is given in Pascal!!!
    if ma:
        file.write(lj("K",2)+lj("1"))
    file.write("\n")
    file.close()
    return

def ss(value, decimals):
    """Help function to calc_properties."""
    tmp = str(round(value, decimals))
    return tmp.ljust(decimals + 6)


def calc_properties(a_old, a, id, d, ma, nnd=1):
    """Calculates prioperties and writes them in a file.

    Parameters:
    a_old (obj): a_old is an atoms object from clas defined from ase.
                it's the old atom that needs to be updated.
    a (obj): a is an atoms object from clas defined from ase.
            it's the new updated atom obj for MD molecular dyanimcs.
    id ():
    d ():
    ma ():
    nnd (float): nnd is the nearest neighbour distance for an ideal crystal lattice.
    Returns: None

    """

    epot, ekin, etot, temp = energies_and_temp(a)
    msd =  meansquaredisp(a, a_old)
    lc = lattice_constants(a)
    vol, pr = volume_pressure(a)

    file=open("property_calculations/properties_"+id+".txt", "a+")
    file.write(ss(epot, d)+ss(ekin, d)+ss(etot, d)+ss(temp, 2)+ss(msd, d))
    file.write(ss(lc[0], 3)+ss(lc[1], 3)+ss(lc[2], 3))
    file.write(ss(vol, 3)+ss(pr, 3))
    if ma:
        debye, linde = debye_lindemann(a,msd,temp,nnd)
        file.write(ss(debye, 2)+ss(linde, d))

    file.write("\n")
    file.close()
    return

def finalize_properties_file(a, id, d, ma):

    epot = []
    ekin = []
    etot = []
    temp = []
    msd = []
    pr =[]
    debye = []
    linde = []
    file=open("property_calculations/properties_"+id+".txt", "a+")
    steps = 0
    for i, line in enumerate(file):
        if i >= 6:
            epot.append(line.split(" ")[0])
            ekin.append(line.split(" ")[1])
            etot.append(line.split(" ")[2])
            temp.append(line.split(" ")[3])
            msd.append(line.split(" ")[4])
            pr.append(line.split(" ")[5])
            debye.append(line.split(" ")[6])
            linde.append(line.split(" ")[7])

            steps += 1
    epot_t = sum(epot)/steps
    ekin_t = sum(ekin)/steps
    etot_t = sum(etot)/steps
    temp_t = sum(temp)/steps
    msd_t = sum(msd)/steps
    pr_t = sum(pr)/steps
    debye_t = sum(debye)/steps
    linde_t = sum(linde)/steps
    Cv = specific_heat(temp, steps, len(a.get_chemical_symbols())
    file.write("\nTime averages:\n")

    # Help function for formating
    def lj(str, k = d):
        return str.ljust(k+6)

    file.write(lj("Epot")+lj("Ekin")+lj("Etot")+lj("Temp",2)+lj("MSD"))
    file.write(lj("Pressure"))
    if ma:
        file.write(lj("DebyeT",2)+lj("Lindemann"))
    file.write(lj("Specific heat"))
    file.write("\n")

    file.write(lj("eV/atom")+lj("eV/atom")+lj("eV/atom")+lj("K",2)+lj("Å^2"))
    file.write(lj(lj("Pa"))
    # Check if pressure is given in Pascal!!!
    if ma:
        file.write(lj("K",2)+lj("1"))
    file.write(lj("CONTROL"))
    file.write("\n")

    file.write(ss(epot, d)+ss(ekin, d)+ss(etot, d)+ss(temp, 2)+ss(msd, d))
    file.write(ss(pr, 3))
    if ma:
        file.write(ss(debye_t, 2)+ss(linde_t, d))
    file.write(ss(Cv, d))
    file.close()
    return
