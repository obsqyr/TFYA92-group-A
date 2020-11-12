import math
from ase import atoms

def distance2(pos1, pos2):
    return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2

def distance(pos1, pos2):
    return math.sqrt(distance2(pos1, pos2))


def meansquaredisp(atoms, old_atoms)
    pos = atoms.get_positions()
    old_pos = old_atoms.get_positions()
    length = len(pos)

    if length != len(old_pos)
        raise TypeError("Numbers of atoms doesnt match.")
        sys.exit('ERROR')

    msd = 0.0000

    for atom in range(length):
        msd =+ distance2(pos[atom], old_pos[atom])

    return msd/length
