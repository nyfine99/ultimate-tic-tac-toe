"""
In this file, we implement an improved version of UCT. This version prioritizes
not giving away free moves and capturing boxes when possible. It uses
constants below in the Q value calculation to implement this, as well as taking
the move which either captures a square or doesn't give away a free move in the
event of tied r values. These constants are added to the win rate in both the
Q value calculation and during move selection.
"""

# After only STOP_VALUE spaces are available, this system no longer takes effect.
# Note that this is only checked at the start of the get_move function, not with
# each recursive call to UCT
STOP_VALUE = 82 # N/A, currently

# The constant added to r for a captured box
CAPTURE_BOX_CONST = 0.08

# The constant subtracted from r when an unrestricted move is given
GIVE_FREE_CONST = 0.08

# performing necessary imports
from ultimate_ttt import *
import supervisor
import random
import time
import math

# a global variable which tracks the sets of all game states seen;
# this is split into "X" and "O" to prevent one player from peeking 
# at another's data
imp_seen = {"X": {}, "O": {}} # map from player -> 
# (map from states -> [r_state, t_state])
# states are represented as board strings

imp_total_tries = 0 # tracks how many times the get_move algorithm has
# been run; I wanted to compare this to improved and it helped with debugging


def alt_make_move(game_state, tile, bigx, bigy, smallx, smally):
    # an alternate make_move function which returns None if the move is
    # invalid and updates the game state if it is valid. However, this will
    # now also return whether or not the new game state resulted in a
    # new captured box for the player as a boolean if the move is valid;
    # this need not return whether a free move was given away, as this 
    # is implied by move_loc
    # Place the tile on the board at the indicated location, 
    # and update all components of game_state accordingly.
    # Returns False if this is an invalid move, True otherwise.
    big_board = game_state[0]
    small_winners = game_state[1]
    move_loc = game_state[2]
    if not is_valid_move(big_board, small_winners, move_loc, 
        bigx, bigy, smallx, smally):
        return None

    box_captured = False # this will become true if a box was captued
    # if this point is reached, the move is valid, and the 
    # game_state needs to be updated
    # adjusting big_board
    big_board[bigx][bigy][smallx][smally] = tile
    # adjusting small_winners, if applicable
    if check_tttboard_for_winner(big_board[bigx][bigy]) == tile:
        big_board[bigx][bigy] = indicate_winner(big_board[bigx][bigy], tile)
        small_winners[bigx][bigy] = tile
        box_captured = True
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

    return box_captured


def get_state_string(game_state):
    # Returns the game_state represented as a string.

    # We should first note that the small board winners are implied by 
    # the big board, so this need not be included in the string.
    # However, two states could have the same board setup but a different
    # move_loc, so the string must include both

    board = game_state[0]
    move_loc = game_state[2]
    s = ""
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    s = s + board[i][j][k][l]

    s = s + str(move_loc[0]) + str(move_loc[1])
    return s

def get_state_string_after_move(game_state, move, curr_player):
    # Returns the state string after applying move to the board

    state_copy = get_game_state_copy(game_state)
    box_captured = alt_make_move(
        state_copy, curr_player, move[0], move[1], move[2], move[3])
    s = get_state_string(state_copy)
    gives_free_move = (state_copy[2][0] == 3)
    return s, box_captured, gives_free_move


