from ultimate_ttt import *
import random

def get_move(game_state, tile):
	possibleMoves = getValidMoves(game_state)
	random.shuffle(possibleMoves)
	return possibleMoves[0]