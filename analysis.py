#!/usr/bin/env python3
from read_settings import read_settings_file
import os

def find_equilibrium(fnames):

    """
    Parameters:
    fnames (list): A list of strings of file names

    Returns: None

    """
    LC = 9999
    Etot = 9999
    N = ""
    E_list = []
    V_list = []
    for name in fnames:
        f = open("property_calculations/"+name, "r+")
        lines = f.read().split("\n")
        E = lines[-1].split()[2]
        E_list.append(E)
        V_list.append(lines[6].split()[10])
        if E < Etot:
            Etot = E
            LC = lines[6].split()[7]
            N = name

        #Bulk mod = V * d^2E/dV^2, evaluated at equilibrium volume.

        f.close()


    return

def sort(arg):
    setting = read_settings_file()
    filenames = os.listdir("property_calculations/")
    steps = settings['LC_steps']
    LC_list = []
    BulkM_list = []
    N_list = []

    for i in len(filenames)/steps:
        LC, BulkM, N = find_equilibrium(filenames[steps*i:steps*i+steps])
        LC_list.append(LC)
        BulkM_list.append(BulkM)
        N_list.append(N)

        for fname in filenames[steps*i:steps*i+steps]:
            if fname != N
                os.remove("property_calculations/"+fname)
    return

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
