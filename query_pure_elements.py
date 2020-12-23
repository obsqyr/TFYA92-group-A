import subprocess
import shlex
import os
import json
from read_mp_project import read_mp_properties
# This module can be used for the extraction
# of monoatomic materials.

els_list = ["Ag", "Au", "Fe", "Cu", "Zn", "Pt", "Ti", "Co", "Ni", "Mg", "Pd"]
respond_list = []
for el_str in map(str, els_list):
    f = open("tmp.json", "w")
    subprocess.call(shlex.split('./query_mp_project.sh ' + el_str +' -- ' + el_str), stdout=f)
    f.close()
    with open("tmp.json") as f:
        data = json.load(f)
    os.remove("tmp.json")
    # Error handling if request fails
    if not data["valid_response"] or data["num_results"] == 0:
        break
    else:
        response_el_str = data["response"]
        respond_list = respond_list + response_el_str

# Make the json file with all responses
dict_res = {"response": respond_list}
with open("pure_elements.json", "w") as f:
    json.dump(dict_res, f, indent=4)
