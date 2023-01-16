# ultimate-tic-tac-toe

After implementing the UCT algorithm in a class of mine for Reversi (see [reversi-uct-project repository](https://github.com/nyfine99/reversi-uct-project)), I wanted to apply it to other games. I settled on Ultimate Tic-Tac-Toe, as I always found the game enjoyable and figured it wouldn't be too complicated to code from scratch (or at least from the rough outline from my Reversi project). The resulting game and automated players are in this repository. A solid explanation of the rules of Ultimate Tic-Tac-Toe can be found [here](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).

## The UCT Algorithm

See the README in my [reversi-uct-project repository](https://github.com/nyfine99/reversi-uct-project) for an explanation of this algorithm. Its baseline implementation does not change much with Ultimate Tic-Tac-Toe, though as we'll see later, its effectiveness does.

## Game Files

The following files are used either for the Ultimate Tic-Tac-Toe logic or for playing the game.

### ultimate_ttt.py

This file contains the game's logic and functions which allow it to be displayed to the user.

### supervisor.py

This file allows for the user to pit two of the algorithms against each other, a human player against one of the algorithms, or two humans against each other for a single game. Usage details to follow.

### test.py

This file allows for the user to pit two of the algorithms against each other, a human player against one of the algorithms, or two humans against each other for several games, and to observe the results. Usage details to follow.

## Player Files

The following files are all contained within the "players" folder, and contain essential functions for both human and automated players.

### human.py

This file allows a human to play against any of the automated players, or against another human.

### random_player.py

This file contains the get_move function for a random player, which moves randomly.

### ordinary_uct.py

This file contains the code implementing the ordinary UCT algorithm for Ultimate Tic-Tac-Toe.

### adjusted_uct_v1.py

This file contains the code implementing an adjusted version of the UCT algorithm for Ultimate Tic-Tac-Toe. This adjusted version multiplies the square root part of the formula in Q value calculation by constants corresponding to whether the move captures a small board (good) and whether the move gives the opponent an unrestricted move (bad). In testing with multiple values (unrecorded), this version does not perform so well against ordinary UCT.

### adjusted_uct_v2.py

This file contains the code implementing an adjusted version of the UCT algorithm for Ultimate Tic-Tac-Toe. This adjusted version adds to/subtracts from the win rate of a given move with constants corresponding to whether the move captures a small board (adds) and whether the move gives the opponent an unrestricted move (subtracts). In testing with multiple values, this version performs well against ordinary UCT; to see the results with various parameter values, see experiment_results.csv, or a synopsis in the "Notes and Conclusions" section.

### adjusted_uct_v2_copy.py

This file is an exact copy of adjusted_uct_v2.py, and it allows for playing adjusted_uct_v2.py against itself with different parameter values.

### adjusted_uct_v3.py

This file contains the code implementing an adjusted version of the UCT algorithm for Ultimate Tic-Tac-Toe. This adjusted version adds to/subtracts from the win rate of a given move with constants corresponding to whether the move captures a small board (adds) and whether the move gives the opponent an unrestricted move (subtracts). However, these constants are only utilized while a specified amount of spaces are left unfilled; otherwise, the ordinary UCT algorithm is used. In testing with multiple values, this version performs well against ordinary UCT; to see the results with various parameter values, see experiment_results.csv, or a synopsis in the "Notes and Conclusions" section.

## Other Files

### experiment_results.csv

This file contains the results from experiments with the adjusted UCT files with various parameter values.

## Usage

### Single Game 
To run two programs against each other, to play against a program, or to play against another human, cd to ultimate-tic-tac-toe and put the following line of code into the terminal:

```bash
python3 supervisor.py prog1 prog2 timeout_limit verbose
```

prog1: the name of the program which will go first, and play as X. Example: to assign a human player to be X, use "players.human" as prog1.

prog2: the name of the program which will go second, and play as O. Example: to assign an ordinary UCT player to be O, use "players.ordinary_uct" as prog2.

timeout_limit (optional): the time alloted to any player using some form of UCT to make their move. By default, this is 1 second.

verbose (optional): determines whether or not to show the board before each move; 1 (True) to show the board, 0 (False) not to show the board. By default, this is True.

Example: to test the ordinary UCT algorithm against the improved UCT algorithm, with ordinary moving first, showing the board between moves, and alloting each player 2 seconds to move, we would say:

```bash
python3 supervisor.py players.ordinary_uct players.improved 2.0 1
```

### Multiple Games
To run two programs against each other for multiple games, cd to ultimate-tic-tac-toe and put the following line of code into the terminal:

```bash
python3 test.py prog1 prog2 num_games timeout_limit verbose
```

This works as with the single game above, but with the following additions: 

- num_games sets the number of games for which the programs will run against each other.
- Between games, the system will print the total number of X wins thus far, as well as how many games have been played.

Example: to test the ordinary UCT algorithm against the improved UCT algorithm, with ordinary moving first, for 25 games; not showing the board between moves and alloting each player 0.5 seconds to move, we would say:

```bash
python3 test.py players.ordinary players.improved 25 0.5 0
```

## Notes and Conclusions

TBA.