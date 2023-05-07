height = 0
width = 0
area = 0
mine_limit = 0
mines = 0

def getInput():
    global area
    global mine_limit
    getHeight()
    getWidth()
    print(height)
    print(width)
    area = width * height
    print(area)
    mine_limit = area // 2
    print(mine_limit)
    getMines()

def getHeight():
    global height
    while(True):
        try:
            height = int(input("Please choose a height for this game (up to 20): "))
            if height < 1 or height > 20:
                raise TypeError
            break
        except TypeError:
            print("Invalid entry. Please enter an integer between 1-20.")

def getWidth():
    global width
    while(True):
        try:
            width = int(input("Please choose a width for this game (up to 20): "))
            if width < 1 or width > 20:
                raise TypeError
            break
        except TypeError:
            print("Invalid entry. Please enter an integer between 1-20.")

def getMines():
    global mines
    while(True):
        try:
            mines = int(input("Please choose the number of mines for this game.\nYou can place up to {0} mines for a grid of this size: ".format(mine_limit)))
            if mines < 1 or mines > mine_limit:
                raise TypeError
            break
        except TypeError:
            print("Invalid entry. Please enter an integer between 1-{0}.".format(mine_limit))

getInput()


