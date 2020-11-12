import ase.io
import math as m
import numpy as np

NACL = ase.io.read("nacl.cif", None)

x = NACL.get_atomic_numbers()
print (x)
print (len(x))

y = NACL.get_positions()
#print (y[3])
print (y)
#print (len(y))
#print (y[3,2])

print (2*y)
