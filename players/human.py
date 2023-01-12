from ultimate_ttt import *

def get_move(game_state, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the string 'quit')
    DIGITS1TO3 = '1 2 3'.split()
    while True:
        print('Enter your move, or type quit to end the game.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 4 and move[0] in DIGITS1TO3 and (
            move[1] in DIGITS1TO3 and move[2] in DIGITS1TO3 and
            move[3] in DIGITS1TO3):
            bigx = int(move[0]) - 1
            bigy = int(move[1]) - 1
            smallx = int(move[2]) - 1
            smally = int(move[3]) - 1
            if isValidMove(game_state[0], game_state[1], game_state[2], 
                bigx, bigy, smallx, smally) == False:
                print('That is not a valid move.')
                print('Type the big column, ' + 
                'then the big row, then the small column, ' + 
                'then the small row; all digits from 1 to 3.')
                print('For example, 3111 will be the top-left corner or the top-right board.')
            else:
                break
        else:
            print('That is not a valid move.')
            print('Type the bigx digit (1-3), ' + 
            'then the bigy digit (1-3), then the smallx digit (1-3), ' + 
            'then the smally digit (1-3).')
            print('For example, 3111 will be the top-left corner or the top-right board.')

    return [bigx, bigy, smallx, smally]