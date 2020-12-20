#!/usr/bin/env python3
# Currently uses mongomock instead of pymonogo. Just change to pymongo for usage.
import mongomock
import os
import re
import warnings
import json
import datetime
from bson.json_util import dumps
import chemparse
from string import ascii_uppercase, ascii_lowercase

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
    print("This is pretty_formula ", pretty_formula)
    print("This is the dict ", dict)
    vals = list(dict.values())

    res = []
    for i in range(0, len(vals)):
        ratio_i = vals[i]/sum(vals)
        res.append(ratio_i)
    return res

def species_sites(pretty_formula):
    """Outputs a list over species at sites.

    Paramters:
    pretty_formula (str): A string over the pretty formula, empirical formula, over material.

    Returns:
    list: Returns a list of strings. Where each strings are an element symbol for each sites given
            by cartesian_site_positions.
    """
    dict = chemparse.parse_formula(pretty_formula)
    key_list = list(dict.keys())
    res_str = " "

    for key_str in map(str, key_list):
        cnt_element = dict[key_str]
        duplicate_str = key_str + " "
        extended_str = duplicate_str * int(cnt_element)
        res_str = res_str + extended_str

    res = res_str.split()
    return res

def anynomize_one_symbol(el_num_list):
    """ Code a list of elements. To have the anynomous formula.

    Paramters:
    el_num_list (list): A list of strings. Each string are numbers e.g. "10" over the number of
                    atoms of specific spieces.

    Returns:
    str: Returns a string of the anynomous formula, with proportion numbers, for the material.
    """

    # putting in "#"" to mark the end of string "ABCD..Z#"
    uppercase = ascii_uppercase + "#"

    for i in range(0, len(el_num_list)):
        first = uppercase[i]
        if first == "#": # after A,B,C...Z comes Aa, Ba, Ca,.. Za,.. e.t.c
            print("Now first = #, and i is ", i)
            print("After anynomize_two_symbols ")
            #break

        el_num = el_num_list[i]
        if el_num == str(1): # if 1 then omitted.
                el_num = ""

        else:
            yield first + el_num

def anynomize_two_symbols():
    # putting in "#"" to mark the end of string "ABCD..Z#"
    uppercase = ascii_uppercase + "#"

    print("Inside anynomize_two_symbols ")
    # Making codeing Aa, Ba, Ca,.. Za, Ab, Bb,...Zb etc.
    for i in range(26, len(el_num_list)): # A-Z is 26 symbols.
            ii = i
            for second in ascii_lowercase:
                for first in uppercase:
                    print("inside anyno_two this is first, second ", first, second)
                    if first == "#": # symbol after Zx where x is a-z
                        break
                    ii += 1
                    yield first + second + el_num[ii]


#    for first in uppercase: # Give you A-Z each time you iterate over.
#        if first == "#": # After A,B,C..Z comes Aa, Ba, Ca...
#            for second in ascii_lowercase:
#                for first in ascii_uppercase:
#                    yield first + second + el_num
#        else:
#            yield first + el_num



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
    sorted_values = sorted(value_list, reverse=True)

    # Make it anynomous
    res_str = []
    if len(sorted_values) <= 26: # A-Z is 26 symbols in total
        for value in anynomize_one_symbol(sorted_values):
            res_str.append(value)

    else:
        # after A,B,C...Z comes Aa, Ba, Ca,.. Za,.. e.t.c
        for value in anynomize_two_symbols(sorted_values):
            res_str.append(value)

    return res_str


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

    files = os.listdir("property_calculations") # How many files in dir
    file_cnt = len(files)

    for i in range(file_cnt):
        file = open("property_calculations/properties_"+str(i)+".txt", "r")
        lines = file.read().splitlines()
        Id = lines[0].split(":")[1]
        Id = int(Id)
        unit_cell_comp = lines[1].split(":")[1]
        system_name = lines[2].split(":")[1]
        system_name = system_name.replace(" ", "") # remove white space
        elements = extract_elements(system_name)
        el_ratios = calc_element_ratios(system_name)
        species_at_sites = species_sites(system_name)
        formula_anonymous = make_anonymous_form(system_name)
        #cartesian_site_pos = get_sites_pos()
        #species = make_species_structure("d")

        pattern = re.compile(r'Time averages:')
        found = False
        for i in range(len(lines)):
            sentence = lines[i]
            #print("This is the sentence ", lines[i])
            if re.search(pattern, sentence):
                time_av_line = lines[i+3]
                time_av_line = time_av_line.split()
                dt = datetime.datetime.now()
                found = True
        if found: # only store in database if time average exist.
            post = {"pretty_formula": system_name,
                    "Unit Cell Composition": unit_cell_comp ,
                    "Properties": {"Epot [eV/atom]": float(time_av_line[0]), "Ekin [eV/atom]": float(time_av_line[1]), "Etot [eV/atom]": float(time_av_line[2]),
                                    "Temp [K]": float(time_av_line[3]), "MSD [Å^2]": float(time_av_line[4]),"Self diffusion [Å^2/fs]": float(time_av_line[5]),
                                    "Pressure [Pa]": float(time_av_line[6]), "Specific_heat [eV/K]": float(time_av_line[7])},
                    "last_modified": dt,
                    "nperiodic_dimensions": 3, # work with cubic materials- HARD CODED
                    "dimension_types": [1, 1, 1],
                     "elements": elements,
                     "elements_ratios": el_ratios ,
                     "chemsys": "-".join(elements),
                     "nelements": len(elements),
                     "species_at_sites": species_at_sites,
                     #"nsites": len(cartesian_site_pos),
                     #"cartesian_site_positions": cartesian_site_pos
                     "formula_anonymous": formula_anonymous

                    }
            collection.insert_one(post).inserted_id
        else:
            warnings.warn("No time averages over properties found.")
    return collection

def MDdb_to_json(collection):
    path = "optimade-python-tools/optimade/server/data/MD_structures.json"
    cursor = collection.find()
    with open(path, 'w') as file:
        file.write('[' + '\n')
        for document in cursor:
            file.write(dumps(document, indent = 3))
            file.write(',')
        file.write('\n' + ']')
    return None

if __name__ == "__main__":
    db = make_MDdb()
    MDdb_to_json(db)
