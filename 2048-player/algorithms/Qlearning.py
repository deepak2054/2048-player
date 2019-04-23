import copy
import numpy as np
import sys
sys.path.append(sys.path[0]+'/../')
from core.evaluate_function import *
from core.logic import *
from core.utils import *

def init():
    """
      initialies the board for the 2048 game
    """
    dec_pair = np.arange(16)
    empty_cells = np.arange(16)
    maxMerge = np.arange(9)

    states = []
    for i in dec_pair:
        for j in empty_cells:
            for k in maxMerge:
                states.append((i, j, k))

    # initial Q value 
    values = {}
    for state in states:
        values[state] = 0

    return values

def getQ(board, length, direction, Q, state2):
    """
       contains the discounted sum of a reward to  earn (average)
    """
    if length == 0:
        return 0

    p = 1/length
    gamma = 0.9
    reward = add_upElements(board, direction, 0)
    Q_value = p * (reward + gamma * Q[state2])
    return Q_value

def updateQval(board, length, direction, Q, state1, state2):
    Q[state1] = getQ(board, length, direction, Q, state2)

def getState(board):
    state_list = []
    evaluation = Evaluator(board)
    state_list.append(evaluation.decrement())
    state_list.append(evaluation.empty_cells(board))
    state_list.append(evaluation.mergingCells_max())
    state = tuple(state_list)

    return state

moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')
def train(Q):
    #initialize game
    board = generate_panel(4)
    init_two(board)
    score = 0

    while not check_gameOver(board):
        actions = []
        next_move = None
        max_Q =  float('-inf')
        number_of_moves = 0
        old_state = getState(board)

        #get all availabe action
        for direction in moves:
            if check_move_possible(board, direction):
                actions.append(direction)
        #find the policy to Q
        for direction in actions:
            tmp_board = copy.deepcopy(board)
            move(tmp_board, direction)
            add_upElements(tmp_board, direction, 0)
            move(tmp_board, direction)
            new_state = getState(board)
            Q_value = getQ(tmp_board, len(actions), direction, Q, new_state)
            if Q_value >= max_Q:
                max_Q = Q_value
                next_move = direction

        #update Q value
        move(board, next_move)
        add_upElements(board, next_move, 0)
        move(board, next_move)
        new_state = getState(board)
        updateQval(board, len(actions), next_move, Q, old_state, new_state)
        number_of_moves += 1
        simple_adder(board)


def testing(Q):
    # initializing games
    board = generate_panel(4)
    init_two(board)
    number_of_moves = 0
    score = 0

    while not check_gameOver(board):
        actions = []
        next_move = None
        max_Q = float('-inf')
        old_state = getState(board)

        # get all available actions 
        for direction in moves:
            if check_move_possible(board, direction):
                actions.append(direction)
        # find the policy to Q
        for direction in actions:
            tmp_board = copy.deepcopy(board)
            move(tmp_board, direction)
            add_upElements(tmp_board, direction, 0)
            move(tmp_board, direction)
            new_state = getState(board)
            Q_value = getQ(tmp_board, len(actions), direction, Q, new_state)
            if Q_value >= max_Q:
                max_Q = Q_value
                next_move = direction

        # update Q value
        # print('before',board)
        move(board, next_move)
        number_of_moves += 1
        add_upElements(board, next_move, 0)
        move(board, next_move)
        # print('after', board)
        new_state = getState(board)
        updateQval(board, len(actions), next_move, Q, old_state, new_state)
        simple_adder(board)

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != '*':
                score += board[i][j]

    return get_max_no_cells(board), number_of_moves, score, tile_count(board)

def run():
    Q = init()
    iteration = 30

    while(iteration > 0):
        train(Q)
        iteration -= 1

    #testing by using current Q
    return testing(Q)


if __name__ == "__main__":
    result = []
    for i in range(20):
        stats = {}
        max_cell, total_moves, score, tiles = run()
        stats['movements'] = total_moves
        stats['score'] = score
        stats['max_tile'] = max_cell
        stats['depth'] = 0
        stats['tile_count'] = tiles
        result.append(stats)
        print(stats)

    print(result)