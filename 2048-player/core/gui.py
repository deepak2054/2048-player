# The code mainly comes from https://github.com/yangshun/2048-python/blob/master/puzzle.py
import copy
import threading
import numpy as np
import time
from random import *
from tkinter import *
from sys import platform
import sys
sys.path.append(sys.path[0]+'/../')
from algorithms.MCTS import random_move_naive
from algorithms.expectimax import expecti_max_main
from algorithms.minimax import Minimax
from core.utils import *
from core.logic import *


SIZE = 500
GRID_LEN = 4
GRID_PADDING = 8

BACKGROUND_columnOR_GAME = "#92877d"
BACKGROUND_columnOR_CELL_EMPTY = "#9e948a"
BACKGROUND_columnOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e", 4096:"#edc22e", 8192:"#eff9c5",16384:"#11f29c"}
CELL_columnOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2",
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2", 4096: "#f9f53e", 8192:"#f9f6f3",16384:"#f9f6f3"}
FONT = ("Verdana", 20, "bold")

MOVES = ('UP', 'DOWN', 'LEFT', 'RIGHT')

class Game(Frame):
    def __init__(self, mode=True, define_AI = 'MINIMAX'):
        Frame.__init__(self)
        self.actions = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                         'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}
        self.grid()
        self.master.title('2048 Player - CS534 Final Project')
        self.master.bind("<Key>", self.keyDown)
        self.grid_cells = []
        self.matrices()
        self.grids()
        self.scores()
        self.updateScores()
        self.UpdateGridCells()

        if mode:
            print('inside mode')
            if platform == 'win32' or platform == 'cygwin':
                class clippanelthread(threading.Thread):
                    def __init__(self):
                        threading.Thread.__init__(self)

                    def run(self):
                        clippanelcheck()

                def clippanelcheck():
                    if define_AI.upper() == 'EXPECTIMAX':
                        self.expectimax_AI_run()
                    elif define_AI.upper() == 'MCTS':
                        self.mcts_AI_run()
                    elif define_AI.upper() == "MINIMAX":
                        self.Ai_minimax_run()
                    elif define_AI.upper() == "MINIMAX_PRUNING":
                        self.Ai_minimax_pruning_run()
                clippanelthread.daemon = True

                clippanelthread().start()
            else:
                if define_AI.upper() == 'EXPECTIMAX':
                    self.expectimax_AI_run()
                elif define_AI.upper() == 'MCTS':
                    self.mcts_AI_run()
                elif define_AI.upper() == "MINIMAX":
                    self.Ai_minimax_run()
                elif define_AI.upper() == "MINIMAX_PRUNING":
                    self.Ai_minimax_pruning_run()
        self.mainloop()

    def scores(self):
        footer_label = Frame(self.background, bg=BACKGROUND_columnOR_CELL_EMPTY, width=SIZE/2, height=50)
        footer_label.grid(row = GRID_LEN, columnumn = 0, columnumnspan = 2, padx=GRID_PADDING, pady=GRID_PADDING)
        title_cell = Label(master=footer_label, text="Score:", bg=BACKGROUND_columnOR_DICT[2], justify=CENTER, font=FONT, width=10,
                  height=2)
        title_cell.grid()
        footer_score = Frame(self.background, bg=BACKGROUND_columnOR_CELL_EMPTY, width=SIZE/2, height=50)
        footer_score.grid(row = GRID_LEN, columnumn = 2, columnumnspan = 2, padx=GRID_PADDING, pady=GRID_PADDING)
        self.score_cell = Label(master=footer_score, text=self.score, bg=BACKGROUND_columnOR_DICT[2], justify=CENTER, font=FONT, width=10,
                  height=2)
        self.score_cell.grid()


    def grids(self):
        self.background = Frame(self, bg=BACKGROUND_columnOR_GAME, width=SIZE, height=SIZE+50)
        self.background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(self.background, bg=BACKGROUND_columnOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, columnumn=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_columnOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def generate(self):
        return randint(0, GRID_LEN - 1)

    def matrices(self):
        self.matrix = generate_panel(4)
        init_two(self.matrix)
        self.score = 0

    def UpdateGridCells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == '*':
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_columnOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_columnOR_DICT[new_number],
                                                    fg=CELL_columnOR_DICT[new_number])
        self.update_idletasks()

    def updateScores(self):
        self.score_cell.configure(text=self.score)


    def keyDown(self, event):
        key = repr(event.char).replace("'", "")
        if key in self.actions:
            action = self.actions[key]
            if check_move_possible(self.matrix, action):
                move(self.matrix, action)
                self.score += add_upElements_v2(self.matrix, action)
                move(self.matrix, action)
                simple_adder(self.matrix)
                self.updateScores()
                self.UpdateGridCells()
                if check_gameOver(self.matrix):
                    self.grid_cells[1][1].configure(text="Game", bg=BACKGROUND_columnOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Over!", bg=BACKGROUND_columnOR_CELL_EMPTY)

    def generate_next(self):
        index = (self.generate(), self.generate())
        while self.matrix[index[0]][index[1]] != "*":
            index = (self.generate(), self.generate())
        self.matrix[index[0]][index[1]] = 2

    def mcts_AI_run(self):
        while not check_gameOver(self.matrix):
            action, successpanels = random_move_naive(self.matrix,self.score,30)
            if check_move_possible(self.matrix,action):
                move(self.matrix, action)
                self.score += add_upElements_v2(self.matrix, action)
                move(self.matrix, action)
                self.updateScores()
                self.UpdateGridCells()
                simple_adder(self.matrix)
                self.UpdateGridCells()
               

    def expectimax_AI_run(self):
        while not check_gameOver(self.matrix):

            depth = 2
            best_move = None
            best_val = -1

            for direction in MOVES:
                if not check_move_possible(self.matrix, direction):
                    # clear()
                    continue

                temp_panel = copy.deepcopy(self.matrix)
                move(temp_panel, direction)
                add_upElements(temp_panel, direction, 0)
                move(temp_panel, direction)

                alpha = expecti_max_main(temp_panel, depth)
                if best_val < alpha:
                    best_val = alpha
                    best_move = direction

            move(self.matrix,best_move)
            self.score += add_upElements_v2(self.matrix, best_move)
            move(self.matrix,best_move)
            self.updateScores()
            self.UpdateGridCells()
            simple_adder(self.matrix)
            self.UpdateGridCells()

    def Ai_minimax_run(self):
        while not check_gameOver(self.matrix):
            mm = Minimax(board= self.matrix, max_depth= 5)
            best_move = mm.basicMove()
            if check_move_possible(self.matrix, best_move):
                move(self.matrix, best_move)
                self.score +=add_upElements_v2(self.matrix, best_move)
                move(self.matrix, best_move)
                self.updateScores()
                self.UpdateGridCells()
                simple_adder(self.matrix)
                self.UpdateGridCells()
            

    def Ai_minimax_pruning_run(self):
        while not check_gameOver(self.matrix):
            mm = Minimax(board= self.matrix, max_depth= 4)
            best_move = mm.alphabeta_move()
            if check_move_possible(self.matrix, best_move):
                move(self.matrix, best_move)
                self.score +=add_upElements_v2(self.matrix, best_move)
                move(self.matrix, best_move)
                self.updateScores()
                self.UpdateGridCells()
                simple_adder(self.matrix)
                self.UpdateGridCells()
  
