import ase.io
import math as m
import numpy as np
from read_settings import read_settings_file

NACL = ase.io.read("nacl.cif", None)

x = NACL.get_atomic_numbers()
#print (x)
#print (len(x))

y = NACL.get_positions()
#print (y[3])
#print (y)
#print (len(y))

data = read_settings_file()
print (data['time_step'])
