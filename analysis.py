#!/usr/bin/env python3
from read_settings import read_settings_file
import os
from matplotlib import pyplot

def extract():
    file = open("property_calculations/collected_data", "w+")
    setting = read_settings_file()
    d = setting['decimals']

    def lj(str, k = d):
        return str.ljust(k+10)

    file.write(lj("Material")+lj("MSD")+lj("Self_diff")+lj("Spec_heat")+lj("Lattice_C"))
    file.write(lj("Bulk_mod")+lj("Coh_Energy")+lj("Debye",2)+lj("Lindemann")+"\n")

    for filename in os.listdir("property_calculations/"):

        if filename.startswith("properties_") and filename.endswith(".txt"):
            print("property_calculations/"+filename)
            f = open("property_calculations/"+filename, "r")
            lines = f.read().split("\n")

            if lines[-4] == "Time averages:":
                mat = lines[2].split()[1]
                print(mat)
                msd = lines[-1].split()[4]
                selfd = lines[-1].split()[5]
                Cv = lines[-1].split()[7]
                file.write(lj(mat)+lj(msd)+lj(selfd)+lj(Cv))

                if len(lines[4].split()) > 12:
                    debye = lines[-1].split()[8]
                    linde = lines[-1].split()[9]

                file.write("\n")
            f.close()
    file.close()
    return

def plot_properties():
    msd = []
    selfd = []
    spec_h = []
    #latt_c = []
    #bulk_m = []
    #coh_en = []
    #debye = []
    #linde = []

    f = open("property_calculations/collected_data", "r")

    lines = f.readlines()[1:]
    for x in lines:
        msd.append(float(x.split()[1]))
        selfd.append(float(x.split()[2]))
        #spec_h.append(float(x.split()[3]))
        #latt_c.append(float(x.split()[4]))
        #bulk_m.append(float(x.split()[5]))
        #coh_en.append(float(x.split()[6]))
        #debye.append(float(x.split()[7]))
        #linde.append(float(x.split()[8]))

    f.close()
    #Plotting mean square displacment vs self diffusion const
    # in figure 1
    pyplot.figure(1)
    pyplot.scatter(msd,selfd)
    #Labeling the axes with names from properties.py
    pyplot.xlabel("Mean square displacement [Å^2]")
    pyplot.ylabel("Self diffusion [Å^2/fs]")

    pyplot.show()

    return

if __name__ == "__main__":
    extract()
    plot_properties()
