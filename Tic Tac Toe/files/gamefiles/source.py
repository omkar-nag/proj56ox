import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns X or O depending on the next player.
    """
    cnt_x = 0
    cnt_o = 0

    for i in board:
        for j in i:
            if( j == X ):
                cnt_x += 1
            if( j== O):
                cnt_o += 1
    if cnt_x <= cnt_o :
        return X
    return O
    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j=action
    if board[i][j] != EMPTY:
        raise Exception('Invalid move')
    newBoard = copy.deepcopy(board)
    currPlayer = player(board)
    newBoard[i][j] = currPlayer
    return newBoard
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    values=[[],[],[]]    
    ver = [0,0,0]
    hor = [0,0,0]
    dia = [0,0]
    replacements = {
        'X': 1,
        'O': -1,
        None: 0,
    }

    for i in range(3):
        values[i] = [replacements[x] for x in board[i]]
        
    for i in range(3):
        for j in range(3):
            ver[i] += values[j][i]
            hor[i] += values[i][j]
        dia[0] += values[i][i]
        dia[1] += values[i][2-i]

    result = ver + hor + dia
    if 3 in result:
        return X
    if -3 in result:
        return O
    return None

def terminal(board):
    if winner(board) or not actions(board):
        return True
    return False


def utility(board):
    win = winner(board)
    if(win == X):
        return 1
    elif(win == O):
        return -1
    else:
        return 0