def Q_value(r_next_move, t_next_move, t_total, curr_player, 
    box_captured, gives_free_move):
    """
    r_next_move: r_y, the observed reward at state y, where y is the 
    state of the game after the move being examined is made
    t_next_move: t_y, the number of times we have explored state y, where
    y is the state of the game after the move being examined is made
    t_total: the total explorations we have made of the current state
    curr_player: the tile of the player whose turn it currently is to move
    
    Returns the "score" for the player owning curr_player of making the move 
    currently being explored.
    """
    local_box_const = 0.0
    if box_captured:
        local_box_const = CAPTURE_BOX_CONST
    local_free_const = 0.0
    if gives_free_move:
        local_free_const = GIVE_FREE_CONST
    if curr_player == 'X':
        # we are at a max node, so we want to maximize the following:
        return r_next_move + local_box_const - local_free_const + math.sqrt(
            2 * math.log(t_total)/t_next_move)
    # we are at a min node, so we want to maximize the following:
    return 1 - r_next_move + local_box_const - local_free_const + math.sqrt(
            2 * math.log(t_total)/t_next_move)
    # note: the maximization of the result is done in UCB_choose


def UCB_choose(game_state, state_string, possible_moves, curr_player, 
    states_seen):
    """
    game_state: the game_state being examined
    state_string: the string representation of the game_state
    (passed in to save time)
    possible_moves: all possible moves that curr_player can make
    curr_player: the tile of the player whose turn it is to move in this state
    states_seen: the set of states seen, mapped to each state's r and t values
    
    Returns the move which UCB_choose, as described in class, would select
    from the set of possible moves.
    """
    
    random.shuffle(possible_moves)
    # tracks the sum of t values for all child states; this will be relevant
    # if all child states have already been seen
    t_total = 0
    for i in range(0, len(possible_moves)):
        # obtaining the child state corresponding to making the move 
        # possible_moves[i]
        new_state, _, _ = get_state_string_after_move(game_state, 
            possible_moves[i], curr_player)
        if new_state not in states_seen:
            # this move has not yet been examined, so we return it
            return possible_moves[i]
        t_total += states_seen[new_state][1]

    # if this point is reached, all children states have been seen; so, we
    # will find the move with the best "score" as specified in the UCB_choose
    # pseudocode from class; the move which best maximizes exploration vs 
    # exploitation
    curr_max = -1
    best_move = -1
    for i in range(0, len(possible_moves)):
        new_state, box_captured, gives_free_move = get_state_string_after_move(
            game_state, possible_moves[i], curr_player)
        r_t_pair = states_seen[new_state] # this has the list [r_y, t_y] 
        # for child state y
        curr_Q_val = Q_value(r_t_pair[0], r_t_pair[1], t_total, curr_player,
            box_captured, gives_free_move)
        if curr_Q_val > curr_max:
            # in this case, the possible_moves[i] has a better score than 
            # the other moves checked so far
            curr_max = curr_Q_val
            best_move = possible_moves[i]
    
    return best_move

