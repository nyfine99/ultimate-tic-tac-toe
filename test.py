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



def supervisor_test(prog1_name,prog2_name,TIMEOUT_LIMIT, verbose):
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
            if verbose:
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
            if verbose:
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
        return 1.0
    elif c == 'O':
        print('Player 2 wins!')
        return 0.0
    else:
        print('The game is a draw.')
        return 0.5


if __name__=="__main__":
    # default timeout limit and verbose values
    TIMEOUT_LIMIT=0.5
    verbose=False

    prog1_name=sys.argv[1]
    prog2_name=sys.argv[2]
    num_games=int(sys.argv[3])
    if len(sys.argv)>4:
        TIMEOUT_LIMIT=float(sys.argv[4])
    if len(sys.argv)>5:
        verbose=int(sys.argv[5])

    x_wins = 0.0
    for i in range(1, num_games+1):
        x_wins += supervisor_test(prog1_name,prog2_name,TIMEOUT_LIMIT,verbose)
        if prog1_name == "ordinary_uct" or prog2_name == "ordinary_uct":
            ordinary_uct.ord_seen = {"X": {}, "O": {}}
            # print("Ordinary total calls to UCT: " + str(ordinary_uct.ord_total_tries))
            ordinary.ord_total_tries = 0
        if prog1_name == "improved_uct" or prog2_name == "improved_uct":
            improved_uct.imp_seen = {"X": {}, "O": {}}
            # print("Improved total calls to UCT: " + str(improved_uct.imp_total_tries))
            improved_uct.imp_total_tries = 0
        print("X wins:" + str(x_wins))
        print("Games played: " + str(i))

    # print(x_wins/num_games)