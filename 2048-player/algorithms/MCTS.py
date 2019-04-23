import copy



# Importing all the utilties

from logic import *

# Importing all the logics 

from util_dupli import *



operations_keypanel = {'w': 'UP', 'W': 'UP', 's': 'DOWN', 'S': 'DOWN',
                   'a': 'LEFT', 'A': 'LEFT', 'd': 'RIGHT', 'D': 'RIGHT'}

# randomMove_naive takes panel, current score and provides the next move


def randomMove_naive(panel, current_score, no_of_test_moves=100):
   

    moves = ('UP', 'DOWN', 'LEFT', 'RIGHT')

    successPanels = []

    scores = [current_score for a in range(len(moves))]
    for a in range(len(moves)):
        operation = moves[a]
        test_panel = copy.deepcopy(panel)

        if check_move_possible(test_panel, operation):

            move(test_panel, operation)
           
            scores[a] = add_upElements(test_panel, operation, scores[a])
         

            move(test_panel, operation)
            add_number(test_panel)


            total_tries = 0
            total_score_added = 0
            temporary_panel = copy.deepcopy(test_panel)
            for tries in range(no_of_test_moves):
                
                run_times = 1
                test_panel = copy.deepcopy(temporary_panel)
                
                while not check_gameOver(test_panel):
                    test_operation = moves[random.randint(0, 3)]
                  
                  
                    if check_move_possible(test_panel, test_operation):

                        move(test_panel, test_operation)
                      
                        total_score_added += add_upElements_v2(test_panel, test_operation)                    
                        move(test_panel, test_operation)
                        add_number(test_panel)
                        run_times += 1
                
                total_tries += run_times
        
        
                if get_max_no_cells(test_panel) > 4096:

                    successPanels.append(test_panel)

            scores[a] += total_score_added / total_tries

    if max(scores) == current_score:
        print("this time the AI can not make a move")
        return moves[random.randint(0, 3)], successPanels
    else:
        return moves[scores.index(max(scores))], successPanels

def runMCTS_naive(N=4,no_of_test_moves=100):

    random.seed()

    panel = generate_panel(N)
    init_two(panel)
    print_panel(panel)
    current_score = 0

    stuck = 0
    human = False
    while not check_gameOver(panel):

        print(" ")
        print("The score at the moment(Current Score), ", current_score)
        print("Possible operations: up, left, right, down, exit")
        if not human:
            operation, successPanels = randomMove_naive(
                panel, current_score, no_of_test_moves)
            if len(successPanels) > 0:
                c = input("find success panel in test run, please press enter")
                for successBoard in successPanels:
                    print_panel(successBoard)
                    print(" ")
                c = input("Enter to continue: ")
            operation = operation.upper()
        else:
            print("AI is stucked !!! Asking for human help :(  ")
            print("Possible operations: up, left, right, down, exit")
            operation = input('Your operation: ')
            operation = operation.upper()
            human = False

        if operation == "EXIT":
            break
      
        if check_move_possible(panel, operation):
            move(panel, operation)
         
            current_score += add_upElements_v2(panel, operation)
            move(panel, operation)
            clear()
            add_number(panel)
            print_panel(panel)
            print(" ")
        else:
            stuck += 1
           
            print("The operation provided is  ", operation, " but can not move")
            if stuck >= 10:
                clear()
                print_panel(panel)
                stuck = 0
                human = True

   
    print("Your Score is ", current_score)
    print("Max number in panel is", get_max_no_cells(panel))
    print("Game end")
    return get_max_no_cells(panel)


def human_turn():
    panel = generate_panel(4)
    init_two(panel)
    print_panel(panel)
    current_score = 0
    while not check_end(panel):
        print(" ")
        print("current score is, ", current_score)
        print("Possible operations: up, left, right, down, exit")
        print("Please press WASD for UP LEFT DOWN RIGHT")
        operation = operations_keypanel[key_press()]
        operation = operation.upper()
        if operation == "EXIT":
            break
  
        if check_move_possible(panel, operation):
            move(panel, operation)
            current_score = add_upElements(panel, operation, current_score)
            move(panel, operation)
            clear()
            add_number(panel)
            print_panel(panel)
        else:
            clear()
            print_panel(panel)
    print("")
    print("Game Overrr!!")
    print("Your Score is ", current_score)
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
