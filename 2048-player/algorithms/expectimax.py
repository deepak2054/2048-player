import copy
import numpy as np
import sys
sys.path.append(sys.path[0]+'/../')
from core.logic import *
from core.utils import *

possible_moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')
probability = {0: 0, 2: 0.9, 4: 0.1}


#this function  evaluates the current score within  the panel

def evaluate_current_score(panel):
    '''
    Evaluates the current score within the panel
    '''
    N = len(panel)
    matrix_calculate = [[1 for a in range(N)] for a in range(N)]
    matrix_calculate = np.array(matrix_calculate)

    matrix_calculate[0][0] = 2 ** 15
    matrix_calculate[0][1] = 2 ** 14
    matrix_calculate[0][2] = 2 ** 13
    matrix_calculate[0][3] = 2 ** 12

    matrix_calculate[1][0] = 2 ** 8
    matrix_calculate[1][1] = 2 ** 9
    matrix_calculate[1][2] = 2 ** 10
    matrix_calculate[1][3] = 2 ** 11

    matrix_calculate[2][0] = 2 ** 7
    matrix_calculate[2][1] = 2 ** 6
    matrix_calculate[2][2] = 2 ** 5
    matrix_calculate[2][3] = 2 ** 4

    matrix_calculate[3][0] = 2 ** 0
    matrix_calculate[3][1] = 2 ** 1
    matrix_calculate[3][2] = 2 ** 2
    matrix_calculate[3][3] = 2 ** 3

  

    score = 0
    for a in range(N):
        for m in range(N):
            if panel[a][m] != '#':
                score += panel[a][m] * matrix_calculate[a][m]

    return score


def expecti_max_main(panel, depth):
    total_score = 0
    total_probability = 0
    if depth == 0:
        return evaluate_current_score(panel)

    else:
        for empty in get_not_filled_cell(panel):
            best_score = 0
            best_move = None

           # Generating new numbers in the panel


            new_panel = copy.deepcopy(panel)
            row, column = empty
            z = random.randint(0, 99)
            #new_number = 0
            if z < 90:
                new_number = 2
            else:
                new_number = 4

            new_panel[row][column] = new_number

            for directions in possible_moves:
                if not check_move_possible(panel, directions):
                    continue

                #move new panel in direction
                temporary_panel = copy.deepcopy(new_panel)
                move(temporary_panel, directions)
                add_upElements(temporary_panel, directions, 0)
                move(temporary_panel, directions)
                score = expecti_max_main(temporary_panel, depth - 1)

                if score > best_score:
                    best_score = score
                    best_move = directions

            if best_move != None:
                total_score += probability[new_number] * best_score
            else:
                total_score += probability[new_number] * evaluate_current_score(temporary_panel)
            total_probability += probability[new_number]

        if total_probability == 0:
            return total_score

        return total_score / total_probability


def run_expecti_max_main():
    panel = generate_panel(4)
    init_two(panel)
    print_panel(panel)

    total_possible_moves = 0
    depth = 1

    while not check_gameOver(panel):
        best_move = None
        best_value = -1

        for direction in possible_moves:
            if not check_move_possible(panel, direction):
                #clear()
                continue

            temporary_panel = copy.deepcopy(panel)
            move(temporary_panel, direction)
            add_upElements(temporary_panel, direction, 0)
            move(temporary_panel, direction)

            gamma = expecti_max_main(temporary_panel, depth)
            if best_value < gamma:
                best_value = gamma
                best_move = direction

        move(panel, best_move)
        add_upElements(panel, best_move, 0)
        move(panel, best_move)
        total_possible_moves += 1
        clear()
        print_panel(panel)
        simple_adder(panel)


if __name__ == "__main__":
    run_expecti_max_main()
