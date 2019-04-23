#changed panel to panel, generate_panel to generate_panel, # to #,

# In this section we define the core utilites for the project


import random
import copy as cp

# The list of available actions

actions = ("ABOVE", "BELOW", "LEFT", "RIGHT")


# The function generate_panel generates the panel 


def generate_panel(N):

    # The Dimension is not 'VALID'

    assert N >= 1, "Invalid Dimension"


    # A is always an 'INTEGER'

    assert type(N) == int, "N must be Integer"



    panel = [['#' for i in range(N)] for i in range(N)]
    return panel

# The function print_panel prints the outlook of the panel

def print_panel(panel):


    N = len(panel)

    for rows in range(0,N):

        print("           ")

        for columns in range(0,N):
            if panel[rows][columns] != '#':
                print(repr(panel[rows][columns]).ljust(5), end="")
           
            else:
                print(panel[rows][columns].ljust(5), end="")


# check_full continuously checks if the panel is full

def check_full(panel):
  
    N = len(panel)
    for a in range(N):

        for m in range(N):

            if panel[a][m] == '#':

                return False
    return True


# get_not_filled_cell finds all the emplty cells in the panel. In this case we use a tuple to replace the location of the cell


def get_not_filled_cell(panel):
   
    not_filled_cell = []
    N = len(panel)
    for a in range(N):
        for m in range(N):
            if panel[a][m] == '#':
                not_filled_cell.append((a,m))
    
    return not_filled_cell


# Find the the maximum number of cells in the panel

def get_max_no_cells(panel):
   
    N = len(panel)
    perfect_cell = 0
    for a in range(N):
        for m in range(N):
            if panel[a][m] != '#' and panel[a][m] > perfect_cell:
                perfect_cell = panel[a][m]
    
    return perfect_cell

# check_gameOver checks if the game is at ending stage.

def check_gameOver(panel):
   
    N = len(panel)

    # Checking if the panel is full and if adjoining cells are exactly same
    
    if not check_full(panel):
        return False
    
    # Now checking the rows for the gameOver condition
    
    for a in range(N):
        for m in range(1,N):
            if panel[a][m] == panel[a][m-1]:
                return False
    
    # Again checking the colums for gameOver condition
    
    for a in range(N):
        for m in range(1,N):
            if panel[m][a] == panel[m-1][a]:
                return False
    
    return True

# To find the element in the certain positon A(x,y)

def find_element(panel, m):
   
    x, y = m
    N = len(panel)
    if x < 0 or x >= N or y < 0 or y >= N:
        return None

    return panel[x][y]

# To put an element in a certain position

def place_elem(panel, m, pos):
  
    x, y = m
    N = len(panel)
    if x < 0 or x >= N or y < 0 or y >= N:
        return None
    panel[x][y] = pos
    return True


# In order to swap two elements in different position m1 and m2

def swap(panel, m1, m2):
 
    a1, m1 = m1
    x2, y2 = m2
    panel[a1][m1], panel[x2][y2] = panel[x2][y2], panel[a1][m1]



# Simply in order to clear the console

def clear():
   
    import os
    b = os.system("clear")


# To simulate the key pfinalsed on the keyboard

def pressed_key():
   
    import tty
    import sys
    import termios

    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)

    x = 0

    if x != chr(27):
        x = sys.stdin.read(1)[0]


    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    return x



def init_two(panel):
  
    N = len(panel)

    a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
    times = 0

    while times < 10 and panel[a1][m1] != '#':
        a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
        times += 1

    if panel[a1][m1] == '#':
        panel[a1][m1] = 2

    times = 0

    a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
    while times < 3 and panel[a1][m1] != '#':
        a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
        times += 1

    if panel[a1][m1] == '#':
        panel[a1][m1] = 4


# In order to place number 2 on the panel

def two_placer(panel):
  
    N = len(panel)
    number_2_generator = random.randint(0,10)

    if number_2_generator < 9:
        a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
        times = 0
        while times < 10 and panel[a1][m1] != '#':
            a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
            times += 1

        if panel[a1][m1] == '#':
            panel[a1][m1] = 2

    number_4_generator = random.randint(0, 10)

    if number_4_generator < 1:
        times = 0
        a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
        while times < 3 and panel[a1][m1] != '#':
            a1, m1 = random.randint(0,N-1), random.randint(0,N-1)
            times += 1

        if panel[a1][m1] == '#':
            panel[a1][m1] = 4


# add two same numbers in panel

def simple_adder(panel):

    not_filled_cell = get_not_filled_cell(panel)
    if len(not_filled_cell) == 0:
        print("no empty cells, return")
        return

    rows, columns = not_filled_cell[random.randint(0, len(not_filled_cell)-1)]
    p = random.randint(0,99)
    if p < 90:
        panel[rows][columns] = 2
    else:
        panel[rows][columns] = 4


# count the number of tiles to make the panel full

def tile_count(panel):
 
    N = len(panel)

    final = {}

    for a in range(N):
        for m in range(N):
            if panel[a][m] in final:
                final[panel[a][m]] += 1
            else:
                final[panel[a][m]] = 1

    return final


def star_replacer(panel):
    N = len(panel)
    new_panel = cp.deepcopy(panel)
    for a in range(N):
        for m in range(N):
            if new_panel[a][m] =="#":
                new_panel[a][m] = 0
    return new_panel