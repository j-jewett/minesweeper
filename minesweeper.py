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
game_test = True

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

# PARSE PLAYER ENTRY. Checks if help, close, or flags are called. Calls cell conversion helpers
def parseEntry(entry):
    # TEMP VARIABLE USAGE FOR GAME TESTING
    global game_test
    global public_grid
    global private_grid

    # HELP CHECK
    if entry.lower() == "help":
        getHelp()
    # GAME CLOSE CHECK
    elif entry == "close":
        print("Thanks for playing!")
        exit()
    # FLAG CHECK
    elif entry[-2:] == "+p" or entry[-2:] == "+P":
        if entry[0].isupper() and entry[1].islower():
            row_coord, col_coord = publicConversion(entry)
            plantFlag(public_grid, row_coord, col_coord)
        else:
            print("Invalid entry. Type 'help' for help.")
    # FLAG REMOVAL CHECK
    elif entry[-2:] == "-p" or entry[-2:] == "-P":
        if entry[0].isupper() and entry[1].islower():
            row_coord, col_coord = publicConversion(entry)
            removeFlag(public_grid, row_coord, col_coord)
        else:
            print("Invalid entry. Type 'help' for help.")
    
    # !!! VALID ENTRY CHECK
    elif len(entry) == 2:
        if entry[0].isupper() and entry[1].islower():
            row_coord, col_coord = publicConversion(entry)
            priv_row, priv_col = privateConversion(row_coord, col_coord)
            # TEST PRINTS TO CHECK FOR CORRECT COORDINATE CONVERSIONS
            print(row_coord)
            print(col_coord)
            print(priv_row)
            print(priv_col)

            # RETURNS TRUE IS PUBLIC CELL IS SELECTABLE (Has no flags or revealed numbers)
            if publicCheck(public_grid, row_coord, col_coord):
                # !!! RETRIEVES BACKEND VALUE OF SELECTED CELL AND UPDATES GRID                       
                cellCheck(private_grid, priv_row, priv_col)
            #game_test = False
        else:
            print("Invalid entry. Type 'help' for help.")
    # INVALID ENTRY
    else:
        print("Invalid entry. Type 'help' for help.")

# CONVERTS ENTRY TO PUBLIC GRID INDICES
def publicConversion(entry):
    temp_row_coord = entry[0].lower()
    temp_col_coord = entry[1]
    row_coord = 0
    col_coord = 0
    for i in range(0, len(alc)):
        if temp_row_coord == alc[i]:
            row_coord = i + 1
    for i in range(0, len(alc)):
        if temp_col_coord == alc[i]:
            col_coord = i + 1
    return row_coord, col_coord


# CONVERTS ENTRY TO PRIVATE GRID INDICES
def privateConversion(row_coord, col_coord):
    priv_row = row_coord - 1
    priv_col = col_coord - 1
    return priv_row, priv_col

# PLANTS FLAG ON PUBLIC GRID
def plantFlag(grid, row_coord, col_coord):
    if grid[row_coord][col_coord] == "_":
        grid[row_coord][col_coord] = 'P'


# REMOVE FLAG ON PUBLIC GRID
def removeFlag(grid, row_coord, col_coord):
    if grid[row_coord][col_coord] == 'P':
        grid[row_coord][col_coord] = '_'

# CHECKS FOR PUBLIC FLAG BEFORE CALL PRIVATE CELL CHECK
def publicCheck(grid, row, col):
    cell_value = grid[row][col]
    if cell_value == "_":
        return True
    elif cell_value == "P":
        print("Remove the flag before selecting this cell using the suffix '-p'.")
        return False
    elif cell_value >= "0":
        print("This cell as already been selected, please make a different entry.")
        return False

# !!! CHECKS FOR CONTENTS OF PRIVATE CELL
def cellCheck(grid, row, col):
    cell_value = grid[row][col]
    # PLAYER FOUND A MINE, TRIGGERS GAME END
    if cell_value == "x":
        hitMine(grid)
    # !!! PLAYER FOUND A ZERO, CREATES 'NUMBER ENCLOSURE' AROUND CELL AND ADJACENT ZEROS
    elif cell_value == "0":
        hitZero()
    # REVEALS NUMBER OF ADJACENT MINES ON PUBLIC GRID
    elif int(cell_value) > 0:
        updatePublic(cell_value, row, col)

    
    


# UPDATES PUBLIC GRID
def updatePublic(val, row, col):
    global public_grid
    public_grid[row + 1][col + 1] = val

# !!! REVEALS CLUSTER OF CELLS WHEN A PLAYER FINDS A ZERO
def hitZero():
    pass

# TRIGGERS GAME END IF PLAYER HITS A MINE
def hitMine(grid):
    addCoordinates(grid)
    for row_line in grid:
        print(row_line)
    print("You hit a mine, better luck next time!")
    exit()

# !!! CHECKS IF GAME END CONDITIONS ARE MET (Hit a mine or selected all non-mine cells)
def endCheck():
    pass



# RETRIEVE GAME SETTINGS FROM USER
getGameSettings()

# CREATE GAME WITH SETTING
createGame(height, width, mines)

# RUN GAME FOR TESTING
while(game_test):
    displayPublicGrid(public_grid)
    entry = getGameInput()
    parseEntry(entry)

# PUBLIC GRID TEST
for row_line in public_grid:
        print(row_line)

# PRIVATE GRID TEST
for row_line in private_grid:
   print(row_line)

