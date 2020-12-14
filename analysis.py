#!/usr/bin/env python3
from read_settings import read_settings_file
import os
import numpy as np
import math

def find_equilibrium(fnames):

    """
    Parameters:
    fnames (list): A list of strings of file names

    Returns: None

    """
    print("Start")
    LC = 9999
    Etot = 9999
    N = ""
    E_list = []
    LC_list = []
    V_list = []
    for name in fnames:
        f = open("property_calculations/"+name, "r+")
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

    p = np.polyfit(LC_list, E_list, 2)
    if p[0] =< 0:
        print("Dynamically unstable in this range.")
        print(fnames)
        break
    else:
        LC_interp = -p[1]/(2*p[0])
        E_interp = np.polyval(p, LC_interp)
        V_interp = LC_interp**3
        q = np.polyfit(V_list, E_list,3)
        B = V_interp*(6*q[0]*V_interp + 2*q[1])

    print("E_list, LC_list, V_list, Etot, LC, N, LC_interp, E_interp, V_interp")
    print(E_list, LC_list, V_list, Etot, LC, N, LC_interp, E_interp, V_interp + "\n")

    return LC, B, N, LC_interp

def sort():
    setting = read_settings_file()
    filenames = os.listdir("property_calculations/")
    steps = 1 + 2*settings['LC_steps']
    LC_list = []
    BulkM_list = []
    N_list = []
    LCi_list = []

    for i in len(filenames)/steps:
        LC, BulkM, N, LCi = find_equilibrium(filenames[steps*i:steps*(i+1)])
        LC_list.append(LC)
        BulkM_list.append(BulkM)
        N_list.append(N)
        LCi_list.append(LCi)
        for fname in filenames[steps*i:steps*i+steps]:
            if fname != N:
                os.remove("property_calculations/"+fname)
    return LC_list, LCi_list, BulkM_list

def extract():
    file = open("property_calculations/collected_data", "w+")
    setting = read_settings_file()
    d = setting['decimals']

    def lj(str, k = d):
        return str.ljust(k+10)

    file.write(lj("Material")+lj("MSD")+lj("Self_diff")+lj("Specific heat")+lj("Lattice constant"))
    file.write(lj("Bulk modulus")+lj("Cohesive energy")+lj("Debye",2)+lj("Lindemann")+"\n")


    for filename in os.listdir("property_calculations/"):
        if filename.startswith("properties_") and filename.endswith(".txt"):
            print("property_calculations/"+filename)
            f = open("property_calculations/"+filename, "r")
            #print(f.read().split("\n")[-1])
            lines = f.read().split("\n")
            mat = lines[2].split()[1]
            print(mat)
            #lastline = f.read().split("\n")[-1]
            msd = lines[-1].split()[4]
            selfd = lines[-1].split()[5]
            Cv = lines[-1].split()[7]
            file.write(lj(mat)+lj(msd)+lj(selfd)+lj(Cv))
            f.close()
    file.close()
    return

if __name__ == "__main__":
    extract()
