# different kinds of evaluations
# May be used in different heuristic functions

import math
import copy
from logic import add_upElements
from utils import get_not_filled_cell

class Evaluator:
    def __init__(self, panel):
        self.panel = panel


    # The number of empty cells remaining in the panel

    def empty_cells(self, new_panel):
       
        N = len(new_panel)

        count_var = 0
        for a in range(N):
            for m   in range(N):
                if new_panel[a][m] == '#':
                    count_var += 1
        return count_var

    def mergingCells_max(self):
        moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')
        emptyCells_before = self.empty_cells(self.panel)
        maximum_merged = 0
        for move in moves:
            new_panel = copy.deepcopy(self.panel)
            add_upElements(new_panel, move, 0)
            empty_cells_after_merge = self.empty_cells(new_panel)
            merge = empty_cells_after_merge - emptyCells_before
            if merge > maximum_merged:
                maximum_merged = merge

        return maximum_merged

    def decrement(self):
        count_var_pair = 0
        new_panel = copy.deepcopy(self.panel)
        empty = get_not_filled_cell(new_panel)
        for index in empty:
            new_panel[index[0]][index[1]] = 0

        for a in range(len(new_panel[0]) - 1):
            if new_panel[0][a] > new_panel[0][a+1]:
                count_var_pair += 1
            if new_panel[2][a] > new_panel[2][a+1]:
                count_var_pair += 1

        for a in range(len(new_panel[0]) - 1):
            if new_panel[1][a] < new_panel[1][a+1]:
                count_var_pair += 1
            if new_panel[3][a] < new_panel[3][a+1]:
                count_var_pair += 1

        if new_panel[0][3] > new_panel[1][3]:
            count_var_pair += 1

        if new_panel[1][0] > new_panel[2][0]:
            count_var_pair += 1

        if new_panel[2][3] > new_panel[3][3]:
            count_var_pair += 1

        return count_var_pair

class MinimaxEvaluator(Evaluator):
    def __init__(self, panel):
        Evaluator.__init__(self, panel)


    #  the function smoothness is difference between the neighbouring tiles.

    def smoothness(self):

        N = len(self.panel)
        result = 0
        for a in range(N):
            for m   in range(N):
                if self.panel[a][m] != '#':
                    curr_value = math.log(self.panel[a][m],2)
                    for direction in ('RIGHT', 'DOWN'):
                        theNext_cell = self.get_first_non_empty_cell(i,j, direction)
                        if theNext_cell != None:
                            x, y = theNext_cell
                            theNext_numValue = math.log(self.panel[x][y],2)
                            result -= abs(curr_value - theNext_numValue)
        return result

    # How monotonous is the panel?
    def monotonicity(self):
       

        N = len(self.panel)

        score = [0,0,0,0]

        # For vertical direction 'UP' and 'DOWN'

        for row in range(N):
            current_cell = 0
            while current_cell < N and self.panel[row][current_cell] == '#':
                current_cell += 1
            nextCell = current_cell + 1
            while nextCell < N:
                while nextCell < N and self.panel[row][nextCell] == '#':
                    nextCell += 1

                if nextCell < N:
                    if self.panel[row][current_cell] > self.panel[row][nextCell]:
                        score[0] += self.panel[row][nextCell] - self.panel[row][current_cell]
                    elif self.panel[row][current_cell] < self.panel[row][nextCell]:
                        score[1] += self.panel[row][current_cell] - self.panel[row][nextCell]

                current_cell = nextCell
                nextCell += 1

        # left/right direction
        for column in range(N):
            current_cell = 0
            while current_cell < N and self.panel[current_cell][column] == '#':
                current_cell += 1
            nextCell = current_cell + 1
            while nextCell < N:
                while nextCell < N and self.panel[nextCell][column] == '#':
                    nextCell += 1

                if nextCell < N:
                    if self.panel[current_cell][column] > self.panel[nextCell][column]:
                        score[2] += self.panel[nextCell][column] - self.panel[current_cell][column]
                    elif self.panel[current_cell][column] < self.panel[nextCell][column]:
                        score[3] += self.panel[current_cell][column] - self.panel[nextCell][column]

                current_cell = nextCell
                nextCell += 1

        return max(score[0], score[1]) + max(score[2],score[3])

    # Gives the number of empty cells

    def empty_cells(self):
    
        N = len(self.panel)

        count_var = 0
        for a in range(N):
            for m   in range(N):
                if self.panel[a][m] == '#':
                    count_var += 1
        return count_var


# Finds the maximum value of the panel
    def maximum_value(self):
     
        N = len(self.panel)
        result = 0
        for a in range(N):
            for m   in range(N):
                if self.panel[a][m] != '#' and self.panel[a][m] > result:
                    result = self.panel[a][m]

        return result



    # Gets the first non - empty cell 

    def get_first_non_empty_cell(self, row, column, direction='RIGHT'):
        
        N = len(self.panel)

        if direction.upper() == 'RIGHT':
            # find in the same row:
            for  o in range(column, N):
                if self.panel[row][o] != '#':
                    return row, o

        elif direction.upper() == 'DOWN':
            # find in the same column
            for  o in range(row, N):
                if self.panel[o][column] != '#':
                    return o, column

        return None