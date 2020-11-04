import numpy

class Extract:
    """docstring for Extract."""

    #pos = open("Positions_example", "r")
    #poslist = pos.readlines()

    def __init__(self, arg):
        self.var = arg
        self.pos = open("Positions_example", "r")
        self.poslist = self.pos.readlines()

    def latticeconst(self):
        return self.poslist[1]
    def latticevectors(self):
        return [self.poslist[14], self.poslist[15], self.poslist[16]]

ex = Extract(4)

print ex.latticeconst()
print ex.latticevectors()
