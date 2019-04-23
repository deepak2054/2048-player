from sys import platform
from core.gui import Game
from core.logic import *
from core.utils import actions
import copy
from algorithms.expectimax import expecti_max_main


ACTIONS_MAP = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
           'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT','q':'EXIT','Q':"EXIT"}


def win32_press():
    import keypanel
    flag = True
    p = None
    while flag:
        try:
            for i in ACTIONS_MAP:
                if keypanel.is_pressed(i):
                    p = i
                    flag = False
                    break
            for i in ["q", "Q"]:
                if keypanel.is_pressed(i):
                    p = i
                    flag = False
                    break
        except:
            pass
    return p


def linux_press():
    p = pressed_key()
    while p not in ACTIONS_MAP:
        print("key press not recognized, please press wasd or WASD")
        p = pressed_key()
    return p


def run_console():
    panel = generate_panel(4)
    init_two(panel)
    print_panel(panel)
    curr_score = 0
    while not check_gameOver(panel):
        print("\ncurrent score is, ", curr_score)
        print("Possible actions: up, left, right, down, exit")
        print("Please press WASD for UP LEFT DOWN RIGHT Q for exit")

        if platform.startswith('linux') or platform == 'darwin':
            p = linux_press()
        elif platform == 'win32' or platform == 'cygwin':
            p = win32_press()
        else:
            p = win32_press()

        if p == 'q' or p == 'Q':
            break
        action = ACTIONS_MAP[p]
        action = action.upper()
        if action == "EXIT":
            break
       
        if check_move_possible(panel, action):
            move(panel, action)
            curr_score = add_upElements(panel, action, curr_score)
            # move(panel, action)
            clear()
            simple_adder(panel)
            print_panel(panel)
        else:
            clear()
            print_panel(panel)
    print("/nGame Over/nTo restart, Please type run_keypanel()")


def run_gui(algo):
    Game(mode=True, define_AI=algo)


def run(mode = "gui", algo = "expectimax"):
    if mode == "gui":
        run_gui(algo = algo)
    elif mode == "console":
        run_console()
    elif mode == "score":
 
        if algo == "expectimax":
            panel = generate_panel(4)
            init_two(panel)
            curr_score = 0
            while not check_gameOver(panel):
                depth = 2
                best_move = None
                best_val = -1

                for direction in actions:
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

                move(panel,best_move)
                curr_score += add_upElements_v2(panel, best_move)
                move(panel,best_move)
                simple_adder(panel)
            max_cell = get_max_no_cells(panel)
            return curr_score, max_cell
        else:
            raise ValueError("We dont have such a algorithm: {} .PLEASE TRY AGAIN".format(algo))

    else:
        raise ValueError("Unexpect Mode. Choose one from 'gui' or 'console'")


if __name__ == "__main__":
    run(mode = "console", algo = "expectimax")


