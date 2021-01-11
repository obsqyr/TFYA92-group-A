import subprocess
import shlex
import os
import json
from read_mp_project import read_mp_properties
# This module can be used for the extraction
# of monoatomic materials.

def make_pure_elements(els_list):
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

    return respond_list

def filter(arg_list, nsitemin, nsitemax):
    """Filters so nsites is within nsitemin and nsitemax.

    Parameters:
    arg_list (list): list of materials.
    nsitesmin (int): min of nsites.
    nsitemax (int): max of nsites.

    Returns:
    list: filtered list.
    """
    for i,el in enumerate(arg_list):
        nsites = el["nsites"]
        if nsites > nsitemax or nsites < nsitemin:
            # remove
            del arg_list[i]
        else:
            pass

    respond_filter_list = arg_list
    return respond_filter_list

def make_json_file(material_list, filename="pure_elements.json"):
    """Make the json file. Default name pure_elements.jsonself.

    Parameters:
    material_list (list): List of dictionaries, each dict contains a material.
    filename (str): path to that file that is to be created.

    Returns:
    None
    """
    # Make the json file with all responses
    dict_res = {"response": material_list}
    with open(filename, "w") as f:
        json.dump(dict_res, f, indent=4)
    return

if __name__ == "__main__":
    els_list = ["Ag", "Au", "Fe", "Cu", "Zn", "Pt", "Ti", "Co", "Ni", "Mg", "Pd"]
    nsitesmin = 1
    nsitesmax = 4
    respond_list = make_pure_elements(els_list)
    respond_filter_list = filter(respond_list, nsitesmin, nsitesmax)
    make_json_file(respond_filter_list) # with default file name pure_elements.json
