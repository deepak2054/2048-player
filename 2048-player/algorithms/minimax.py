# ACKNOWLEDGEMENT:
# The idea of implementation comes from the following courses, codes and answers:
# https://www.youtube.com/watch?v=STjW3eH0Cik&t=2128s
# https://github.com/ss4936/2048
# https://github.com/ovolve/2048-AI/tree/master/js
# https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048/22389702#22389702

import sys
sys.path.append(sys.path[0]+'/../')
from core.evaluate_function import MinimaxEvaluator
import numpy as np
import copy as cp
import math
from core.logic import move, check_gameOver, move, add_upElements_v2
from core.utils import actions, get_not_filled_cell

class Minimax:
    def __init__(self, board = None, max_depth = 4):
        self.board = board
        self.max_depth = max_depth
        self.ACTIONS = actions

    def evaluate(self, board):
        '''
        An function used for  evaluation
        '''
        me = MinimaxEvaluator(board)
        emptyCounts = me.empty_cells()
        ssmoothWeights = 0.1
        monoWeights = 1.0
        emptyWeights = 2.7
        maxWeights = 1.0
        smooth = me.smoothness()*ssmoothWeights
        mono = me.monotonicity() * monoWeights
        # When no empty cells the while loop should terminate.
        # So no need to consider it here.
        if(emptyCounts == 0):
            emp = -np.inf
        else:
            emp = math.log(emptyCounts, 2) * emptyWeights
        maxwgt = me.maximum_value() * maxWeights
        return smooth + mono + emp + maxwgt

    def basicMove(self):
        '''
        This function return direction which is calculated by  using a basic or a  nonpruning algorithm
        :returns: a  string indicating direction
        '''
        bestMove = None
        maxValue = -np.inf
        # currently is max player. Facing on 4 directions, you iterate, compare the heuristic,
        # choose the best direction to go.
        for action in self.ACTIONS:
            # bestValue = -np.inf
            boardCopy = cp.deepcopy(self.board)
            if move(boardCopy, action):
                move(boardCopy, action)
                add_upElements_v2(boardCopy,action)
                move(boardCopy, action)
                bestValue = self.basicRun(boardCopy, self.max_depth, False)
            # if action == "RIGHT" or action == "DOWN":
            #     bestValue += 500
                if bestValue > maxValue:
                    maxValue = bestValue
                    bestMove = action
        if bestMove == None:
            # raise ValueError("The best move is None! Check minimax algorithm.")
            return self.ACTIONS[np.random.randint(0,3)]
        return bestMove

    def basicRun(self, board, max_depth, is_max):
        if (max_depth == 0) or check_gameOver(board):
            return self.evaluate(board)
        if is_max:
            bestValue = -np.inf
            children = []
            for action in self.ACTIONS:
                boardCopy = cp.deepcopy(board)
                if move(boardCopy, action):
                    move(boardCopy, action)
                    add_upElements_v2(boardCopy, action)
                    move(boardCopy, action)
                    children.append(boardCopy)
            for child in children:
                bestValue = max(bestValue, self.basicRun(child, max_depth - 1, False))

            return bestValue
        else:
            bestValue = np.inf
            children = []
            empty_cells = get_not_filled_cell(board)
            for cell in empty_cells:
                boardCopy = cp.deepcopy(board)
                boardCopy[cell[0]][cell[1]] = 2
                children.append(boardCopy)
                boardCopy = cp.deepcopy(board)
                boardCopy[cell[0]][cell[1]] = 4
                children.append(boardCopy)
            for child in children:
                bestValue = min(bestValue, self.basicRun(child, max_depth - 1, True))
            return bestValue




    def alphabeta_move(self):
        '''
        This function return direction calculate by a alpha-beta pruning algorithm
        :return: a direction string
        '''
        bestMove = None
        maxValue = -np.inf
        # currently is max player. Facing on 4 directions, you iterate, compare the heuristic,
        # choose the best direction to go.
        for action in self.ACTIONS:
            bestValue = -np.inf
            boardCopy = cp.deepcopy(self.board)
            if move(boardCopy, action):
                move(boardCopy, action)
                add_upElements_v2(boardCopy,action)
                move(boardCopy,action)
                bestValue = self.alphabeta_run(boardCopy, self.max_depth, -np.inf, np.inf, False)
            # if action == "RIGHT" or action == "DOWN":
            #     bestValue += 500
            if bestValue >= maxValue:
                maxValue = bestValue
                bestMove = action
            print(bestValue)
        if bestMove == None:
            raise ValueError("The best move is None! Check minimax algorithm.")
        return bestMove

    def alphabeta_run(self, board, max_depth, alpha, beta, is_max):
        if max_depth == 0:
            return self.evaluate(board)
        if not check_gameOver(board):
            return self.evaluate(board)

        if is_max:
            bestValue = -np.inf
            children = []
            for action in self.ACTIONS:
                boardCopy = cp.deepcopy(board)
                if move(boardCopy, action):
                    move(boardCopy, action)
                    add_upElements_v2(boardCopy, action)
                    move(boardCopy, action)
                    children.append(boardCopy)
            for child in children:
                bestValue = max(bestValue, self.alphabeta_run(child, max_depth - 1, alpha, beta, False))
                if bestValue >= beta:
                    return bestValue
                alpha = max(alpha, bestValue)
            return bestValue
        else:
            bestValue = np.inf
            children = []
            empty_cells = get_not_filled_cell(board)
            for cell in empty_cells:
                boardCopy = cp.deepcopy(board)
                boardCopy[cell[0]][cell[1]] = 2
                children.append(boardCopy)
                boardCopy = cp.deepcopy(board)
                boardCopy[cell[0]][cell[1]] = 4
                children.append(boardCopy)
            for child in children:
                bestValue = min(bestValue, self.alphabeta_run(child, max_depth - 1, alpha, beta, True))
                if bestValue <= alpha:
                    return bestValue
                beta = min(beta, bestValue)
            return bestValue

x=Minimax()
x.basicMove()