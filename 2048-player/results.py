# Run in backend to test performance for different algorithms
# we measure a panel using maximum score, and total score, and lasting moves

from algorithms.MCTS import random_move_naive
from algorithms.expectimax import expecti_max_main
from algorithms.minimax import Minimax

from core.utils import *
from core.logic import *
import copy

# sample results output
# 'monte_carlo_simulation'
# simulates XX steps for each move
# {'max_tile':occur_times}
# {max scores}
# {'total_score': occur_times}
# average_moves to end of game


def get_results_mcts(which_algorithm = 'mcts', test_times = 5, sim_moves = (50,100,200,400,800)):

    res_all = []
    res_single = []

    total_score = {}

    max_total_scores = {}
    for sim_move in sim_moves:

        max_tiles = {}
        max_total_score = 0
        average_moves = 0
        for i in range(test_times):
            panel = generate_panel(4)
            init_two(panel)
            curr_score = 0
            number_of_moves = 0
            panel_info = {}

            while not check_gameOver(panel):
                action, successpanels = random_move_naive(panel, curr_score, no_of_test_moves=sim_move)
                if check_move_possible(panel, action):
                    number_of_moves += 1

                    move(panel, action)
                    curr_score += add_upElements_v2(panel, action)
                    move(panel, action)
                    simple_adder(panel)

            max_tile = get_max_no_cells(panel)
            tile_counts = tile_count(panel)

            panel_info['movements'] = number_of_moves
            panel_info['score'] = curr_score
            panel_info['max_tile'] = max_tile
            panel_info['depth'] = sim_move
            panel_info['tile_count'] = tile_counts
            res_single.append(panel_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1

            if max_total_score < curr_score:
                max_total_score = curr_score

            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration when number of test simulation is {}".format(i, sim_move))

        max_total_scores[sim_move] = max_total_score

        res_all.append(which_algorithm + ' with sim_move {}'.format(sim_move))
        res_all.append(max_tiles)
        # res_all.append(total_score)
        # res_all.append(max_total_scores)
        res_all.append('Max_score is {}'.format(max_total_score))
        res_all.append('average_moves_till_end: {}'.format(average_moves/test_times))
        res_all.append('\n')

    res_all.append(max_total_scores)
    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(sim_moves)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(sim_moves)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single

def get_results_expectimax(which_algorithm = 'expectimax', test_times = 20, max_depth=(1,2)):
    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    res_all = []
    res_single = []

    total_score = {}


    for depth in max_depth:

        max_total_score = 0
        max_tiles = {}
        average_moves = 0
        for i in range(test_times):
            panel = generate_panel(4)
            init_two(panel)
            curr_score = 0
            number_of_moves = 0
            panel_info = {}

            # depth = 1

            while not check_gameOver(panel):
                best_move = None
                best_val = -1

                for direction in moves:
                    if not check_move_possible(panel, direction):
                            # clear()
                        continue

                    temp_panel = copy.deepcopy(panel)
                    move(temp_panel, direction)
                    add_upElements(temp_panel, direction, 0)
                    move(temp_panel, direction)

                    alpha = expecti_max_main(temp_panel, depth)
                    if best_val < alpha:
                        best_val = alpha
                        best_move = direction

                number_of_moves += 1
                move(panel, best_move)
                curr_score += add_upElements_v2(panel, best_move)
                move(panel, best_move)
                simple_adder(panel)

            max_tile = get_max_no_cells(panel)
            tile_counts = tile_count(panel)

            panel_info['movements'] = number_of_moves
            panel_info['score'] = curr_score
            panel_info['max_tile'] = max_tile
            panel_info['depth'] = depth
            panel_info['tile_count'] = tile_counts
            res_single.append(panel_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
            if max_total_score < curr_score:
                max_total_score = curr_score
            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration in depth {}".format(i, depth))

        res_all.append(which_algorithm + ' with depth {}'.format(depth))
        res_all.append(max_tiles)
        res_all.append('max score for this depth is {}'.format(max_total_score))
    # res_all.append(total_score)
        res_all.append('average_moves_till_end: {}'.format(average_moves/test_times))
        res_all.append('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single

def get_results_minimax(which_algorithm='minimax', test_times=20, max_depth = (1,2,3,4)):

    res_all = []
    res_single = []

    total_score = {}


    for depth in max_depth:

        max_tiles = {}
        average_moves = 0
        max_total_score = 0

        for i in range(test_times):
            panel = generate_panel(4)
            init_two(panel)
            curr_score = 0
            number_of_moves = 0
            panel_info = {}

            player = Minimax(panel, depth)

            while not check_gameOver(panel):
                best_move = player.basicMove()
                if check_move_possible(panel, best_move):
                    number_of_moves += 1
                    move(panel,best_move)
                    curr_score += add_upElements_v2(panel,best_move)
                    move(panel,best_move)
                    simple_adder(panel)

            max_tile = get_max_no_cells(panel)
            tile_counts = tile_count(panel)

            panel_info['movements'] = number_of_moves
            panel_info['score'] = curr_score
            panel_info['max_tile'] = max_tile
            panel_info['depth'] = depth
            panel_info['tile_count'] = tile_counts
            res_single.append(panel_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
            if max_total_score < curr_score:
                max_total_score = curr_score
            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration in depth {}".format(i, depth))

        res_all.append(which_algorithm + ' with depth {}'.format(depth))
        res_all.append(max_tiles)
        res_all.append('max score for this depth is {}'.format(max_total_score))
        res_all.append('average_moves_till_end: {}'.format(average_moves / test_times))
        res_all.append('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single



def get_results_minimax_pruning(which_algorithm='minimax_pruning', test_times=20, max_depth = (1,2,3,4)):

    res_all = []
    res_single = []

    total_score = {}


    for depth in max_depth:

        max_tiles = {}
        average_moves = 0
        max_total_score = 0

        for i in range(test_times):
            panel = generate_panel(4)
            init_two(panel)
            curr_score = 0
            number_of_moves = 0
            panel_info = {}

            player = Minimax(panel, depth)

            while not check_gameOver(panel):
                best_move = player.alphabeta_move()
                if check_move_possible(panel, best_move):
                    number_of_moves += 1
                    move(panel,best_move)
                    curr_score += add_upElements_v2(panel,best_move)
                    move(panel,best_move)
                    simple_adder(panel)

            max_tile = get_max_no_cells(panel)
            tile_counts = tile_count(panel)

            panel_info['movements'] = number_of_moves
            panel_info['score'] = curr_score
            panel_info['max_tile'] = max_tile
            panel_info['depth'] = depth
            panel_info['tile_count'] = tile_counts
            res_single.append(panel_info)

            if max_tile not in max_tiles:
                max_tiles[max_tile] = 1
            else:
                max_tiles[max_tile] += 1
            if curr_score not in total_score:
                total_score[curr_score] = 1
            else:
                total_score[curr_score] += 1
            if max_total_score < curr_score:
                max_total_score = curr_score
            average_moves += number_of_moves

            # debug output
            print("Finish {} iteration in depth {}".format(i, depth))

        res_all.append(which_algorithm + ' with depth {}'.format(depth))
        res_all.append(max_tiles)
        res_all.append('max score for this depth is {}'.format(max_total_score))
        res_all.append('average_moves_till_end: {}'.format(average_moves / test_times))
        res_all.append('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'total_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_all:
            out.write(str(e))
            out.write('\n')

    with open('results_{}_{}_{}.txt'.format(which_algorithm, 'single_count', str(max_depth)), mode='wt', encoding='utf-8') as out:
        for e in res_single:
            out.write(str(e))
            out.write('\n')

    return res_all, res_single


## For each element, we generate a dictionary.
#{"movements: 1111,
#  "score": 111,
# "max_tile": 2048,
#  "depth": 2}

def get_mcts():
    get_results_mcts(sim_moves=(50,100,200,400),test_times=20)

def get_expectimax():
    get_results_expectimax(test_times=100,max_depth=(1,2))

def get_minimax():
    get_results_minimax(test_times=100, max_depth=(1,2))
    get_results_minimax(test_times=50, max_depth=(3,4))

def get_minimax_pruning():
    get_results_minimax_pruning(test_times=100, max_depth=(1,2,3,4,5))
    get_results_minimax_pruning(test_times=50, max_depth=(6,7,8))
