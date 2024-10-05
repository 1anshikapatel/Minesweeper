"""
Author: Liz Matthews and additions by Vanshika and Anshika. 
File: minesweeperGUI.py

Displays a window with multiple buttons and plays the connect four game.We attempted to add the high score button. 
"""

import tkinter
import tkinter.simpledialog
from tkinter import PhotoImage
from minesweeper import Minesweeper
from os.path import join, exists
import time
import threading
import pickle

class MinesweeperGUI(tkinter.Tk):
                    
    def __init__(self):
        """Creates the minesweeper game with buttons."""
        super().__init__()
        
  
        
        # Images dictionary to have one PhotoImage per file
        self.images = {
            "!" : PhotoImage(file = join("images","flag.png")),
            "*" : PhotoImage(file = join("images","bomb.png")),
            " " : PhotoImage(file = join("images","empty.png")),
            "?" : PhotoImage(file = join("images","unknown.png")),
            "X" : PhotoImage(file = join("images","explode.png")),
            "." : PhotoImage(file = join("images","smile.png")),
            "S" : PhotoImage(file = join("images","scared.png")),
            "W" : PhotoImage(file = join("images","win.png")),
            "L" : PhotoImage(file = join("images","dead.png"))
        }
        
        for i in range(1, 9):
            self.images[str(i)] = PhotoImage(file = join("images",
                                                        f"{i}.png"))
        
        # Size is 10 x 10
        self.size = 10
        
        # Starts with 10 mines
        self.mines = 10
        
        self.timer = 0
        self.timerGo = False        
        
        # Create a minesweeper game and set the size appropriately
        self.game = Minesweeper(size=self.size, mines=self.mines)
        
        # Window Stuff
         
        self.title("Minesweeper!")
        self.resizable(False, False)
        
        # Emote to react to your clicks
        self.emote = tkinter.Label(self, text="")
        self.emote.grid(row=0, column=self.game.num_columns//2)
        self.emote["image"] = self.images["."]
        
        # Label to show how many mines are in the board
        self.numMines = tkinter.StringVar(self, f"Mines: {self.mines}")
        minesLabel = tkinter.Label(self, textvariable=self.numMines)
        minesLabel.grid(row=0, column=0, columnspan=3)

        self.time = tkinter.StringVar(self, f"Time: {self.formatTime()}")
        timerLabel = tkinter.Label(self, textvariable=self.time)
        timerLabel.grid(row=0, column= self.game.num_columns//2-2, columnspan=2)

        # Label to show how many unflagged mines are left.
        self.unflaggedMines = tkinter.StringVar(self,
                                                f"Unflagged Mines: {self.mines-self.game.total_flags}")
        umLabel = tkinter.Label(self, textvariable=self.unflaggedMines)
        umLabel.grid(row=0, column= self.game.num_columns -3, columnspan=3)
  
        # Create size x size buttons for the game
        
        self.boardButtons = []
        row=0
        for row in range(self.game.size):
            self.boardButtons.append([])
            for column in range(self.game.size):
                button = tkinter.Button(self,
                                        text = "",
                        command=lambda r=row, c=column: self.nextMove(r, c))
                button["foreground"] = "black"
                button["background"] = "white"
                
                # For face animations
                button.bind("<ButtonPress-1>",
                            lambda e: self.pressClick())
                button.bind("<ButtonRelease-1>",
                            lambda e: self.releaseClick())
                
                # Right click binding
                button.bind("<ButtonRelease-2>",
                            lambda e, r=row, c=column: self.flag(r, c))
                button.bind("<ButtonRelease-3>",
                            lambda e, r=row, c=column: self.flag(r, c))
                
                button.grid(row = row+1, column = column)
                self.boardButtons[-1].append(button)

                
        # Update the view   
        self.setButtons()
        
        # Add a new game button
        self.newGameButton = tkinter.Button(self,
                                            text    = "New Game",
                                            command = self.newGame,
                                            state   = tkinter.DISABLED)
        self.newGameButton.grid(row        = self.game.size + 1,
                                column     = self.game.size -2,
                                columnspan = 2)
        
        # Add a button for changing the total number of mines
        self.changeMinesButton = tkinter.Button(self,
                                                text    = "Change Number of Mines",
                                                command = self.changeMines,
                                                state   = tkinter.NORMAL)
        self.changeMinesButton.grid(row       = self.game.size+1,
                                    column    = 0,
                                    columnspan= 4)
     
    def timerFunc(self):
        while self.timerGo:
            self.timer += 1
            self.time.set(f"Time: {self.formatTime()}")
            time.sleep(1)
    
    def formatTime(self):
        sec     = self.timer % 60
        minutes = self.timer // 60
        return f"{minutes}:{sec:02}"
 
    
    # For the emoticon at the top
    def pressClick(self):
        if not self.game.isGameOver():
            self.emote["image"] = self.images["S"]
        
        if not self.timerGo:
            self.timerGo = True
            self.timerThread = threading.Thread(target=self.timerFunc)
            self.timerThread.start()
          
    def releaseClick(self):
        if not self.game.isGameOver():
            self.emote["image"] = self.images["."]
    
    def changeMines(self):
        """For changing the total number of mines.
        Will call newGame() to reset the board."""
        numMines = tkinter.simpledialog.askinteger("Number of Mines",
                                   "How many mines?")
        if numMines:
          self.mines = max(1,min(self.size**2 - 1,int(numMines)))
          self.numMines.set(f"Mines: {self.mines}")
          self.newGame()
          
    def setButtons(self):
        """Sets the buttons' text based on the state of the game."""
        for row in range(self.game.size):
            for col in range(self.game.size):
                img = self.images[str(self.game.getAt(row, col))]
                self.boardButtons[row][col]["image"] = img
                 
        self.unflaggedMines.set(f"Unflagged Mines: {self.game.minesRemaining()}")
       
    def flag(self, row, column):
        """Called when right-click is pressed on a button."""
        if self.timerGo:
            self.game.flag(row, column)
            self.setButtons()
 
    def nextMove(self, row, column):
        """Makes a move in the game and updates the view with
        the results."""
        if self.game.isGameOver():
            return
        
        # Update the model and view
        self.game.step(row, column)
        self.setButtons()
        
        # Detect game over
        if self.game.isGameOver():
            self.timerGo = False
            # Show all the tiles and update view
            self.game.showAll()
            self.setButtons()
            
            # Detect endgame state
            if self.game.isExploded():
                text = "You lost!"
                self.emote["image"] = self.images["L"]
            else:
                text = f"You won!\nFinal time: {self.formatTime()}"
                self.emote["image"] = self.images["W"]
                
            tkinter.messagebox.showinfo("Game Is Over!", text)
            
            # Enable new game button
            self.newGameButton["state"] = "normal"


    def saveHighScores(self, highScores):
        with open("highScores.pkl", "wb") as file:
            pickle.dump(highScores, file)

    def viewHighScores(self):
        try:
            with open("highScores.pkl", "rb") as file:
                highScores = pickle.load(file)
        except FileNotFoundError:
            highScores = []

        highScores.sort(key=lambda x: (x['mines'], x['time']))

        if not highScores:
            messagebox.showinfo("High Scores", "No high scores available")
            return

        scoreStr = "\n".join([f"Mines: {score['mines']}, Time: {score['time']}" for score in highScores])
        messagebox.showinfo("High Scores", scoreStr)
    
 
    def newGame(self):
        """Create a new minesweeper game and updates the view."""
        self.game = Minesweeper(size=self.size, mines=self.mines)
        self.timer = 0
        self.time.set(f"Time: {self.formatTime()}")
        self.setButtons()  
        self.emote["image"] = self.images["."]

        self.newGameButton["state"] = "disabled"      
        for buttonRow in self.boardButtons:
            for b in buttonRow:
                b["state"] = "normal"

        if self.timerGo:
            self.timerGo = False
            elapsedTime = self.formatTime()

            try:
                with open("highScores.pkl", "rb") as file:
                    high_scores = pickle.load(file)
            except FileNotFoundError:
                high_scores = []

            highScores.append({"mines": self.mines, "time": elapsed_time})
            highScores.sort(key=lambda x: (x['mines'], x['time']))
            highScores = high_scores[:10] 

            self.saveHighScores(highScores)


        def __init__(self):

            self.viewHighScoresButton = tkinter.Button(self, text="View High Scores",command=self.viewHighScores)
            self.viewHighScoresButton.grid(row=self.game.size + 1, column=self.game.size - 4, columnspan=4)

    

def main():
   app = MinesweeperGUI()
   app.mainloop()
   
   app.timerGo = False

if __name__ == "__main__":
   main()
