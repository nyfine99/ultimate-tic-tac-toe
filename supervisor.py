from ultimate_ttt import *
import importlib
import sys
import time

def get_func(programname, functionname):
    module_str = programname  
    module = importlib.import_module(module_str)  # import module from str
    f = getattr(module, functionname)  # get function "function" in module
    return f

def showNextMoveLoc(game_state, tile):
    # Prints out the current score.
    move_loc = game_state[2]
    if move_loc[0] == 3:
        print(tile + ' to move, unrestricted')
    else:
        print(tile + ' to move, restricted to board [' + 
            str(move_loc[0] + 1) + ',' + str(move_loc[1] + 1) + ']')



def supervisor(prog1_name,prog2_name,TIMEOUT_LIMIT, verbose):
    player1_get_move=get_func(prog1_name, 'get_move')
    player2_get_move=get_func(prog2_name, 'get_move')

    if prog1_name==prog2_name:
        prog1_name=prog1_name+"_v1"
        prog2_name=prog2_name+"_v2"

    moves=0

    game_state = get_new_game()
    player1Tile, player2Tile = ['X', 'O']
    turn=prog1_name
    while True:
        if turn == prog1_name:
            if verbose:
                draw_board(game_state)
                showNextMoveLoc(game_state, player1Tile)

            while True:
                start = time.time()
                while time.time() - start < TIMEOUT_LIMIT:
                    move = player1_get_move(game_state, player1Tile)

                if move == 'quit':
                    print("Player 1 has quit the game.")
                    return
                elif is_valid_move(game_state[0], game_state[1], game_state[2], 
                    move[0], move[1], move[2], move[3]):
                    break
                else:
                    print("["+str(move[0]+1)+","+str(move[1]+1)+","+
                        str(move[2]+1)+","+str(move[3]+1)+"]"+
                        " is an invalid move")
            print("Player 1 played:["+str(move[0]+1)+","+str(move[1]+1)+
                ","+str(move[2]+1)+","+str(move[3]+1)+"]")
            make_move(game_state, player1Tile,move[0],move[1],move[2],move[3])

            if winner(game_state) != ' ' or get_valid_moves(game_state) == []:
                break
            else:
                turn = prog2_name

        else:
            if verbose:
                draw_board(game_state)
                showNextMoveLoc(game_state, player2Tile)
            
            while True:
                start = time.time()
                while time.time() - start < TIMEOUT_LIMIT:
                    move = player2_get_move(game_state, player2Tile)
                
                if move == 'quit':
                    print("Player 2 has quit the game.")
                    return
                elif is_valid_move(game_state[0], game_state[1], game_state[2],
                    move[0], move[1], move[2], move[3]):
                    break
                else:
                    print("["+str(move[0]+1)+","+str(move[1]+1)+","+
                        str(move[2]+1)+","+str(move[3]+1)+"]"+
                        " is an invalid move")
            print("Player 2 played:["+str(move[0]+1)+","+str(move[1]+1)+
                ","+str(move[2]+1)+","+str(move[3]+1)+"]")
            make_move(game_state,player2Tile,move[0],move[1],move[2],move[3])


            if winner(game_state) != ' ' or get_valid_moves(game_state) == []:
                break
            else:
                turn = prog1_name

        moves+=1
    # Display the final board and the winner
    draw_board(game_state)
    c = winner(game_state)
    if c == 'X':
        print('Player 1 wins!')
    elif c == 'O':
        print('Player 2 wins!')
    else:
        print('The game is a draw.')


if __name__=="__main__":
    # default TIMEOUT_LIMIT and verbose values
    TIMEOUT_LIMIT=0.5
    verbose=True

    if len(sys.argv)<3:
        print("You need to provide 2 inputs program. One or both of them can be \"computer\"")
        quit()
    prog1_name=sys.argv[1]
    prog2_name=sys.argv[2]
    if len(sys.argv)>3:
        TIMEOUT_LIMIT=float(sys.argv[3])
    if len(sys.argv)>4:
        verbose=int(sys.argv[4])

    supervisor(prog1_name,prog2_name,TIMEOUT_LIMIT=TIMEOUT_LIMIT, verbose=verbose)