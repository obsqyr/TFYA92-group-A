#!/usr/bin/env python3

import math
from ase import Atoms
from ase import units
import numpy as np
from read_settings import read_settings_file
import os
import chemparse

# This file contains functions to calculate material properties

def specific_heat(temp_store, N, atoms):
    """Calculates the specific heat for a material.
    Given by the formula: (E[T²] - E[T]²)/ E[T]² = 3*2^-1*N^-1*(1-3*N*Kb*2^-1*Cv^-1).
    Where Kb is boltzmansconstant, N is the total number of atoms, T is temperature and Cv the specific heat.
    E[A(t)] calculates the expectation value of A, which can in this case be seen as a time average for the
    phase variable A(t).

    Parameters:
    temp_store (list): The list over all intantaneous temperatures of a material once MD has been run.
    N (int): The total number of atoms in the material.

    Returns:
    float: specific heat is returned (J/(K*Kg))
    """
    if len(temp_store) == 0:
        raise ValueError("temp_store is empty, invalid value.")
    steps = len(temp_store)
    z = sum(atoms.get_masses()) * units._amu # total mass: atomic units to kg
    # Set M = (E[T²] - E[T]²)/ E[T]²
    ET = sum(temp_store)/steps
    ET2 = sum(np.array(temp_store)**2)/steps
    M = (ET2 - ET**2)/ET**2
    settings = read_settings_file()
    N = N / settings['supercell_size']**3
    #print("M:", M)
    #print("N:", N)
    #print("T:", temp_store)
    #print(sum(np.array(temp_store)**2))
    #print("ET:", ET)
    #print("ET2:", ET2)
    #Cv1 = -9*N*units.kB/(4*N*M-6)/z*units._e * settings['supercell_size']**3 # specific heat J/(K*Kg)
    Cv2 = ((9*ET**2*N*units._k) / (ET**2 * (6+4*N) - 4*N*ET2)) / z * settings['supercell_size']**3
    #print("Cv1:", Cv1)
    #print("Cv2:", Cv2)
    return Cv2

def distance2(pos1, pos2):
    """Calculates the sqared distance between two atomsx in 3D space"""
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2

def distance(pos1, pos2):
    return math.sqrt(distance2(pos1, pos2))


def meansquaredisp(atoms, old_atoms):
    """ Calculates the mean squared displacement

    Parameters:
    atoms (obj):atoms is an atom object from ase.
    old_atoms (obj):old_atoms is an atom object from the python library.

    Returns:
    float: The mean squared displacement.

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
            and temperature.

    """
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    t = ekin / (1.5 * units.kB)

    return epot, ekin, etot, t


def lattice_constants(a):
    """ Calculates the lattice constant of a materialself.

    Parameters:
    a (obj): a is an atoms object of class defined in ase.

    Returns:
    list: returns the lattice_constants, in the 3 dimensions.
    """

    s = read_settings_file()['supercell_size']
    lc = list(a.get_cell_lengths_and_angles())
    return [lc[0]/s, lc[1]/s, lc[2]/s]

def volume_pressure(a):
    """Calculates volume and pressure of a material.

    Parameters:
    a (obj): a is an atoms object of class defined in ase.

    Returns:
    tuple:returns a tuple of volume and pressure.
    """
    N = len(a.get_chemical_symbols())
    vol = a.get_volume()/N
    stress = a.get_stress()
    pressure = (stress[0] + stress[1] + stress[2])/3 * units._e * units.m**3 * 10**(-9)  # eV/Å^3 to GPa
    return vol, pressure

def debye_lindemann(a, msd, temp):
    """Calculates the debye temperature and the Lindemann
       criterion. Original cell is assumed to be sc, bcc or fcc.
       Lattice constants in a,b and c may be different.
    Parameters:
    a (obj): a is an atoms object of class defined in ase.
    msd (float): mean square displacment
    temp (float): temperature

    Returns
    list: list of debye temperature and lindemann criterion.
    """
    s = read_settings_file()
    debye = math.sqrt(9 * units._hbar**2 * temp / (units._k * a.get_masses()[0] * units._amu * msd) * units.m**2)
    z = s['supercell_size']
    n = len(a) / z**3
    lc = a.get_cell_lengths_and_angles()[0:3]
    if n == 1:
        nnd = min(lc)
    elif n == 2:
        nnd = 1/2 * math.sqrt(lc[0]**2 + lc[1]**2 + lc[2]**2)
    elif n == 4:
        if np.max(lc) != np.min(lc): # all values in lc are not the same
            lc = np.delete(lc, np.argwhere(lc==max(lc)))
        nnd = 1/2 * math.sqrt(lc[0]**2 + lc[1]**2)
    else:
        nnd = 9999
    lindemann = math.sqrt(msd)/nnd
    return debye, lindemann

