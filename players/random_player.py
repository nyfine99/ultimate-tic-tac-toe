from ultimate_ttt import *
import random

def get_move(game_state, tile):
	possible_moves = get_valid_moves(game_state)
	random.shuffle(possible_moves)
	return possible_moves[0]