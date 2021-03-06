#!/usr/bin/env python3
# Currently uses mongomock instead of pymonogo. Just change to pymongo for usage.
import mongomock
import os
import re
import warnings
import datetime
from bson.json_util import dumps
import chemparse
from string import ascii_uppercase, ascii_lowercase
from read_settings import read_settings_file


def extract_elements(pretty_formula):
    """Returns a list of strings over elements pretty_formula consists of.

    Paramters:
    pretty_formula (str): A string over the pretty formula, empirical formula, over material.

    Returns:
    list: Returns a list of strings, consisting of elements from empirical formula.
    """
    dict = chemparse.parse_formula(pretty_formula)
    elements_list = list(dict.keys())

    return elements_list

def calc_element_ratios(pretty_formula):
    """ Calculates the ratio of unique elements in a material.

    Paramters:
    pretty_formula (str): A string over the pretty formula, empirical formula, over material.

    Returns:
    list: Returns a list of floats. These floats are element ratios for the elements given in the same
            order as they occur in pretty_formula.
    """
    dict = chemparse.parse_formula(pretty_formula)
    vals = list(dict.values())

    res = []
    for i in range(0, len(vals)):
        ratio_i = vals[i]/sum(vals)
        res.append(ratio_i)
    return res


def anynomize_one_symbols(el_num_list):
    """ Code a list of elements. Make the anynomous coding A,B,C,...Z followed by corresponding chemical
        propotional number. So for the chemical Ag3Na2Mg4 get the coding A4B3C1.

    Paramters:
    el_num_list (list): A list of strings. Each string are numbers specifiying the number of
                        atoms of specific spieces. For example for system Ag3Na2Mg4
                        el_num_list should be ["4", "3", "2"].

    Returns:
    str: Returns a string of the anynomous formula, with proportion numbers, for the material.
    """
    # putting in "#"" to mark the end of string "ABCD..Z#"

    for i in range(0, len(el_num_list)):
        first = ascii_uppercase[i]
        el_num = el_num_list[i]
        if el_num == str(1): # if 1 then omitted.
                el_num = ""
                yield first + el_num
        else:
            yield first + el_num

def anynomize_two_symbols(el_num_list):
    """ Code a list of elements. Make the anynomous coding Aa, Ba, Ca,..Za, Ab, Bb,..Zb e.t.c
        followed by corresponding chemical propotional number. This function is called only if the number of
        elements exceeds 26. It's called after anynomize_one_symbols(el_num_list) to code anynomous formula
        for the number 27th and above element.

    Paramters:
    el_num_list (list): A list of strings. Each string are numbers specifiying the number of
                        atoms of specific spieces.

    Returns:
    str: Returns a string of the anynomous formula, of two symbols followed by proportion numbers for the material.
    """
    # putting in "#"" to mark the end of string "ABCD..Z#"
    uppercase = ascii_uppercase + "#"
    # Making codeing Aa, Ba, Ca,.. Za, Ab, Bb,...Zb etc.
    ii = -1
    for second in ascii_lowercase:
        if ii == len(el_num_list):
            break
        for first in uppercase:
            ii += 1
            if first == "#": # symbol after Zx where x is a-z
                ii = ii - 1
                break
            elif ii == len(el_num_list):
                break
            el_num = el_num_list[ii]
            if el_num == str(1):
                el_num = ""
                yield first + second + el_num
            else:
                yield first + second + el_num



def make_anonymous_form(pretty_formula):
    """ Converts into formula anynomous.
    Paramters:
    pretty_formula (str): A string over the pretty formula, empirical formula, over material.

    Returns:
    str: Returns a string the anonymous formula. This is the pretty_formula but the elements are
            first ordered by their chemical proportion number, and then, in order left to right,
            replaced by anonymous symbols A, B, C, ..., Z, Aa, Ba, ..., Za, Ab, Bb, ... and so on.
    """
    dict = chemparse.parse_formula(pretty_formula)
    values_list = list(dict.values())
    sorted_values = sorted(values_list, reverse = True)
    # Make into list of strings
    # initially a list of floats so int(x) necessary
    tmp_str = " ".join(str(int(x)) for x in sorted_values)
    sorted_values = tmp_str.split()

    # Make it anynomous
    res_str_list = []
    if len(sorted_values) > 26: # A-Z is 26 symbols in total
        sorted_vals_1 = sorted_values[0:26]
        sorted_vals_2 = sorted_values[26:len(sorted_values)]
        for value in anynomize_one_symbols(sorted_vals_1):
            res_str_list.append(value)
        # after A,B,C...Z comes Aa, Ba, Ca,.. Za,.. e.t.c
        for value in anynomize_two_symbols(sorted_values):
            res_str_list.append(value)
    else: # If less or equal to 26 symbols
        for value in anynomize_one_symbols(sorted_values):
            res_str_list.append(value)

    res_str = "".join(res_str_list)
    return res_str

