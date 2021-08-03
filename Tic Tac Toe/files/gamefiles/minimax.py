from .source import player,actions,result,terminal,utility

X = "X"
O = "O"
EMPTY = None

def minimax(board):
    """
    Returns an optimal move depending on the current player.
    """
    if terminal(board):
        return None
    else:
        if player(board) == X:
            action = helper(board,'max')[1]
            return action
        else:
            action = helper(board,'min')[1]
            return action

def helper(board,strategy):
        """
        Recursive function to calculate optimal move
        """
        if terminal(board):
            return utility(board), None
        
        if strategy == 'min':
            optimal_value = float('inf')
            counter_strategy = 'max'
        elif strategy == 'max':
            optimal_value = float('-inf')
            counter_strategy = 'min'
        optimal_move = None
        for action in actions(board):
                new_value, new_move = helper(result(board, action),counter_strategy)
                if strategy == 'max':
                    if new_value > optimal_value:
                        optimal_value = new_value
                        optimal_move = action
                        if optimal_value == 1:
                            return optimal_value, optimal_move
                if strategy == 'min':
                    if new_value < optimal_value:
                        optimal_value = new_value
                        optimal_move = action
                        if optimal_value == -1:
                            return optimal_value, optimal_move

        return optimal_value, optimal_move
