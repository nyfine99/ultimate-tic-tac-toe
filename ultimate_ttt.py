import random
import sys

def draw_board(game_state):
    # This function prints out the board that it was passed. Returns None.

    def print_row(row_num):
        # A helper function which prints the row_num row of the board, 
        # indexed at 0. Returns None.
        big_board_y = int(row_num/3)
        small_board_y = row_num % 3
        if small_board_y % 3 == 1:
            # We want to print the big board row label at the start of the line
            next_line = str(big_board_y + 1) + '  '
        else:
            next_line = '   '
        for i in range(3):
            for j in range(3):
                next_line = next_line + board[i][big_board_y][j][small_board_y]
                if j < 2:
                    next_line = next_line + '|'
            if i < 2:
                next_line += ' || '
        print(next_line)

    board = game_state[0]
    # board[0][0][0][0] = 'X'
    # board[0][0][2][1] = 'O'
    # board[1][0][0][1] = 'X'
    # board[2][2][0][1] = 'X'
    
    MINOR_HLINE = '   -+-+- || -+-+- || -+-+- '
    TEST_HLINE =  '    | |  ||  | |  ||  | |  '
    MAJOR_HLINE = '  =======##=======##======='
    VLINE =       '         ||       ||       '
    LABEL_LINE =  '     1        2        3   '
    # leaving space to the left for horizontal labels

    print(LABEL_LINE)
    print("") # adding space between labels and board
    # print(VLINE)
    for i in range(9):
        print_row(i)
        if i % 3 != 2:
            print(MINOR_HLINE)
        elif i != 8:
            # print(VLINE)
            print(MAJOR_HLINE)
            # print(VLINE)
    print("")


def get_new_game():
    # Creates a new game, including a blank board, 
    # blank small_winners, and free move_loc.
    big_board = []
    for i in range(3):
        medium_board = []
        for j in range(3):
            small_board = []
            for k in range(3):
                small_board.append([' '] * 3)
            medium_board.append(small_board)
        big_board.append(medium_board)

    small_winners = []
    for i in range(3):
        small_winners.append([' '] * 3)

    move_loc = [3,3] # ex.s: 0,0 is top left; 2,2 is bottom right; 0,1 is 
    # middle row left column; and 3,3 is an unconstrained move
    game_state = (big_board, small_winners, move_loc)
    return game_state


def is_on_board(bigx, bigy, smallx, smally):
    # Returns True if the coordinates are located on the board.
    return bigx >= 0 and bigx <= 2 and bigy >= 0 and bigy <=2 and (
        smallx >= 0 and smallx <= 2 and smally >= 0 and smally <=2)


def is_valid_move(board, small_winners, move_loc, bigx, bigy, smallx, smally):
    # Mostly used as a helper function for get_valid_moves, hence the components
    # of game_state are taken in as parameters rather than game_state
    # bigx, bigy, smallx, and smally indicate the player's desired move.
    # Returns False if the player's move on the space indicated is invalid.
    # Returns True if the move is valid.
    if (is_on_board(bigx, bigy, smallx, smally)) and (
        small_winners[bigx][bigy] == ' ') and (
        (move_loc[0]==3) or (move_loc[0]==bigx and move_loc[1]==bigy)) and (
        board[bigx][bigy][smallx][smally] == ' '):
        return True
    return False


def get_valid_moves(game_state):
    # Returns a list of [bigx,bigy,smallx,smally] lists of valid moves for the
    # player in the current game_state.
    board = game_state[0]
    small_winners = game_state[1]
    move_loc = game_state[2]

    validMoves = []

    if move_loc[0] == 3:
        for bigx in range(3):
            for bigy in range(3):
                for smallx in range(3):
                    for smally in range(3):
                        if is_valid_move(board, small_winners, move_loc, bigx, 
                            bigy, smallx, smally):
                            validMoves.append([bigx, bigy, smallx, smally])
    else:
        for smallx in range(3):
            for smally in range(3):
                if is_valid_move(board, small_winners, move_loc, move_loc[0], 
                    move_loc[1], smallx, smally):
                    validMoves.append([move_loc[0], move_loc[1], 
                        smallx, smally])
    return validMoves

def check_tttboard_for_winner(tttboard):
    # Checks a standard tic-tac-toe board for a winner.
    # Returns 'X' if X wins, 'O' if O wins, and ' ' otherwise
    for c in ['X', 'O']:
        # checking for a horizontal win
        for row in range(3):
            curr_row_c = True
            for col in range(3):
                if tttboard[col][row] != c:
                    curr_row_c = False
                    break
            if curr_row_c:
                return c

        # checking for a vertical win
        for col in range(3):
            curr_col_c = True
            for row in range(3):
                if tttboard[col][row] != c:
                    curr_col_c = False
                    break
            if curr_col_c:
                return c

        # checking for a diagonal win
        curr_rowcol_c = True
        for rowcol in range(3):
            if tttboard[rowcol][rowcol] != c:
                curr_rowcol_c = False
                break
        if curr_rowcol_c:
            return c
        curr_rowcol_c = True
        for rowcol in range(3):
            if tttboard[2-rowcol][rowcol] != c:
                curr_rowcol_c = False
                break
        if curr_rowcol_c:
            return c

    # if this point is reached, we have no winner
    return ' '

