# AI_Hanabi_Assignment
Two player version of the cooperative game Hanabi.
Run the HanabiMain.py to play the game.

# Libraries
NumPy is a Python library necesary to work with arrays.
Random is a Python library for generating pseudo-random numbers.
Copy is a Python module used for copying different elements of a list.
Intertools is a Python module that permits performing memory and computation efficient tasks on iterators.

## Usage

It is recommended to enable dark theme in Python IDLE (or use the command prompt) to have a better layout of the game, i.e. to be able to distinguish properly the colors of the card pile.
To do so, the following steps should be followed:
1. Options ->  Configure IDLE
2. Configure IDLE -> Highlights
3. In highlights, choose IDLE Dark (instead of IDLE Classic)


No installation is necesary. The program can be ran directly on the IDLE. Simply extract the zip file.

To play the game, open the file HanabiMain.py and run it. 
The next steps should be straight forward, a menu is displayed giving all options and how to apply them.
Moreover, is also displayed the status of the game for each turn.

Firstly, is given the option of either playing against the AI or having two players.
This option is given so the code running the game can be studied separately from the code running the AI.

Then is also given the option of having either the default predefined set-up, or to have a newly defined set-up.
For the second option, can be defined the number of cards per player, the number of colors, the card distribution and the maximum number of hint and penalty tokens.
In the default configuration settings, those will be:
-number of cards per player = 4
-number of colors = 2
-card distribution (for each color) = three 1s, two 2s, 3s and 4s, and one 5
-Hint tokens = 8
-Maximun penalty tokens = 3

In both cases, the rules stay the same.
When playing with the AI, it is recommended to only use 2 colors because the AI algorithm can take a long time to run for each round with more colors, 
however, if you have a good computer and time to spare you can choose any up to 5 colors, the algorithm and game engine support it.