def UCT(game_state, curr_player, states_seen):
    """
    game_state: the game_state being examined
    curr_player: the tile of the player whose turn it is to move in this state
    states_seen: the set of seen states, mapped to the each state's r and t 
    values
    
    Updates states_seen appropriately for the current game_state based on the 
    results of the successive calls to UCT.
    Returns the r value of the current move = the r value of the next move
    chosen by UCB_choose (which is then used by the previous calls to 
    recursively update states_seen).
    """

    # get the current state of the game_state in string form, so that we can use it
    # as a key in states_seen
    state_string = get_state_string(game_state)
    if state_string not in states_seen:
        # in this case, we must initialize the r and t values for the current
        # state; we will have adjusted these values by the end of the run
        states_seen[state_string] = [0, 0]

    valid_moves = get_valid_moves(game_state)
    game_winner = winner(game_state)
    if valid_moves == [] or game_winner != ' ':
        # in this case the game is done
        # we treat X as max nodes and O as min nodes, so return 1 if X wins,
        # 0 if O wins
        if game_winner == 'X':
            # X wins; adjust r appropriately and return r value
            states_seen[state_string][0] = (states_seen[state_string][0] * 
                states_seen[state_string][1]+1.0)/(states_seen[state_string][1]+1.0)
            # increment t value
            states_seen[state_string][1] = states_seen[state_string][1] + 1.0
            return 1.0
        elif game_winner == ' ':
            # tie; adjust r appropriately and return r value
            states_seen[state_string][0] = (states_seen[state_string][0] * 
                states_seen[state_string][1] + 0.5)/(states_seen[state_string][1] +1.0)
            # increment t value
            states_seen[state_string][1] = states_seen[state_string][1] + 1.0
            return 0.5
        else:
            # O wins; adjust r appropriately and return r value
            states_seen[state_string][0] = (states_seen[state_string][0] * 
                states_seen[state_string][1])/(states_seen[state_string][1]+1.0)
            # increment t value
            states_seen[state_string][1] = states_seen[state_string][1] + 1.0
            return 0.0
    
    # if we have reached this point, there are valid moves to be made
    # we can save time by passing in board and state_string to UCB_choose
    next_move = UCB_choose(game_state, state_string, valid_moves, curr_player, states_seen)
    next_player = "O"
    if curr_player == "O":
        next_player = "X"
    # next tile is now set to the tile of the player whose turn is next
    # we make the move chosen by UCB_choose...
    make_move(game_state, curr_player, next_move[0], next_move[1], next_move[2], next_move[3])
    # ... and then use a recursive call to UCT to find the r value of 
    # that move ...
    val_next_move = UCT(game_state, next_player, states_seen)
    # ... and then update the r and t values of the current move accordingly
    states_seen[state_string][0] = (states_seen[state_string][0] * 
        states_seen[state_string][1] + val_next_move)/(states_seen[state_string][1] + 1.0)
    states_seen[state_string][1] = states_seen[state_string][1] + 1.0

    # and we return the r value for the current move
    return val_next_move

def get_move(game_state, curr_player):
    # Returns the best known move that can be made after a call to UCT.

    # importing the set of all states seen so far
    global imp_seen
    # importing a counter which counts the total calls to get_move;
    # interesting to see the statistics on this
    global imp_total_tries
    # creating a copy of the board, so that the board is not edited 
    # by our call to UCT
    state_copy = get_game_state_copy(game_state)

    # call UCT
    UCT(state_copy, curr_player, imp_seen[curr_player])

    # take the best known move; if X is currently moving, this is the move
    # with the highest r value, and if O is moving, this is the move with
    # the lowest r value
    poss_moves = get_valid_moves(game_state)
    random.shuffle(poss_moves)
    curr_best = [-1, -1, -1, -1]
    if curr_player =="X":
        curr_max_r = -1
        for move in poss_moves:
            post_move, captures_box, gives_free_move = get_state_string_after_move(
                game_state, move, curr_player)

            local_box_const = 0.0
            if captures_box:
                local_box_const = CAPTURE_BOX_CONST
            local_free_const = 0.0
            if gives_free_move:
                local_free_const = GIVE_FREE_CONST
            if post_move in imp_seen[curr_player] and (
                imp_seen[curr_player][post_move][0] + local_box_const - local_free_const > curr_max_r):
                curr_best = move
                curr_max_r = imp_seen[curr_player][post_move][0] + local_box_const - local_free_const

        # This statement can be used to obtain how UCT views its win probability after this move        
        # print(curr_max_r)

    else:
        curr_min_r = 2
        for move in poss_moves:
            post_move, captures_box, gives_free_move = get_state_string_after_move(
                game_state, move, curr_player)

            local_box_const = 0.0
            if captures_box:
                local_box_const = CAPTURE_BOX_CONST
            local_free_const = 0.0
            if gives_free_move:
                local_free_const = GIVE_FREE_CONST
            if post_move in imp_seen[curr_player] and (
                imp_seen[curr_player][post_move][0] - local_box_const + local_free_const < curr_min_r):
                curr_best = move
                curr_min_r = imp_seen[curr_player][post_move][0] - local_box_const + local_free_const

        # This statement can be used to obtain how UCT views its win probability after this move        
        # print(curr_min_r)

    imp_total_tries = imp_total_tries + 1
    return curr_best