def reader():
    pos = open("Positions_example", "r")
    poslist = pos.readlines()
    print poslist[1]
    print poslist[5]
    print poslist[13]

if __name__ == "__main__":
    reader()
