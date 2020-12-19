# This is for testing to make a mongodb database

#import pymongo
import mongomock
import os
import re
import warnings
import json
import datetime
from bson.json_util import dumps
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
collection = db.posts

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
            dt = datetime.datetime.now()
            dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S." + str(dt.microsecond)[:3]+"Z")
            found = True
    if found: # only store in database if time average exist.
        post = {"Material ID": Id,
                "Material": system_name,
                "Unit Cell Composition": unit_cell_comp ,
                "Properties": {"Epot [eV/atom]": float(time_av_line[0]), "Ekin [eV/atom]": float(time_av_line[1]), "Etot [eV/atom]": float(time_av_line[2]),
                                "Temp [K]": float(time_av_line[3]), "MSD [Å^2]": float(time_av_line[4]),"Self diffusion [Å^2/fs]": float(time_av_line[5]),
                                "Pressure [Pa]": float(time_av_line[6]), "Specific_heat [eV/K]": float(time_av_line[7])},
                "last_modified": dt}
        collection.insert_one(post).inserted_id

        res_list.append(post)
    else:
        warnings.warn("No time averages over properties found.")

path = "optimade-python-tools/optimade/server/data/MD_structures.json"
cursor = collection.find()
with open(path, 'w') as file:
    file.write('[' + '\n')
    for document in cursor:
        file.write(dumps(document, indent = 3))
        file.write(',')
    file.write('\n' + ']')
