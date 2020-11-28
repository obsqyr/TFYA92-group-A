# Main Molecular dynamics simulation loop
import os
import md
import ase.io
from read_mp_project import read_mp_properties
import properties

def main():
    # read in the .json file as an command line argument?
    mp_properties = read_mp_properties('test_120_materials.json')

    # try to create folder 'property_calculations'
    # if it already exists, continue with the program
    try:
        os.mkdir('property_calculations')
    except:
        pass

    # primary loop for MD
    try:
        for id, cif in enumerate(mp_properties['cif']):
            f = open("tmp_cif.cif", "w+")
            f.write(cif)
            f.close()
            atoms = ase.io.read("tmp_cif.cif", None)
            print("\n \n \nRUNNING MOLECULAR DYNAMICS")
            try:
                md_res = md.run_md(atoms, str(id))
                N = len(md_res[0])
                temp_store = md_res[1]
                total_time = md_res[2]
                Cv = properties.specific_heat(temp_store, total_time, N)
            except Exception as e:
                print("\n ERROR IN RUNNING MD \n")
                print("Exception: ", e)
            os.remove("tmp_cif.cif")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
