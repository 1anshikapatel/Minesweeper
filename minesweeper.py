"""
Author: Anshika and Vanshika 
Lab: 12
File: minesweeper.py
Purpose: Define the Minesweeper game logic and Tile class.
"""

import random

class Tile(object):
    def __init__(self):
        self.has_mine = False
        self.known = False
        self.exploded = False
        self.flagged = False
        self.neighbors = 0
    
    def __str__(self):
        if self.flagged:
            return "!"
        elif not self.known:
            return "?"
        elif self.exploded:
            return "X"
        elif self.has_mine:
            return "*"
        elif self.neighbors == 0:
            return " "
        else:
            return str(self.neighbors)
    
    def reveal(self):
        self.known = True
        if self.has_mine:
            self.exploded = True
            return True
        return False
    
    def increaseNeighbors(self):
        self.neighbors += 1
    
    def toggleFlag(self):
        self.flagged = not self.flagged

# Testing the Tile class
def main():
    tile= Tile()
    print(f"Initial Tile:{tile}")

    tile.toggleFlag()
    print(f"Tile after toggling flag:{tile}")

    tile.increaseNeighbors()
    print(f"Tile after increasing neighbors:{tile}")
    
    mine_present=tile.reveal()
    print(f"Tile after revealing: {tile}")
    print(f"Has mine:{mine_present}")

if __name__ == "__main__":
    main()

    

class Minesweeper(object):
    def __init__(self, size=4, mines=2):
        self.size = size
        self.mines = mines
        self.total_flags = 0
        self.exploded = False
        self.tiles_left = size * size - mines
        self.first_step = True
        
        # Stub setup for the board
        self.board = [[Tile() for _ in range(self.size)] for _ in range(self.size)]

    @property
    def num_columns(self):
        return len(self.board[0]) if self.board else 0
    
    def minesRemaining(self):
        return self.mines - self.total_flags
    
    def isGameOver(self):
        return self.exploded or self.tiles_left == 0
    
    def placeMines(self, first_row, first_column):
        possible_locations = [(r, c) for r in range(self.size) for c in range(self.size)
                               if (r, c) != (first_row, first_column)]
        mine_locations = random.sample(possible_locations, self.mines)
        
        for row, col in mine_locations:
            self.board[row][col].has_mine = True
            self.increaseNeighbors(row, col)
    
    def flag(self, row, column):
        tile = self.board[row][column]
        if not tile.known:
            tile.toggleFlag()
            if tile.flagged:
                self.total_flags += 1
            else:
                self.total_flags -= 1
    
    def step(self, row, column):
        tile = self.board[row][column]
        
        if self.first_step:
            self.placeMines(row, column)
            self.first_step = False
        
        if not tile.known:
            if tile.reveal():
                self.exploded = True
            else:
                self.tiles_left -= 1
                if tile.neighbors == 0:
                    self.spread(row, column)
    
    def spread(self, row, column):
        for r in range(max(0, row - 1), min(self.size, row + 2)):
            for c in range(max(0, column - 1), min(self.size, column + 2)):
                if (r, c) != (row, column) and not self.board[r][c].known:
                    self.step(r, c)
    
    def showAll(self):
        for row in self.board:
            for tile in row:
                tile.known = True
    
    def getAt(self, row, column):
        return str(self.board[row][column])
    
    def isKnown(self, row, column):
        return self.board[row][column].known
    
    def isExploded(self):
        return self.exploded
    
    def increaseNeighbors(self, row, column):
        for r in range(max(0, row - 1), min(self.size, row + 2)):
            for c in range(max(0, column - 1), min(self.size, column + 2)):
                if (r, c) != (row, column):
                    self.board[r][c].increaseNeighbors()
