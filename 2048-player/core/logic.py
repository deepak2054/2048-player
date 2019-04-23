# The logic for the '2048' game 

# How to play: Use your arrow keys to move the tiles. 
# When two tiles with the same number touch, they merge into one
# And again move them


# Importing all the utilties


# from core.utils import *
from util_dupli import *

# For moving up and other directions
def go_up(panel):
  
    pass

def go_down(panel):
    pass

def go_left(panel):
    pass

def go_right(panel):
    pass


# The panel has to move to represent the operation

def move(panel, operation):
   
    N = len(panel)
    if operation == "UP":
        for column in range(0,N):
            empty_atFirst = 0
            for m in range(0,N):
                if panel[m][column] != '#':
                    swap(panel, (m, column), (empty_atFirst, column))
                    empty_atFirst += 1
    
    if operation == "DOWN":
        for column in range(0,N):
            empty_atFirst = N-1
            for m in range(0,N):
                if panel[N-1-m][column] != '#':
                    swap(panel, (N-1-m, column), (empty_atFirst, column))
                    empty_atFirst -= 1

    if operation == "LEFT":
        for row in range(0,N):
            empty_atFirst = 0
            for m in range(0, N):
                if panel[row][m] != '#':
                    swap(panel, (row, m), (row, empty_atFirst))
                    empty_atFirst += 1
    
    if operation == "RIGHT":
        for row in range(0,N):
            empty_atFirst = N-1
            for m in range(0, N):
                if panel[row][N-1-m] != '#':
                    swap(panel, (row, N-1-m), (row, empty_atFirst))
                    empty_atFirst -= 1


def add_upElements(panel, operation, score_now):
  
    score_new = score_now
    N = len(panel)
    if operation == "UP":
        for column in range(0,N):
            for m in range(0, N-1):
                if panel[m][column] == panel[m+1][column] and panel[m][column] != '#':
                    score_new += 2 * panel[m][column]
                    panel[m][column] = panel[m][column] + panel[m+1][column]
                    panel[m+1][column] = '#'

    if operation == "DOWN":
        for column in range(0,N):
            m = N-1
            while m > 0:
                if panel[m][column] == panel[m-1][column] and panel[m][column] != '#':
                    score_new += 2 * panel[m][column]
                    panel[m][column] = panel[m][column] + panel[m-1][column]
                    panel[m-1][column] = '#'
                m -= 1

    if operation == "LEFT":
        for row in range(0, N):
            for m in range(0, N-1):
                if panel[row][m] == panel[row][m+1] and panel[row][m] != '#':
                    score_new += 2 * panel[row][m]
                    panel[row][m] = panel[row][m] + panel[row][m+1]
                    panel[row][m+1] = '#'

    if operation == "RIGHT":
        for row in range(0,N):
            m = N-1
            while m>0:
                if panel[row][m] == panel[row][m-1] and panel[row][m] != '#':
                    score_new += 2 * panel[row][m]
                    panel[row][m] = panel[row][m] + panel[row][m-1]
                    panel[row][m-1] = '#'
                m -= 1

    return score_new

# After the end of each move we add the elements to the new updated one


def add_upElements_v2(panel, operation):
     
    score_added = 0
    N = len(panel)
    if operation == "UP":
        for column in range(0,N):
            for m in range(0, N-1):
                if panel[m][column] == panel[m+1][column] and panel[m][column] != '#':
                    score_added += 2 * panel[m][column]
                    panel[m][column] = panel[m][column] + panel[m+1][column]
                    panel[m+1][column] = '#'

    if operation == "DOWN":
        for column in range(0,N):
            m = N-1
            while m>0:
                if panel[m][column] == panel[m-1][column] and panel[m][column] != '#':
                    score_added += 2 * panel[m][column]
                    panel[m][column] = panel[m][column] + panel[m-1][column]
                    panel[m-1][column] = '#'
                m -= 1

    if operation == "LEFT":
        for row in range(0, N):
            for m in range(0, N-1):
                if panel[row][m] == panel[row][m+1] and panel[row][m] != '#':
                    score_added += 2 * panel[row][m]
                    panel[row][m] = panel[row][m] + panel[row][m+1]
                    panel[row][m+1] = '#'

    if operation == "RIGHT":
        for row in range(0,N):
            m = N-1
            while m>0:
                if panel[row][m] == panel[row][m-1] and panel[row][m] != '#':
                    score_added += 2 * panel[row][m]
                    panel[row][m] = panel[row][m] + panel[row][m-1]
                    panel[row][m-1] = '#'
                m -= 1

    return score_added


# To check if the move is possible

def check_move_possible(panel, operation):
   
    N = len(panel)
    if operation == "UP":
        for column in range(0,N):
            m=0
            while m < N and panel[m][column] != '#':
                m += 1
            for o in range(m + 1, N):
                if panel[o][column] != None and panel[o][column] != '#':
                    return True

        for column in range(0, N):
            for m in range(0, N-1):
                if panel[m][column] == panel[m+1][column] and panel[m][column] != '#':
                    return True
    
    if operation == "DOWN":
        for column in range(0, N):
            m = N-1
            while m >= 0 and panel[m][column] != '#':
                m -= 1
            for o in range(0,m):    
                if panel[o][column] != None and panel[o][column] != '#':
                    return True
        
        for column in range(0, N):
            m = N-1
            while m>0:
                if panel[m][column] == panel[m-1][column] and panel[m][column] != '#':
                    return True
                m -= 1
        
    
    if operation == "LEFT":
        for row in range(0,N):
            m=0
            while m < N and panel[row][m] != '#':
                m += 1
            for o in range(m+1,N):
                if panel[row][o] != None and panel[row][o] != '#':
                    return True
        
        for row in range(0, N):
            for m in range(0,N-1):
                if panel[row][m] == panel[row][m+1] and panel[row][m] != '#':
                    return True

    if operation == "RIGHT":
        for row in range(0,N):
            m = N-1
            while m >= 0 and panel[row][m] != '#':
                m -= 1
            for k in range(0, m):
                if panel[row][m] != None and panel[row][k] != '#':
                    return True

        for row in range(0, N):
            m = N-1
            while m>0:
                if panel[row][m] == panel[row][m-1] and panel[row][m] != '#':
                    return True
                m -= 1

    return False