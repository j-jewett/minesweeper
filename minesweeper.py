import random 

# GLOBAL VARIABLES

height = 0
width = 0
area = 0
mine_limit = 0
mines = 0
public_grid = []
private_grid = []

# FUNCTIONS

# RETRIEVE GAME SETTINGS FROM USER
def getGameSettings():
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

# CREATE PUBLIC AND PRIVATE GAME GRID
def createGame(height, width, mines):
    global public_grid
    global private_grid
    public_grid = [["_" for col in range(width)] for row in range(height)]
    private_grid = [["_" for col in range(width)] for row in range(height)]

    # POPULATES GRID 
    generateMines(private_grid, mines)
    generateNumbers(private_grid)
    
# RANDOM MINE GENERATION
def generateMines(grid, mines):
    temp_mines = mines
    while temp_mines > 0:
        for row in grid:
            for cell in range(0, len(row)):
                if row[cell] != "x" and random.randint(1, area) == 1:
                    row[cell] = "x"
                    temp_mines -= 1


# ITERATES THROUGH PRIVATE GRID, CALLS ADJACENT COUNTER TO POPULATE GRID
def generateNumbers(grid):
    for row in range(0, len(grid)):
        for col in range(0, len(grid[0])):
            adjacentCounter(grid, row, col)            
        
            

# COUNTS ADJACENT MINES AND POPULATES CELL WITH CORRECT NUMBER
def adjacentCounter(grid, row, col):
    adjacentMines = 0
    #inBounds = row - 1 >= 0 and col - 1 >= 0 and row + 1 <= len(grid) - 1 and col + 1 <= len(grid[0]) - 1
    if grid[row][col] == "x":
        return
    try:
        if grid[row - 1][col] == "x" and row - 1 >= 0 and grid[row][col] != "x":
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row - 1][col - 1] == "x" and row - 1 >= 0 and col - 1 >= 0 and grid[row][col]:
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row - 1][col + 1] == "x" and row - 1 >= 0:
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row][col - 1] == "x" and col - 1 >= 0:
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row + 1][col - 1] == "x" and col - 1 >= 0:
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row + 1][col + 1] == "x":
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row][col + 1] == "x":
            adjacentMines += 1
    except:
        pass
    try:
        if grid[row + 1][col] == "x":
            adjacentMines += 1
    except:
        pass
    grid[row][col] = str(adjacentMines)
        
    

            
    
    

# RETRIEVE GAME SETTINGS FROM USER
getGameSettings()

# CREATE GAME WITH SETTING
createGame(height, width, mines)


# PUBLIC GRID TEST
for row_line in public_grid:
        print(row_line)

# PRIVATE GRID TEST
for row_line in private_grid:
   print(row_line)