def is_full(tttboard):
    # Returns True if tttboard is full, false otherwise
    for i in range(3):
        for j in range(3):
            if tttboard[i][j] == ' ':
                return False
    return True


def indicate_winner(small_board, tile):
    # Adjusts a small board on which a player has won 
    # to indicate it more clearly.
    # Returns the adjusted small board.
    if tile == 'X':
        small_board[0][0] = 'X'
        small_board[0][1] = ' '
        small_board[0][2] = 'X'
        small_board[1][0] = ' '
        small_board[1][1] = 'X'
        small_board[1][2] = ' '
        small_board[2][0] = 'X'
        small_board[2][1] = ' '
        small_board[2][2] = 'X'
    elif tile == 'O':
        small_board[0][0] = 'O'
        small_board[0][1] = 'O'
        small_board[0][2] = 'O'
        small_board[1][0] = 'O'
        small_board[1][1] = ' '
        small_board[1][2] = 'O'
        small_board[2][0] = 'O'
        small_board[2][1] = 'O'
        small_board[2][2] = 'O'
    return small_board


def make_move(game_state, tile, bigx, bigy, smallx, smally):
    # Place the tile on the board at the indicated location, 
    # and update all components of game_state accordingly.
    # Returns False if this is an invalid move, the new game_state otherwise.
    big_board = game_state[0]
    small_winners = game_state[1]
    move_loc = game_state[2]
    if not is_valid_move(big_board, small_winners, move_loc, 
        bigx, bigy, smallx, smally):
        return False

    # if this point is reached, the move is valid, and the 
    # game_state needs to be updated
    # adjusting big_board
    big_board[bigx][bigy][smallx][smally] = tile
    # adjusting small_winners, if applicable
    if check_tttboard_for_winner(big_board[bigx][bigy]) == tile:
        big_board[bigx][bigy] = indicate_winner(big_board[bigx][bigy], tile)
        small_winners[bigx][bigy] = tile
    # adjusting move_loc
    if small_winners[smallx][smally]!=' ' or is_full(big_board[smallx][smally]):
        # if the next player is sent to a box which has been won or 
        # which is full, they get an unconstrained move
        # adjusting one element at a time so that it isn't adjusting the copy
        move_loc[0] = 3
        move_loc[1] = 3
    else: 
        move_loc[0] = smallx
        move_loc[1] = smally

    return True


def get_game_state_copy(game_state):
    # Make a duplicate of the board list and return the duplicate.
    game_state_copy = get_new_game()
    
    board = game_state[0]
    board_copy = game_state_copy[0]
    winners = game_state[1]
    winners_copy = game_state_copy[1]
    move_loc = game_state[2]
    move_loc_copy = game_state_copy[2]

    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    board_copy[i][j][k][l] = board[i][j][k][l]

            winners_copy[i][j] = winners[i][j]

    move_loc_copy[0] = move_loc[0]
    move_loc_copy[1] = move_loc[1]

    return game_state_copy


def winner(game_state):
    # Returns 'X' if X has won, 'O' if O has won, and ' ' otherwise.
    return check_tttboard_for_winner(game_state[1])


# I use the main method below to test

# if __name__=="__main__":
#     game_state = get_new_game()
#     draw_board(game_state)
#     new_board = [['X', 'O', 'X'],
#         ['O', 'X', 'X'],
#         ['O', 'O', 'X']]
#     print(is_full(new_board))
#     print(check_tttboard_for_winner(new_board))

#     game_state[0][0][0] = indicate_winner(new_board)
#     draw_board(game_state)

#     make_move(game_state, 'X', 1,1,0,0)
#     draw_board(game_state)
#     make_move(game_state, 'O', 0,0,1,1)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,1,2,2)
#     draw_board(game_state)
#     make_move(game_state, 'O', 2,2,1,1)
#     draw_board(game_state)
#     game_state_copy = get_game_state_copy(game_state)
#     make_move(game_state, 'X', 1,1,1,1)
#     draw_board(game_state)
#     draw_board(game_state_copy)
#     print(game_state[1])
#     print(game_state_copy[1])
#     print(game_state[2])
#     print(game_state_copy[2])

#     make_move(game_state, 'X', 1,1,0,0)
#     draw_board(game_state)
#     make_move(game_state, 'O', 0,0,1,1)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,1,2,2)
#     draw_board(game_state)
#     make_move(game_state, 'O', 2,2,1,1)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,1,1,1)
#     draw_board(game_state)
#     make_move(game_state, 'O', 0,0,1,0)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,0,2,0)
#     draw_board(game_state)
#     make_move(game_state, 'O', 2,0,1,0)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,0,1,0)
#     draw_board(game_state)
#     make_move(game_state, 'O', 1,0,1,1)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,0,0,0)
#     draw_board(game_state)
#     make_move(game_state, 'O', 0,0,1,2)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,2,2,2)
#     draw_board(game_state)
#     make_move(game_state, 'O', 2,2,1,2)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,2,2,0)
#     draw_board(game_state)
#     make_move(game_state, 'O', 2,0,1,2)
#     draw_board(game_state)
#     make_move(game_state, 'X', 1,2,2,1)
#     draw_board(game_state)
#     print(winner(game_state))