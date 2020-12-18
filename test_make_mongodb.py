# This is for testing to make a mongodb database

#import pymongo
import mongomock
import os
import re
import warnings
import json
#client = pymongo.MongoClient() # default host and port
# Examples to specify host and port
#client = MongoClient('localhost', 27017)
#client = MongoClient('mongodb://localhost:27017/')
#connect('mongoenginetest', host='mongomock://localhost')

md_runned = os.path.exists("property_calculations")

if not md_runned:
    raise Exception("property_calculations folder doesn't exist.")

client = mongomock.MongoClient()
db = client.test_database
collection = db.test_collection

files = os.listdir("property_calculations") # How many files in dir
file_cnt = len(files)

res_list  = []
for i in range(file_cnt):
    file = open("property_calculations/properties_"+str(i)+".txt", "r")
    lines = file.read().splitlines()
    Id = lines[0].split(":")[1]
    Id = int(Id)
    unit_cell_comp = lines[1].split(":")[1]
    system_name = lines[2].split(":")[1]
    #last_line = lines[-1].split()
    pattern = re.compile(r'Time averages:')

    found = False
    for i in range(len(lines)):
        sentence = lines[i]
        #print("This is the sentence ", lines[i])
        if re.search(pattern, sentence):
            time_av_line = lines[i+3]
            time_av_line = time_av_line.split()
            #print("THIS IS TIME_AV_LINE ", time_av_line)
            found = True
    if found: # only store in database if time average exist.
        post = {"Material ID": Id,
                "Material": system_name,
                "Unit Cell Composition": unit_cell_comp ,
                "Properties": {"Epot [eV/atom]": float(time_av_line[0]), "Ekin [eV/atom]": float(time_av_line[1]), "Etot [eV/atom]": float(time_av_line[2]),
                                "Temp [K]": float(time_av_line[3]), "MSD [Å^2]": float(time_av_line[4]),"Self diffusion [Å^2/fs]": float(time_av_line[5]),
                                "Pressure [Pa]": float(time_av_line[6]), "Specific_heat [eV/K]": float(time_av_line[7])}}

        print("THIS IS THE POST ", post)
        #post_id = db.posts.insert_one(post)

        #print("This is the post_id: ", post_id)
        #print("THIS IS THE MATERIAL", db.posts.find_one({"Material ID": Id}))
        #res_list.append(db.posts.find_one({"Material ID": Id}))
        res_list.append(post)
        #print("THIS IS ThE POST : ", post)
    else:
        warnings.warn("No time averages over properties found.")


#Psuedokod för hur det ska vara(?)
path = "optimade-python-tools/optimade/server/data/MD_structures.json" # Maybe not hard coding this?
with open(path, "w") as f:
    dict = {"koko":3, "BABAB": 333}
    print("THIS IS THE CONTENT OF RES_LIST ", res_list)
    print("THE FIRST ELEMENT ", res_list[0])
    json.dump(res_list, f, indent=3)
    #print(res_list[i])
    #for i in range(0, len(res_list)):
    #    json.dump(res_list[i], f)
    #for i in range(0, len(res_list)):
    #    json.dump(res_list[i], f)
    #f.write("[ \n")
    #for i in range(1, len(res_list)):
    #    f.write(str(res_list[i])+", \n")
        #f.write("\n" + res_list[i] + ", ")
    #f.write("\n" + "]")


#file.write("ID" Id, "Material" system_name, "Unit cell comp" unit_cell_comp,
#    "groupA_properties" {"Epot" time_av_line[0], "Ekin" time_av_line[1], "Etot" time_av_line[2],
#    "Temp" time_av_line[3], "MSD" time_av_line[4], "Self diffusion" time_av_line[5],
#    "Preassure" time_av_line[6], "Specific heat" time_av_line[7]})
