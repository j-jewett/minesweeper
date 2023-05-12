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
            height = int(input("Please choose a height for this game (between 5-26): "))
            if height < 5 or height > 26:
                raise TypeError
            break
        except TypeError:
            print("Invalid entry. Please enter an integer between 5-26.")

# RETRIEVE GAME WIDTH
def getWidth():
    global width
    while(True):
        try:
            width = int(input("Please choose a width for this game (between 5-26): "))
            if width < 5 or width > 20:
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
    while temp_mines >= 1:
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
    
    # VALID ENTRY CHECK
    elif len(entry) == 2:
        if entry[0].isupper() and entry[1].islower():
            row_coord, col_coord = publicConversion(entry)
            priv_row, priv_col = privateConversion(row_coord, col_coord)
            
            # RETURNS TRUE IS PUBLIC CELL IS SELECTABLE (Has no flags or revealed numbers)
            if publicCheck(public_grid, row_coord, col_coord, True):
                # RETRIEVES BACKEND VALUE OF SELECTED CELL AND UPDATES GRID                       
                cellCheck(private_grid, priv_row, priv_col)
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
def publicCheck(grid, row, col, mode=False):
    cell_value = grid[row][col]
    if cell_value == "_":
        return True
    elif cell_value == "P":
        if mode:
            print("Remove the flag before selecting this cell using the suffix '-p'.")
        return False
    else:
        if mode:
            print("This cell as already been selected, please make a different entry.")
        return False

# CHECKS FOR CONTENTS OF PRIVATE CELL
def cellCheck(grid, row, col):
    cell_value = grid[row][col]  
    # !!! PLAYER FOUND A ZERO, CREATES 'NUMBER ENCLOSURE' AROUND CELL AND ADJACENT ZEROS
    if cell_value == "0":
        hitZero(grid, row, col)
    # REVEALS NUMBER OF ADJACENT MINES ON PUBLIC GRID
    elif cell_value != "x":
        updatePublic(cell_value, row, col)
    # PLAYER FOUND A MINE, TRIGGERS GAME END
    elif cell_value == "x":
        grid[row][col] = "X"
        hitMine(grid)
    
    
    
    

    
    


# UPDATES PUBLIC GRID
def updatePublic(val, row, col):
    global public_grid
    public_grid[row + 1][col + 1] = val

# !!! REVEALS CLUSTER OF CELLS WHEN A PLAYER FINDS A ZERO
def hitZero(grid, row, col):
    # LIST TO ITERATE THROUGH TO CHECK ADJACENT CELLS
    updatePublic("0", row, col)
    compass = ["nw", "n", "ne", "e", "se", "s", "sw", "w"]
    for direction in compass:
        # RETURNS TRUE IF CELL IN GIVEN DIRECTION EXISTS
        adjacentCheck(direction, grid, row, col)   

# !!! CHECKS IF ADJACENT 
def adjacentCheck(direction, grid, row, col):
    global public_grid
    if direction == "nw":
        if row > 0 and col > 0 and publicCheck(public_grid, row, col):
            cellCheck(grid, row - 1, col - 1 )
    if direction == "n":
        if row > 0 and publicCheck(public_grid, row, col + 1):
            cellCheck(grid, row - 1, col)
    if direction == "ne":
        if row > 0 and col < len(grid[0]) - 1  and publicCheck(public_grid, row, col + 2):
            cellCheck(grid, row - 1, col + 1)
    if direction == "e":
        if col < len(grid[0]) - 1 and publicCheck(public_grid, row + 1, col + 2):
            cellCheck(grid, row, col + 1)
    if direction == "se":
        if row < len(grid) - 1 and col < len(grid[0]) - 1 and publicCheck(public_grid, row + 2, col + 2):
            cellCheck(grid, row + 1, col + 1)
    if direction == "s":
        if row < len(grid) - 1 and publicCheck(public_grid, row + 2, col + 1):
            cellCheck(grid, row + 1, col)
    if direction == "sw":
        if row < len(grid) - 1 and col > 0 and publicCheck(public_grid, row + 2, col):
            cellCheck(grid, row + 1, col - 1)
    if direction == "w":
        if col > 0 and publicCheck(public_grid, row + 1, col):
            cellCheck(grid, row, col - 1)

# TRIGGERS GAME END IF PLAYER HITS A MINE
def hitMine(grid):
    addCoordinates(grid)
    for row_line in grid:
        print(row_line)
    print("You hit a mine, better luck next time!")
    exit()

# CHECKS IF GAME END CONDITIONS ARE MET (Hit a mine or selected all non-mine cells)
def endCheck(grid):
    global mines
    empty_counter = 0
    for row in grid:
        for col in range(1, len(row)):
            if row[col] == "_" or row[col] == "P":
                empty_counter += 1
    if empty_counter == mines:
        displayPublicGrid(grid)
        print("CONGRATS! You win!")
        exit()



# RETRIEVE GAME SETTINGS FROM USER
getGameSettings()

# CREATE GAME WITH SETTING
createGame(height, width, mines)

# RUN GAME FOR TESTING
while(True):
    displayPublicGrid(public_grid)
    entry = getGameInput()
    parseEntry(entry)
    endCheck(public_grid)



