"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player_x = set()
    player_O = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == X:
                player_x.add((i, j))
            elif cell == O:
                player_O.add((i, j))
    if len(player_x) > len(player_O):
        return O
    else:
            return X




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):              #enumerate() is a built-in Python function that allows you to loop over an iterable and
        for j, cell in enumerate(row):         #keeps track of the index of the current item in the iterable. 
            if cell == EMPTY:                    #produces pairs of (index, element) tuples for each element in my list.In this case our board made of lists.
                possible_actions.add((i,j))      #Each tuple (i, j) in the possible_actions set represents one available empty cell on the board, where a player can place their symbol to make a move.
    return possible_actions


    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = "X"
    player = None
    
    try:
        player = player(board)                  #Calling the player function with board as the parameter, It is calling the function and gets whose turn it is. And we asign it to a new variable player in this function.  
    except:
        pass

    i, j = action
    if board[i][j] != EMPTY:                    #If the index position represented by i, j board is not empty
        raise Exception("Invalid Action")

    if player is None:
        player = player(board)

                         
    new_board = [row.copy() for row in board]   #Copy of the board.List comprenhension: first expression generates elements of the list (row.copy()) and then a loop. Row and board are iterables.
    new_board[i][j] = player                    #This line updates the cell at position i, j on the new_board with the player's symbol (either "X" or "O").
    
    return new_board

 
 


def winner(board):
    """
    Returns the winner of the game, if there is one.

    """
    for row in board:                           #Horizontal win.
        if all(cell == X for cell in row):      #All: checks if all items in an iterable are true
            return X
        elif all(cell == O for cell in row):
            return O
    
    
    for col in range(3):                        #range(3) returns a sequence of numbers from 0 to 2, which corresponds to the column indices.
        if all(board[row][col] == X for row in range(3)):
            return X
        elif all(board[row][col] == O for row in range(3)):
            return O
    
    # Check diagonal wins
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    elif board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
    
    # If there's no winner, return None
    return None
        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Conditions to end game: winner or full board
    Use the winner() function to determine if there is a winner, and if so, return True.
    Check if the board is full by iterating over the board and checking if any cell is empty. If there are no empty cells, return True.
    """
    if winner(board) is not None:
        return True
    
    for row in board:
        for cell in row:
            if cell == EMPTY:     #If there is an empty cell, game is not over.
                return False
            
    return True                    #If all cells are checked and none are empty game is over, so we return True.

    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
