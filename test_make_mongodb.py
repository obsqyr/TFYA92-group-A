# This is for testing to make a mongodb database

#import pymongo
import mongomock
import os
import re
import warnings
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

for i in range(file_cnt):
    file = open("property_calculations/properties_"+str(i)+".txt", "r")
    lines = file.read().splitlines()
    Id = lines[0].split(":")[1]
    unit_cell_comp = lines[1].split(":")[1]
    system_name = lines[2].split(":")[1]
    print("This is the current system: ", Id)
    #last_line = lines[-1].split()
    pattern = re.compile(r'Time averages:')

    found = False
    for i in range(len(lines)):
        sentence = lines[i]
        #print("This is the sentence ", lines[i])
        if re.search(pattern, sentence):
            print("Inside the founding ", lines[i+3])
            time_av_line = lines[i+3]
            found = True
    if not found:
        warnings.warn("No time averages over properties found.")

    post = {"Material ID": Id,
            "Material": system_name,
            "Unit Cell Composition": unit_cell_comp ,
            "Properties": {"Epot [eV/atom]": time_av_line[0], "Ekin [eV/atom]": time_av_line[1], "Etot [eV/atom]": time_av_line[2],
                            "Temp [K]": time_av_line[3], "MSD [Å^2]": time_av_line[4],"Self diffusion [Å^2/fs]": time_av_line[5],
                            "Pressure [Pa]": time_av_line[6], "Specific_heat [eV/K]": time_av_line[7]}}

    post_id = db.posts.insert_one(post)
    print("This is the post_id: ", post_id)
