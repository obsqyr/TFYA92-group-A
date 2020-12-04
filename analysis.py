#!/usr/bin/env python3
from read_settings import read_settings_file
import os

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
