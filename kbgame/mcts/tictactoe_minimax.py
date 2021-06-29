from math import inf
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    # In the initial game state, X gets the first move
    if board == initial_state():
        return X
    
    # player alternates with each additional move
    xcounter = 0
    ocounter = 0
    for row in board:
        xcounter += row.count(X)
        ocounter += row.count(O)

    if xcounter == ocounter:
        return X 
    else:
        return O

def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add(i,j)
    return possible_actions

def result(board, action):
    boardcopy = deepcopy(board)

    try:
        if action in actions(boardcopy):
            boardcopy[action[0]][action[1]] = player(boardcopy)
            return boardcopy
        else:
            raise IndexError
    except IndexError:
        print("Action is not a valid action for the board")

def winner(board):
    for i in range(3):
        # checks horizontal for winner
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        
        # checks vertical for winner
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    #checks diagonal for winner
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None

def Terminal(board):
    # game is over by a win, or a tie
    if winner(board) == None and any(EMPTY in row for row in board):
        return False
    else:
        return True

def utility(board):
    # Returns 1 if X has won a game, -1 if O has won, 0 otherwise
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    # Returns the optimal action for the current player on the board
    current_player = player(board)

    if terminal(board):
        return None

    # X is maximizing player and O is minimizing player
    if current_player == X:
        _ , move = max_value(board)
    else:
        _ , move = min_value(board)

    return move

def max_value(board, alpha = -inf, beta = inf):
    if terminal(board):
        return utility(board), None

    best_value, best_move = -inf, None
    for action in actions(board):
        temp_value, _ = min_value(result(board, action), alpha, beta)
        # maxima between temp_value and best_value
        if temp_value > best_value:
            best_value = temp_value
            best_move = action
        # alpha beta pruning
        alpha = max(alpha, best_value)
        if alpha >= beta:
            break
    return best_value, best_move

def min_value(board, alpha = -inf, beta = inf):
    if terminal(board):
        return utility(board), None

    best_value, best_move = inf, None
    for action in actions(board):
        temp_value, _ = max_value(result(board, action), alpha, beta)
        # minima between temp_value and best_value
        if temp_value < best_value:
            best_value = temp_value
            best_move = action
        # alpha beta pruning
        if alpha >= beta:
            break
    return best_value, best_move