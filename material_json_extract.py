#!/usr/bin/env python3

from read_mp_project import read_mp_properties

mp_properties = read_mp_properties('testing_data_materials.json')

#print("Available properties:",mp_properties.keys())

#print("Printing material_id:")
#print(mp_properties["material_id"])

print("NEW TEST PRINTING...")
# to print the .cif file of first material, write:
# print(mp_properties["cif"][1])

print(mp_properties["cif"][1])