def get_sites_pos(file_str):
    """ Get the cartesian site positions from property files.

    Paramters:
    file_str (str): File path to read from.

    Returns:
    list: Returns a list of lists, where each inner list contains positions
            of each sites. So [[x1, y1, z1],[x2, y2, z2]] is the structure for a
            system of two sites with positions (x1, y1, z1) and (x2, y2, z2)
            respectively.
    """
    file = open(file_str, "r")
    lines = file.read().splitlines()
    file.close()
    #species_els = lines[4].split()
    species_els = lines[5].split()

    # Make strucutre [[],[],[]] if 3 sites e.g.
    site_pos_res = []
    site_num =  len(species_els)
    for i in range(site_num):
        site_pos_res.append([])
    comps_x = lines[5].split()
    comps_y = lines[6].split()
    comps_z = lines[7].split()
    for ii in range(0, site_num):
        val1 = comps_x[ii]
        val2 = comps_y[ii]
        val3 = comps_z[ii]
        site_pos_res[ii].append(float(val1))
        site_pos_res[ii].append(float(val2))
        site_pos_res[ii].append(float(val3))

    return site_pos_res

def get_task_Id(file):
    """ Returns the task_id for structure. It's an id which uniquely
        defines the material for material. It's also known as Material Id
        in the properties files after MD simulation.

        Parameters:
        file (str): file is a string over the path to a file.

        Returns:
        str: returns id number as a string.
    """
    file = open(file, "r")
    lines = file.read().splitlines()
    file.close()
    Id = lines[0].split(":")[1]
    return Id

def get_species(pretty_formula):
    """Get the structure required to fill in the field species.

    Paramters:
    pretty_formula (str): String for the chemical formula of the system.

    Returns:
    list: Returns a list of dictionaries. Every dictionary corresponds to a species. Each
            dictionary contains three elements, with keys "chemical_symbols","concentration"
             and "name" (read documenation for more info). Note that the values are specifically
             written for the MD software that is available.
    """
    res = []

    # list of unique species
    dict = chemparse.parse_formula(pretty_formula)
    unique_species = list(dict.keys())
    for i in range(0, len(unique_species)):
        str_val = unique_species[i]
        res_i = {
                    "chemical_symbols": [str_val],
                    "concentration": [1.0],
                    "name": str_val
                }
        res.append(res_i)
    return res

def get_properties_collected_data(Id, file_str = "property_calculations/collected_data.txt"):
    """ Get the Cohesive energy, Lattice constant, interpolated lattice constant,
        Bulk modulus, Debye and Lindemann for material with Material Id
        (or task id in database)
        Id.

    Paramters:
    Id: Material Id that identify specific material. Also task Id in database.
    file_str (str): File path to "collected_data.txt".

    Returns:
    Boolean: Boolean False returned when id of the material is not found in collected_data.txt
    list: Returns a list of floats for value of Cohesive energy, Lattice constant,
            interpolated lattice constant, Bulk modulus, Debye and Lindemann.
            In the same order as specified.
    """
    settings = read_settings_file()
    file = open(file_str, "r")
    content_str = file.read()
    file.close()

    # /n folloed by Id
    Id = Id.split()[0]
    search_id_str = "\n  " + Id + " "
    if search_id_str in content_str:
        header = content_str.splitlines()[0]
        # index of when line starts
        line_start = content_str.find(search_id_str)
        # index of when line ends
        line_end = content_str.find("\n", line_start + 1)
        line_str = content_str[line_start + 1: line_end]
        col = line_str.split()
        coh_en = float(col[2])
        latt_c = [float(col[i]) for i in range(6, 9)]
        if "Bulk modulus" in header:
            inter_latt_c = [float(col[i]) for i in range(9, 12)]
            bulk_m = float(col[12])
            if len(col) <= 13:
                debye = " "
                linde = " "
            else:
                debye = col[13]
                linde = col[14]
        elif not "Bulk modulus" in header and settings['vol_relax']:
            raise Exception("Bulk Modulus missing.")
    # material id not found
    else:
        not_extra_volrelax = False
        return not_extra_volrelax

    return [coh_en, latt_c, inter_latt_c, bulk_m, debye, linde]

