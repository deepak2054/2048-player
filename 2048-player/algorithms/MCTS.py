import copy



# Importing all the utilties
import sys
sys.path.append(sys.path[0]+'/../')
from core.logic import *

# Importing all the logics 

from core.utils import *



operations_keypanel = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                   'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}



def random_move_naive(panel, curr_score, no_of_test_moves=100):
    '''
    It takes the panel , current score and provides the output for the next move
    '''

    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    succ_panels = []

    scores = [curr_score for a in range(len(moves))]
    for a in range(len(moves)):
        operation = moves[a]
        testPanel = copy.deepcopy(panel)

        if check_move_possible(testPanel, operation):

            move(testPanel, operation)
           
            scores[a] = add_upElements(testPanel, operation, scores[a])
         

            move(testPanel, operation)
            add_number_MCTS(testPanel)


            total_tries = 0
            total_score_added = 0
            temporaryPanel = copy.deepcopy(testPanel)
            for tries in range(no_of_test_moves):
                
                run_times = 1
                testPanel = copy.deepcopy(temporaryPanel)
                
                while not check_gameOver(testPanel):
                    testOperation = moves[random.randint(0, 3)]
                  
                  
                    if check_move_possible(testPanel, testOperation):

                        move(testPanel, testOperation)
                      
                        total_score_added += add_upElements_v2(testPanel, testOperation)                    
                        move(testPanel, testOperation)
                        add_number_MCTS(testPanel)
                        run_times += 1
                
                total_tries += run_times
        
        
                if get_max_no_cells(testPanel) > 4096:

                    succ_panels.append(testPanel)

            scores[a] += total_score_added / total_tries

    if max(scores) == curr_score:
        print("this time the AI can not make a move")
        return moves[random.randint(0, 3)], succ_panels
    else:
        return moves[scores.index(max(scores))], succ_panels

def run_MCTS_naive(N=4,no_of_test_moves=100):

    random.seed()

    panel = generate_panel(N)
    init_two(panel)
    print_panel(panel)
    curr_score = 0

    stuck = 0
    man = False
    while not check_gameOver(panel):

        print(" ")
        print("Current score is(Current Score), ", curr_score)
        print("Possible operations: Up, Down, Left, Right,  Exit")
        if not man:
            operation, succ_panels = random_move_naive(
                panel, curr_score, no_of_test_moves)
            if len(succ_panels) > 0:
                c = input("find success panel in test run, please press enter")
                for successBoard in succ_panels:
                    print_panel(successBoard)
                    print(" ")
                c = input("Enter to continue: ")
            operation = operation.upper()
        else:
            print("AI is stucked !!! Asking for man help :(  ")
            print("Possible operations: up, left, right, down, exit")
            operation = input('Your operation: ')
            operation = operation.upper()
            man = False

        if operation == "EXIT":
            break
      
        if check_move_possible(panel, operation):
            move(panel, operation)
         
            curr_score += add_upElements_v2(panel, operation)
            move(panel, operation)
            clear()
            add_number_MCTS(panel)
            print_panel(panel)
            print(" ")
        else:
            stuck += 1
           
            print("The operation provided is  ", operation, " but can not move")
            if stuck >= 10:
                clear()
                print_panel(panel)
                stuck = 0
                man = True

   
    print("Your Score is ", curr_score)
    print("Max number in panel is", get_max_no_cells(panel))
    print("Game end")
    return get_max_no_cells(panel)


def man_turn():
    panel = generate_panel(4)
    init_two(panel)
    print_panel(panel)
    curr_score = 0
    while not check_gameOver(panel):
        print(" ")
        print("current score is, ", curr_score)
        print("Possible operations: up, left, right, down, exit")
        print("Please press WASD for UP LEFT DOWN RIGHT")
        operation = operations_keypanel[pressed_key()]
        operation = operation.upper()
        if operation == "EXIT":
            break
  
        if check_move_possible(panel, operation):
            move(panel, operation)
            curr_score = add_upElements(panel, operation, curr_score)
            move(panel, operation)
            clear()
            add_number_MCTS(panel)
            print_panel(panel)
        else:
            clear()
            print_panel(panel)
    print("")
    print("Game Overrr!!")
    print("Your Score is ", curr_score)
    print("Max number in panel is", get_max_no_cells(panel))
    print("To run this game, type run()")



# 90% of time add 2 and 10% of time add 4

def add_number_MCTS(panel):

    emptyCells = get_not_filled_cell(panel)
    if len(emptyCells) == 0:
        print("Not any empty cells are found!!!")
        return

    row, column = emptyCells[random.randint(0, len(emptyCells) - 1)]
    random.seed()
    z = random.random()
    if z < 0.9:
        panel[row][column] = 2
    else:
        panel[row][column] = 4

run_MCTS_naive()