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
    response_el_str = data["response"]
    respond_list = respond_list + response_el_str

dict_res = {"response": respond_list}
with open("pure_elements.json", "w") as f:
    json.dump(dict_res, f, indent=4)

r = read_mp_properties("pure_elements.json")
print("This is the keys ", r.keys())
