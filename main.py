# Main Molecular dynamics simulation loop
import os
import md
import ase.io
from read_mp_project import read_mp_properties

def main():
    # read in the .json file as an command line argument?
    mp_properties = read_mp_properties('test_120_materials.json')

    try:
        for id, cif in enumerate(mp_properties['cif']):
            f = open("tmp_cif.cif", "w+")
            f.write(cif)
            f.close()
            atoms = ase.io.read("tmp_cif.cif", None)
            print("\n \n \nRUNNING MOLECULAR DYNAMICS")
            try:
                md.run_md(atoms, str(id))
            except:
                print("\n ERROR IN RUNNING MD \n")
            os.remove("tmp_cif.cif")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