def self_diff(a, msd, time):
    """Calculates the self diffusion coefficient of a material.

    Paramters:
    a (obj): a is an atoms object of class defined in ase.
    msd (float): mean squre displacement.
    time (float): time step.

    Returns:
    float: self diffusion coefficient.
    """
    if time == 0:
        sd = "_"
    else:
        sd = msd/(6*time)
    return sd * 10 # units: mm^2 / s


def initialize_properties_file(a, ai, id, d, ma):
    """Initializes a file over properties with correct titles and main structure
        for an material.

    Parameters:
    a (obj): a is an atoms object of class defined in ase. The material is made
            into an atoms object.
    ai (obj): initial atoms object an object of class sdefined in ase. The unit cell
                atoms object that md runs for.
    id (str): a special number identifying the material system.
    d (int): a number for the formatting of file. Give a correct spacing
            for printing to file.
    ma (boolean): a boolean indicating if the material is monoatomic

    Returns:
    None
    """
    # Help function for formating
    def lj(str, k = d):
        return " "+str.ljust(k + 6)
    file = open("property_calculations/properties_" + id + ".txt", "w+")

    file.write("Material ID: " + id + "\n")
    file.write("Unit cell composition: " + a.get_chemical_formula() + "\n")
    chem_formula = a.get_chemical_formula(mode='hill', empirical=True)
    file.write("Material:  "+ chem_formula + "\n")

    # Write the elements as title
    file.write("Site positions of initial unit cell:" + "\n")
    dict = chemparse.parse_formula(ai.get_chemical_formula())
    els = list(dict.keys())
    prop_num = list(dict.values())
    tmp_ls = [(a + " ") * int(b) for a,b in zip(els, prop_num)] # Get ["Al", "Mg Mg Mg"] for "AlMg3" e.g.
    els_str = "".join(tmp_ls)
    els_ls = els_str.split()  # give you ["Al", "Mg", "Mg", "Mg"] e.g.
    for a in els_ls:
        file.write(lj(a))

    # Write the site positions
    res_array = ai.get_positions()
    for i in range(0, 3): # 3 components
        file.write("\n")
        for ii in range(0, len(res_array)):
            format_str = "." + str(d) + "f"
            val  = format(res_array[:,i][ii], format_str) # d decimals
            file.write(lj(val))

    file.write("\n")
    file.write("Properties:\n")
    file.write(lj("Time")+lj("Epot")+lj("Ekin")+lj("Etot")+lj("Temp",2)+lj("MSD"))
    file.write(lj("Self_diff")+lj("LC_a",3)+lj("LC_b",3)+lj("LC_c",3))
    file.write(lj("Volume")+lj("Pressure"))
    if ma:
        file.write(lj("DebyeT",2)+lj("Lindemann"))
    file.write("\n")
    file.write(lj("fs")+lj("eV/atom")+lj("eV/atom")+lj("eV/atom")+lj("K",2)+lj("Å^2"))
    file.write(lj("mm^2/s")+lj("Å",3)+lj("Å",3)+lj("Å",3))
    file.write(lj("Å^3/atom")+lj("GPa"))
    if ma:
        file.write(lj("K",2)+lj("1"))
    file.write("\n")
    file.close()
    return

def ss(value, decimals):
    """Help function to calc_properties."""
    if isinstance(value,str):
        tmp = value
    else:
        tmp = str(round(value, decimals))
    return " "+tmp.ljust(decimals + 6)


