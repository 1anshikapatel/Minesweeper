
Minesweeper

Minesweeper is a game where you are given a grid of empty spaces that can be stepped upon. When stepping on a space, the space is either empty or contains a mine. Stepping on a space which contains a mine ends the game with the player losing. Stepping on an empty space reveals a number. This number represents how many neighboring tiles have mines. "1" means there is one tile that has a mine directly up, down, left, right, or diagonally to the current space. When all non-mine spaces are stepped upon the game is over and the player wins.

Download the GUI framework here. The framework is set up with the standard model/view/controller design in mind. Your job for this lab is to design the Minesweeper class which controls the game. Additionally, you must create a Tile class. Put both classes in a new file named minesweeper.py. A skeleton framework of code is provided in the download. Work in pieces and test each behavior as you create it. The properties and behaviors your classes need are described in the following sections. Make sure to note which parts have to match the naming scheme exactly as the GUI expects it.


Additional behavior of minesweeper is that if the user steps on a tile which contains zero mines, it will automatically (recursively) step on all adjacent tiles which are not revealed yet. This results in a "flooding" effect.

Also, right-clicking on a tile will flag that tile as "probably has a bomb". Flagging a tile prevents it from being stepped on.
Part 1 - Tile class -
Test out this class in a temporary main() function before moving on to Minesweeper.

Does not need any parameters to be created
States:
Can have a mine present or not
Can be "known" or "unknown"
Known means it will display more information
Unknown means it will display only a "?"
Can be exploded or not
If the tile is revealed and it contains a mine, it will explode
Can be flagged as a potential dangerous tile
Prevents the user from clicking on it later
A property keeping track of how many of its neighbors that have mines
Behaviors:
Can be converted to a string with str()
"!" if it is flagged and not known
"?" if it is not known
"X" if it is exploded
"*" if it has a mine
" " if it has zero neighbors (with mines)
Or a string equivalent to the number of neighbors (with mines) the tile has
Can be revealed with tile.reveal()
Makes the tile known
If it has a mine, sets the exploded property to True 
Returns True if it has a mine, False otherwise
Can be modified with tile.increaseNeighbors()
Increases the total number of neighbors (with mines) by 1
Can be modified with tile.toggleFlag()
Toggles the flagged property between True and False
Set to True if it is False, or False if it is True
Part 2 - Minesweeper class 
The order of behaviors listed below is not necessarily the best order to complete them in.

Must provide two parameters to create a new game with Minesweeper(size, mines)
The size parameter indicates the width and height of the game board
Always a square board
The mines parameter indicates the number of mines created in the board
States:
Keeps track of the size of the board - the width and height of the board are identical
Keeps track of how many mines there are
Two dimensional list of Tile objects representing the board
Just like ConnectFour, but with Tile() instead of strings
Mines will be added later
A property which represents if the game has "exploded"
True if the player revealed a tile and it had a mine on it
A property indicating how many tiles there are left to discover before the game is won
This is how many tiles there are in total minus the number of mines
Property indicating how many total flagged tiles there are

Behaviors
The size of the board can be obtained with len(<minesweeperInstance>)
This is the size of one side of the board
Has a method named EXACTLY minesRemaining()
Returns the number of mines minus the number of flagged tiles
Has a method named EXACTLY isGameOver()
True if the game exploded
True if the number of tiles left is 0
False otherwise
Has a method named EXACTLY getAt(row, column)
Returns the string representation of the tile at the given row and column
Has a method named EXACTLY isKnown(row, column)
Returns if the tile at the given row and column is known/revealed
Has a method to place all necessary mines to start the game
This method will place all the mines in the minesweeper game board as well as increase neighbor counts for all neighbors
Importantly, this method is NOT called in __init__, but is instead delayed to be called once the user makes their first move
This is so you can prevent the user from having an instant game over by happening to click on a space which has a mine
Needs to be given two parameters of row and column of where not to place a bomb
This is where the user clicked first to start the game
Randomly places all mines on the board
Use random.sample() with a list of all possible coordinate locations (minus the starting location) to prevent duplicate locations for mines
For each mine location:
Place a mine at the row and column
Increase the neighbor counts for all neighboring tiles, including diagonally
Has a method named EXACTLY step(row, column)
If this step is the first step in the game call the method to place all the mines
This way the mines can be placed in the game without instant game overs
You will need an instance property to detect the first step of the game
If the tile is flagged it does not do anything and returns from the method
Reveals the tile if it is unknown
If the given tile has a mine, sets the exploded property to True
Otherwise it uses the spreading method (see next bullet point) on this tile.
Has a method to "spread" a step to neighbors
If a user steps on a tile that has zero mines in its neighbors, then it should spread to all of its neighbors
Achieve this by calling self.step(r, c) on each neighbor which is still not known
Don't try to step on neighbors which are known, otherwise you get an infinite loop
Has a method named EXACTLY showAll()
Makes all the tiles known (does not call reveal())
For showing the entire board after the game ends
Has a method named EXACTLY isExploded()
Returns True if the game has exploded (revealed a tile that has a mine)
Has a method named EXACTLY flag(row, column)
Toggles the flag of the tile at the given row and column
Increases or decreases the total number of flagged tiles depending on the state of the flag of the tile
Has a method named EXACTLY getTotalFlags()
Returns how many flags there are currently
Store in an instance variable that is modified appropriately by flag()  
