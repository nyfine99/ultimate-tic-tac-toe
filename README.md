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

### test_with_memory.py

Similar to the above, but does not clear the players' states-seen dictionaries between games. Usage details to follow.

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

Example: to test the ordinary UCT algorithm against version 2 of the adjusted UCT algorithm, with ordinary moving first, showing the board between moves, and alloting each player 2 seconds to move, we would say:

```bash
python3 supervisor.py players.ordinary_uct players.adjusted_uct_v2 2.0 1
```

### Multiple Games
To run two programs against each other for multiple games, with "memory" (meaning, each player retains their states-seen), cd to ultimate-tic-tac-toe and put the following line of code into the terminal:

```bash
python3 test_with_memory.py prog1 prog2 num_games timeout_limit verbose
```

To do so without memory, say:

```bash
python3 test.py prog1 prog2 num_games timeout_limit verbose
```

This works as with the single game above, but with the following additions: 

- num_games sets the number of games for which the programs will run against each other.
- Between games, the system will print the total number of X wins thus far, as well as how many games have been played.

Example: to test the ordinary UCT algorithm against version 2 of the adjusted UCT algorithm, with ordinary moving first, for 25 games; not showing the board between moves and alloting each player 0.5 seconds to move; and with memory; we would say:

```bash
python3 test_with_memory.py players.ordinary_uct players.adjusted_uct_v2 25 0.5 0
```


## Notes

It should be noted that, after completion, testing was discovered to have been done with a version of test.py which did not clear the states-seen dictionaries between games for all of the UCT files (with "memory", discussed earlier). Meaning, if multiple games were run, players would save the states-seen from previous games for use in the current one. While this is similar to how human players operate, where we learn from our mistakes, this was not initially my desired testing method for the UCT algorithms, though it is justifiable after the fact. I hope to one day rerun the tests with the non-remembering test.py; the test.py which keeps the states-seen is now saved as test_with_memory.py.

Adjusted UCT v1 performed poorly against ordinary UCT, with both given 2 seconds to move, in initial testing. This testing is not recorded in experiment_results, and no further testing was done, as focus shifted to adjusted UCT v2, which did perform well in initial testing.

However, v2 with the appropriate parameter values (in the 0.1 to 0.125 range for both CAPTURE_BOX_CONST and GIVE_FREE_CONST) was found to perform rather well against ordinary UCT, achieving a win rate north of 0.6 (counting draws as 0.5) as both X and O when both players were given 2 seconds to move. This win rate is outside of the 95% confidence interval of what we would expect to see if adjusted UCT v2 and ordinary UCT were truly equal, and thus this outperformance is significant. The v2 parameters have not been fully optimized, but parameter values of 0.1 and 0.125 (for both added parameters) perform similarly against each other, both when given 2 and when given 15 seconds to move; when 0.05, 0.075, 0.15, and 0.2 were tested against 0.1 with 2 seconds to move, decreased performance was observed.

In limited testing, v3 did not outperform v2 with a STOP_VALUE of 27 and with both players having 2 seconds to move, but further testing is needed for other parameter values.

In terms of performance against humans, there appears to have been a massive upgrade from ordinary UCT to adjusted UCT v2. Ordinary UCT was able to beat a ten year old beginner with 15 seconds to move, but I consistently crushed it. However, adjusted UCT v2 beat me about as often as I beat it when given 15 seconds to move, with parameter values of both 0.1 and 0.125.

Feel free to browse experiment_results for more detailed results.

## Conclusion

Overall, I am pleased with the performance of adjusted UCT v2 with both of its additional parameters having value either 0.1 or 0.125, especially against me, as this version of the automated player was able to beat me! That said, there is certainly still room to optimize.