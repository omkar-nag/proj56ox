import os,time,sys,json,shutil

from .source import actions,result,terminal,utility,initial_state
from .minimax import minimax
from .board_view import display_board

def print_center(s):
    print(s.center(shutil.get_terminal_size().columns))
    return ""

def width():
    return int((shutil.get_terminal_size().columns)/2) - 1

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def MainGame():
    clear_terminal()
    board = initial_state()
    s = "TIC TAC TOE"

    print("\n")
    print_center(s)
    print_center("")
    print_center('Choose X or O: ')
    player = input(" "*width()).capitalize()

    print_center("")

    while player != 'X' and player!='O':
        print_center('Enter a valid character')
        player = input(" "*width()).capitalize()

    clear_terminal()
    print_center("\n")
    print_center(s)
    print_center("\n")

    print_center('Use this as a guide to the board:' + "\n")
    print_center(display_board(board,True))

    ai_turn = False 
    if player == 'O':
        ai_turn = True
    tiles = {1:(0,0) , 2:(0,1) , 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2), 7:(2,0), 8:(2,1), 9:(2,2)}
    tiles2 = {(0,0):1 , (0,1):2 , (0,2):3, (1,0):4, (1,1):5, (1,2):6, (2,0):7, (2,1):8, (2,2):9}
    
    while not terminal(board):
        if ai_turn:
            
            print_center('AI is making its move...')
            print_center('')
            time.sleep(3)
            ai_action = minimax(board)
            board = result(board,ai_action)
            ai_turn = False
        else:
            while True:
                print_center('Insert a value between 1-9: ')
                while True:
                    try:
                        player_action = int(input(" "*width()))
                        print_center("")
                        break
                    except:
                        print_center('Please enter an integer value')
                

                possible_actions = actions(board)
                try: 
                    board = result(board,tiles[player_action])
                    ai_turn = True
                    break
                except Exception:
                    x=[]
                    for i in possible_actions:
                        x.append(tiles2[i])
                    print_center('Invalid move! Your possible moves are:')
                    
                    print_center(json.dumps(sorted(x)))
                    print_center("")
        
        clear_terminal()

        print("\n")
        print_center(s)
        print_center("\n")
        print_center("Guide")
        print_center(display_board(board,True))
        print_center(display_board(board,False))

    if utility(board)==1:
        if player == 'X':
            print_center('Congratulations, you win!')
        else:
            print_center('Sorry, you lose!')
    elif utility(board)==-1:
        if player == 'O':
            print_center('Congratulations, you win!')
        else:
            print_center('Sorry, you lose!')
    else:
        print_center('The game ended in a draw!') 
    

    print_center('Would you like to play again? (Y/N)')
    play_again = input(" "*width()).lower()
    if play_again == 'y':
        MainGame()
    else:
        clear_terminal()
        print_center('\n')
        print_center('Thank you for playing!')
        sys.exit()