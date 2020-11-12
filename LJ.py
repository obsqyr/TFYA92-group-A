import math

def pot_LJ(r, sigma=1, epsilon=1):
    return 4*epsilon*( (sigma/r)**12 - (sigma/r)**6 )


def pot_LJTS(pos1, pos2, sigma=1, epsilon=1, r_cutoff=1):
    r = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2
                  + (pos1[2] - pos2[2])**2)

    if (r <= r_cutoff):
       return  pot_LJ(r) - pot_LJ(r_cutoff)
    else:
        return 0
        
    
if __name__ == "__main__":
   print(pot_LJTS([4,5,2],[3,1,5], r_cutoff=6))
