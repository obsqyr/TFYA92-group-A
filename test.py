import unittest
import json
import os
import subprocess
from read_mp_project import read_mp_properties

print(".....Runnint unittest for feature: material extraction.....")

class Testreadmp(unittest.TestCase):
    # Testing properties of extracted materials.
    # read_mp_project.py checked
    def test_extracted_materials(self):
        mp_properties = read_mp_properties('testing_data_materials.json')
        tmp_keys = ['material_id', 'pretty_formula', 'elements',
                'nelements', 'energy', 'energy_per_atom', 'density', 'volume',
                 'nsites', 'band_gap', 'total_magnetization', 'G_Reuss', 'G_VRH',
                  'G_Voigt', 'G_Voigt_Reuss_Hill', 'K_Reuss', 'K_VRH', 'K_Voigt',
                   'K_Voigt_Reuss_Hill', 'elastic_anisotropy', 'elastic_tensor',
                    'homogeneous_poisson', 'poisson_ratio', 'universal_anisotropy',
                     'elastic_tensor_original', 'compliance_tensor', 'warnings', 'piezo',
                      'diel', 'copyright', 'cif', 'elasticity']
        with open('testing_data_materials.json') as f:
            json_data = json.load(f)
        num_results = json_data["num_results"]


        self.assertEqual(tmp_keys, list(mp_properties))
        # check if content of extracted cif is the same as manually downloaded.
        with open("AcAg_mp-866199_computed.cif") as f:
            content_in_cif = f.read()
        self.assertEqual(mp_properties["cif"][0], content_in_cif)
        self.assertEqual(mp_properties["material_id"][0],"mp-866199")

        self.assertEqual(len(mp_properties["cif"]), num_results)


    # Testing fails and error handlingself.
    # query_mp_project.sh checked
    def test_extration_process(self):
        # no materials existed. Trying to exttract something which doesn't existself.
        # No MP_API_KEY
        # Check if errors or warnings are in?
        # The warnings should be handled
        with open('testing_data_materials.json') as f:
            json_data = json.load(f)
        valid_response = json_data["valid_response"]
        self.assertEqual(True, valid_response)
        # create temporary file to store response results
        #subprocess.call(["query_mp_project.sh AM -- O > tmp_res_file.json", "AM --"])
        #subprocess.call([""])
        """
        with open("tmp_res_file.json") as f:
            json_data = json.load(f)
        valid_response = json_data["valid_response"]
        num_results = json_data["num_results"]
        self.assertEqual(valid_response, True)
        self.assertEqual(num_results, 0)
        os.remove("tmp_res_file.json")
        """


if __name__ == '__main__':
    unittest.main()