def make_MDdb():
    """ Makes a mongodb database from results by running MD simulation.

    Returns: Returns the database, in this case one collection, over the results.
    """
    md_runned = os.path.exists("property_calculations")
    if not md_runned:
        raise Exception("property_calculations folder doesn't exist.")
    client = mongomock.MongoClient()
    db = client.test_database
    collection = db.posts
    files = os.listdir("property_calculations")
    files.remove("collected_data.txt") #file collected_data not included

    for file in map(str, files):
        path = "property_calculations/" + file
        Id = get_task_Id(path)
        file = open(path, "r")
        lines = file.read().splitlines()
        unit_cell_comp = lines[1].split(":")[1]
        system_name = lines[2].split(":")[1]
        system_name = system_name.replace(" ", "") # remove white space
        cartesian_site_pos = get_sites_pos(path)
        species_at_sites = lines[4].split()
        species = get_species(system_name)
        elements = extract_elements(system_name)
        el_ratios = calc_element_ratios(system_name)
        formula_anonymous = make_anonymous_form(system_name)
        dt = datetime.datetime.now()
        prop_collected = get_properties_collected_data(Id)
        # Is False when id not found
        if not prop_collected:
            pass

        else:
            cohesive, lattice_constant, inter_latt_c, bulkmod, debye, lindemann = prop_collected
            lc_a, lc_b, lc_c = lattice_constant
            lc_i_a, lc_i_b, lc_i_c = inter_latt_c

            if len(species_at_sites) != len(cartesian_site_pos):
                raise Exception("nsites not the same as number of species_at_sites. For material ID", Id)

            pattern = re.compile(r'Time averages:')
            found = False
            for i in range(len(lines)):
                sentence = lines[i]
                if re.search(pattern, sentence):
                    time_av_line = lines[i+3]
                    time_av_line = time_av_line.split()
                    found = True
             # only store in database if time averages of properties exist.
             # and in case of volume relaxed, only store the relevant system.
            if found:
                post = {
                        "pretty_formula": system_name,
                        "unit_cell_composition": unit_cell_comp ,
                        "epot [eV/atom]": float(time_av_line[0]),
                        "ekin [eV/atom]": float(time_av_line[1]),
                        "etot [eV/atom]": float(time_av_line[2]),
                        "temp [K]": float(time_av_line[3]),
                        "MSD [angstrom^2]": float(time_av_line[4]),
                        "self_diffusion [angstrom^2/fs]": float(time_av_line[5]),
                        "pressure [Pa]": float(time_av_line[6]),
                        "specific_heat [eV/K]": float(time_av_line[7]),
                        "lattice_constant_a": lc_a,
                        "lattice_constant_b": lc_b,
                        "lattice_constant_c": lc_c,
                        "interpolated_lattice_constant_a": lc_i_a,
                        "interpolated_lattice_constant_b": lc_i_b,
                        "interpolated_lattice_constant_c": lc_i_c,
                        "bulk_modulus": bulkmod,
                        "cohesive_energy": cohesive,
                        "debye": debye,
                        "lindemann": lindemann,
                        "last_modified": dt,
                        "nperiodic_dimensions": 3, #bulk 3D system
                        "dimension_types": [1, 1, 1],
                        "elements": elements,
                        "elements_ratios": el_ratios ,
                        "chemsys": "-".join(elements),
                        "nelements": len(elements),
                        "species_at_sites": species_at_sites,
                        "formula_anonymous": formula_anonymous,
                        "structure_features": [], #Specific for MD
                        "task_id": Id,
                        "cartesian_site_positions": cartesian_site_pos,
                        "species": species,
                        "nsites": len(cartesian_site_pos)
                        }
                collection.insert_one(post).inserted_id
            else:
                warnings.warn("No time averages over properties found.")
    return collection

def MDdb_to_json(collection):
    # ----------------------IMPORTANT INFORMATION ------------------------------------
    # Note that to make data aviailable file MD_structures.json needs to have path
    # "optimade-python-tools/optimade/server/data/MD_structures.json" in
    # repository https://github.com/attlevafritt/tfya92-groupa-optimade-python-tools.git
    if not os.path.exists('MD_result_data'):
        os.mkdir('MD_result_data')
    path = "data/MD_structures.json"
    cursor = collection.find()
    with open(path, 'w') as file:
        file.write('[' + '\n' + "   ")
        for i, document in enumerate(cursor):
            file.write(dumps(document, indent = 6))
            if i != collection.count() - 1: # if last element don't print ,
                file.write(',')
        file.write('\n' + ']')
    return None

if __name__ == "__main__":
    db = make_MDdb()
    MDdb_to_json(db)