def calc_properties(a_old, a, id, d, ma):
    """Calculates prioperties and writes them in a file.

    Parameters:
    a_old (obj): a_old is an atoms object from clas defined from ase.
                it's the old atom that needs to be updated.
    a (obj): a is an atoms object from clas defined from ase.
            it's the new updated atom obj for MD molecular dyanimcs.
    id (str):
    d (int):
    ma (boolean):
    Returns: None

    """
    f=open("property_calculations/properties_"+id+".txt", "r")

    epot, ekin, etot, temp = energies_and_temp(a)
    msd =  meansquaredisp(a, a_old)
    settings = read_settings_file()
    ln = sum(1 for line in f)
    time = settings['time_step']*settings['interval']*(ln-6)
    selfd = self_diff(a, msd, time)
    lc = lattice_constants(a)
    vol, pr = volume_pressure(a)
    f.close()

    file=open("property_calculations/properties_"+id+".txt", "a+")
    file.write(ss(time, d)+ss(epot, d)+ss(ekin, d)+ss(etot, d)+ss(temp, 2)+ss(msd, d))
    file.write(ss(selfd, d)+ss(lc[0], 3)+ss(lc[1], 3)+ss(lc[2], 3))
    file.write(ss(vol, 3)+ss(pr, d))
    if ma:
        debye, linde = debye_lindemann(a,msd,temp)
        file.write(ss(debye, 2)+ss(linde, d))

    file.write("\n")
    file.close()
    return

def finalize_properties_file(a, id, d, ma):
    """ Calculates and records the properties of a material.

    Parameters:
    a (obj): Atoms object form ase.
    id (str): a special number identifying the material system.
    d (int): a number for the formatting of file. Give a correct appending
            for strings.
    ma (boolean): ma is a boolean, for True the system is monoatomic.

    Returns: None

    """
    epot = []
    ekin = []
    etot = []
    temp = []
    msd = []
    selfd = []
    pr = []
    debye = []
    linde = []

    settings = read_settings_file()
    f=open("property_calculations/properties_"+id+".txt", "r")
    f_lines = f.readlines()
    steps = math.floor(settings['max_steps'] / settings['interval'])
    for line in f_lines[-steps:]:
        epot.append(float(line.split()[1]))
        ekin.append(float(line.split()[2]))
        etot.append(float(line.split()[3]))
        temp.append(float(line.split()[4]))
        msd.append(float(line.split()[5]))
        selfd.append(line.split()[6])
        pr.append(float(line.split()[11]))
        if ma:
            debye.append(float(line.split()[12]))
            linde.append(float(line.split()[13]))
    f.close()

    epot_t = sum(epot)/steps
    ekin_t = sum(ekin)/steps
    etot_t = sum(etot)/steps
    temp_t = sum(temp)/steps
    msd_t = sum(msd)/steps
    selfd_t = sum(float(i) for i in selfd[1:])/(steps-1)
    pr_t = sum(pr)/steps
    debye_t = sum(debye)/steps
    linde_t = sum(linde)/steps
    Cv = specific_heat(temp, len(a.get_chemical_symbols()), a)

    file=open("property_calculations/properties_"+id+".txt", "a+")
    file.write("\nTime averages:\n")

    # Help function for formating
    def lj(str, k = d):
        return " "+str.ljust(k+6)

    file.write(lj(" ")+lj("Epot")+lj("Ekin")+lj("Etot")+lj("Temp",2)+lj("MSD"))
    file.write(lj("Self_diff")+lj("Pressure"))
    file.write(lj("Spec_heat"))
    if ma:
        file.write(lj("DebyeT",2)+lj("Lindemann"))

    file.write("\n")

    file.write(lj(" ")+lj("eV/atom")+lj("eV/atom")+lj("eV/atom")+lj("K",2)+lj("Å^2"))
    file.write(lj("mm^2/s")+lj("GPa"))
    file.write(lj("J/(K*Kg)"))

    if ma:
        file.write(lj("K",2)+lj("1"))
    file.write("\n")

    file.write(lj(" ")+ss(epot_t, d)+ss(ekin_t, d)+ss(etot_t, d)+ss(temp_t, 2)+ss(msd_t, d))
    file.write(ss(selfd_t, d)+ss(pr_t, d))
    file.write(ss(Cv, d))
    if ma:
        file.write(ss(debye_t, 2)+ss(linde_t, d))
    file.close()
    return

def delete_properties_file(id):
    """ Deletes a property file by its id

    Parameters:
    id (): a special number identifying the material system, as an int.

    Returns: None

    """
    os.remove("property_calculations/properties_"+str(id)+".txt")
    return

def clean_property_calculations():
    """ Idea: delete all propeties files without 'Time averages:'
    in them.
    """
    print(" -- Cleaning property_calculations directory -- ")
    counter = 0
    for filename in os.listdir("property_calculations"):
        f = open("property_calculations/"+ str(filename), "r")
        if "Time averages:" not in f.read():
            counter += 1
            os.remove("property_calculations/"+str(filename))

    print(" -- Removed " + str(counter) + " properties files -- ")

if __name__ == "__main__":
    clean_property_calculations()
