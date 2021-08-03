
import shutil
import copy

def print_row(board,row):
    print(f'{board[row][0]}|{board[row][1]}|{board[row][2]}'.center(shutil.get_terminal_size().columns))
    if not row == 2:
        print('-----|-----|-----'.center(shutil.get_terminal_size().columns))

def display_board(board,initial):
    if initial:
        newboard = [['  1  ','  2  ','  3  '],['  4  ','  5  ','  6  '],['  7  ','  8  ','  9  ']]
    else:  
        newboard = copy.deepcopy(board)
        for i in range(3):
            for j in range(3):
                if newboard[i][j] == 'X':
                    newboard[i][j] = '  X  '
                elif newboard[i][j] == 'O':
                    newboard[i][j] = '  O  '
                else:
                    newboard[i][j] = '     '


    for i in range(3):
        print_row(newboard,i)

    print("\n")

    return ""