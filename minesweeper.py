import random
from string import ascii_uppercase as auc
from string import ascii_lowercase as alc 

# GLOBAL VARIABLES

height = 0
width = 0
area = 0
mine_limit = 0
mines = 0
public_grid = []
private_grid = []
# TEMP VARIABLE TO TEST GAME FUNCTIONALITY AS I BUILD
gameTest = True

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

# RETRIEVE GAME HEIGHT
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

# RETRIEVE GAME WIDTH
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

# RETRIEVE NUMBER OF MINES TO GENERATE
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

    # FINISHES GRID SETUP  
    generateMines(private_grid, mines)
    generateNumbers(private_grid)
    addCoordinates(public_grid)

    # WELCOME MESSAGE
    print("WELCOME TO MINESWEEPER")
    getHelp()
    
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
            adjacentCounter(grid, row, col)            
        
            
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


# ADDS COORDINATE SYSTEM ALONG THE LEFT AND TOP SIDES OF PUBLIC LIST
def addCoordinates(grid):
    upperCoords = ["="]

    for row in range(0, len(grid)):
        grid[row].insert(0, auc[row])

    for col in range(0, len(grid[0]) - 1):
        upperCoords.append(alc[col])
    grid.insert(0, upperCoords)
    
# RENDER PUBLIC GRID IN TERMINAL
def displayPublicGrid(grid):
    for row_line in grid:
        print(row_line)

def getGameInput():
    entry = input("Pick a cell to to check: ")
    return entry

# PRINT INSTRUCTIONS FOR PLAYER
def getHelp():
    print("Pick a cell by by typing the coordinates in 'Ab' form")
    print("Append '-p' to your entry to plant a flag")
    print("Type 'help' for instructions")
    print("Type 'close' to end the game")

# !!! PARSE PLAYER ENTRY. Checks if help, close, or flags are called. Calls cell conversion helpers
# Still need to finish code for valid entries (checks and flags)
def parseEntry(entry):
    # TEMP VARIABLE USAGE FOR GAME TESTING
    global gameTest

    if entry == "help":
        getHelp()
        return
    elif entry == "close":
        closeGame()
    elif entry[-2:] == "-p":
        pass
    elif len(entry) == 2:
        if entry[0].isupper() and entry[1].islower():
            rowCoord, colCoord = publicConversion(entry)
            privRow, privCol = privateConversion(rowCoord, colCoord)
            # TEST PRINTS TO CHECK FOR CORRECT COORDINATE CONVERSIONS
            print(rowCoord)
            print(colCoord)
            print(privRow)
            print(privCol)
            gameTest = False
        else:
            print("Invalid entry. Type 'help' for help.")
            getGameInput()
    else:
        print("Invalid entry. Type 'help' for help.")
        getGameInput()

# !!! CONVERTS ENTRY TO PUBLIC GRID INDICES
def publicConversion(entry):
    tempRowCoord = entry[0].lower()
    tempColCoord = entry[1]
    rowCoord = 0
    colCoord = 0
    for i in range(0, len(alc)):
        if tempRowCoord == alc[i]:
            rowCoord = i + 1
    for i in range(0, len(alc)):
        if tempColCoord == alc[i]:
            colCoord = i + 1
    return rowCoord, colCoord


# !!! CONVERTS ENTRY TO PRIVATE GRID INDICES
def privateConversion(rowCoord, colCoord):
    privRow = rowCoord - 1
    privCol = colCoord - 1
    return privRow, privCol

# !!! PLANTS FLAG ON PUBLIC GRID
def plantFlag():
    pass

# !!! CHECKS FOR CONTENTS OF PRIVATE CELL
def cellCheck():
    pass

# !!! UPDATES PUBLIC GRID
def updatePublic():
    pass

# !!! REVEALS CLUSTER OF CELLS WHEN A PLAYER FINDS A ZERO
def hitZero():
    pass

# !!! CHECKS IF GAME END CONDITIONS ARE MET (Hit a mine or selected all non-mine cells)
def endCheck():
    pass

# !!! CLOSE GAME
def closeGame():
    pass
    
    

# RETRIEVE GAME SETTINGS FROM USER
getGameSettings()

# CREATE GAME WITH SETTING
createGame(height, width, mines)

# RUN GAME FOR TESTING
while(gameTest):
    displayPublicGrid(public_grid)
    entry = getGameInput()
    parseEntry(entry)

# PUBLIC GRID TEST
for row_line in public_grid:
        print(row_line)

# PRIVATE GRID TEST
for row_line in private_grid:
   print(row_line)

