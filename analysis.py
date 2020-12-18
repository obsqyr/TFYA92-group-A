#!/usr/bin/env python3
from read_settings import read_settings_file
import os
from matplotlib import pyplot
import numpy as np
import math
import glob
import properties as pr

def find_eq_lc(fnames):

    """
    Parameters:
    fnames (list): A list of strings of file path/names

    Returns:
    tuple: returns a tuple of lattice constant, bulk modulus,
    filename and interpolated lattice constant.

    """
    print("Start")
    LC = 9999
    Etot = 9999
    N = ""
    E_list = []
    LC_list = []
    V_list = []
    for name in fnames:
        f = open(name, "r+")
        lines = f.read().split("\n")
        E = float(lines[-1].split()[2])
        l = float(lines[6].split()[7])
        E_list.append(E)
        LC_list.append(l)
        V_list.append(float(lines[6].split()[10]))

        if E < Etot:
            Etot = E
            LC = l
            N = name
        f.close()

    settings = read_settings_file()
    n = LC_list[0]**3 * settings['supercell_size']**3 / V_list[0]
    p = np.polyfit(LC_list, E_list, 2)
    if p[0] <= 0:
        print("Dynamically unstable in this range.")
        print(fnames)
        B = 0
        LC_interp = 0
    else:
        LC_interp = -p[1]/(2*p[0])
        E_interp = np.polyval(p, LC_interp)
        V_interp = LC_interp**3 * settings['supercell_size']**3 / n 
        q = np.polyfit(V_list, E_list,3)
        B = V_interp*(6*q[0]*V_interp + 2*q[1])*160.2 # conversion from ev/Å^3 to GigaPascal
        #print("E_list, LC_list, V_list, Etot, LC, N, LC_interp, E_interp, V_interp, B")
        #print(E_list, LC_list, V_list, Etot, LC, N, LC_interp, E_interp, V_interp, B,"\n")

    return LC, B, N, LC_interp

def sort_properties_files():
    """
    Paramters:
    None

    Returns:
    tuple: returns a tuple of lists of lattice constants, bulk moduli,
    interpolated lattice constants and file paths.
    """
    settings = read_settings_file()
    filenames = sorted(glob.glob("property_calculations/properties_*"))
    steps = 1 + 2*settings['LC_steps']
    LC_list = []
    BulkM_list = []
    N_list = []
    LCi_list = []

    for i in range(0,round(len(filenames)/steps)):
        LC, BulkM, N, LCi = find_eq_lc(filenames[steps*i:steps*(i+1)])
        LC_list.append(LC)
        BulkM_list.append(BulkM)
        N_list.append(N)
        LCi_list.append(LCi)
        """
        for fname in filenames[steps*i:steps*i+steps]:
            if fname != N:
                os.remove(fname)
        """
    return LC_list, LCi_list, BulkM_list, N_list

def extract():
    """
    Paramters:
    None

    Returns:
    None
    """
    file = open("property_calculations/collected_data.txt", "w+")
    settings = read_settings_file()
    d = settings['decimals']

    def lj(str, k = d):
        return " "+str.ljust(k+10)


    file.write(lj("Material")+lj("Cohesive energy")+lj("MSD")+lj("Self_diff")+lj("Specific heat"))

    if settings['vol_relax']:
        file.write(lj("Lattice constant")+lj("Interpolated LC")+lj("Bulk modulus"))

    file.write(lj("Debye",2)+lj("Lindemann"))
    file.write("\n")
    file.close()
    N_list = glob.glob("property_calculations/properties_*")
    if settings['vol_relax']:
        LC_list, LCi_list, BulkM_list, N_list = sort_properties_files()

    for i, filename in enumerate(sorted(N_list)):
        print(filename)
        f = open(filename, "r")
        lines = f.read().split("\n")
        f.close()
        if lines[-4] == 'Time averages:':
            mat = lines[2].split()[1]
            print(mat)
            Ecoh = lines[-1].split()[0]
            msd = lines[-1].split()[4]
            selfd = lines[-1].split()[5]
            Cv = lines[-1].split()[7]
            file = open("property_calculations/collected_data.txt", "a+")
            file.write(lj(mat)+lj(Ecoh)+lj(msd)+lj(selfd)+lj(Cv))
            if settings['vol_relax']:
                LC = LC_list[i]
                LCi = LCi_list[i]
                BulkM = BulkM_list[i]
                file.write(pr.ss(LC,d+4)+pr.ss(LCi,d+4)+pr.ss(BulkM,d+4))
            if len(lines[-1].split()) > 8:
                debye = lines[-1].split()[8]
                linde = lines[-1].split()[9]
            file.write("\n")
            file.close()
    return

def plot_properties():
    msd = []
    selfd = []
    spec_h = []
    latt_c = []
    inter_latt_c = []
    bulk_m = []
    coh_en = []
    debye = []
    linde = []

    f = open("property_calculations/collected_data.txt", "r")

    lines = f.readlines()[1:]
    for x in lines:
        coh_en.append(float(x.split()[1]))
        msd.append(float(x.split()[2]))
        selfd.append(float(x.split()[3]))
        spec_h.append(float(x.split()[4]))
        latt_c.append(float(x.split()[5]))
        inter_latt_c.append(float(x.split()[6]))
        bulk_m.append(float(x.split()[7]))
        if len(x.split()) > 8:
            debye.append(float(x.split()[8]))
            linde.append(float(x.split()[9]))

    f.close()
    #Plotting mean square displacment vs self diffusion const
    # in figure 1
    pyplot.figure(1)
    pyplot.scatter(msd,selfd)
    #Labeling the axes with names from properties.py
    pyplot.xlabel("Mean square displacement [Å^2]")
    pyplot.ylabel("Self diffusion [Å^2/fs]")

    pyplot.savefig("figures/MSD-SD.png")
    
    pyplot.figure(2)
    pyplot.scatter(latt_c,bulk_m)
    pyplot.xlabel("Lattice constant [Å]")
    pyplot.ylabel("Bulk modulus [GPa]")
    pyplot.savefig("figures/LC-BM.png")

    pyplot.figure(3)
    pyplot.scatter(latt_c, coh_en)
    pyplot.xlabel("Lattice constant [Å]")
    pyplot.ylabel("Cohesive energy [eV/atom]")
    pyplot.savefig("figures/LC-Ecoh.png")

    #pyplot.figure(3)
    #pyplot.scatter(latt_c, coh_en)
    #pyplot.xlabel("Lattice constant [Å]")
    #pyplot.ylabel("Cohesive energy [eV/atom]")
    #pyplot.savefig("figures/LC-Ecoh.png")
    
    pyplot.show()
                                
    return

if __name__ == "__main__":
    extract()
    plot_properties()
