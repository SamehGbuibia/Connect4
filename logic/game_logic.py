import random
from resources.constents import *


class GameLogic:
    def __init__(self,isPlayer1Mode,isTokenRed ) :
        self.isPlayer1Mode = isPlayer1Mode
        self.isTokenRed = isTokenRed
        self.reset()
        
    def reset(self):
        self.player1Turn = True
        self.winner=0
        self.winnerCordination = ()
        for i in range(GRILLE_ROWS):
            for j in range(GRILLE_COLS):
                GRILLE[i][j]=0
        
    def add_Token(self, column: int) -> bool:
            isTokenAdded = False
            for i in range(GRILLE_ROWS):
                if(GRILLE[i][column]==0):
                    if((self.player1Turn and self.isTokenRed) or(not self.player1Turn and not self.isTokenRed)):
                        GRILLE[i][column]=1
                    else :
                        GRILLE[i][column]=2
                    isTokenAdded = True
                    break
            if(isTokenAdded and self.player1Turn and self.isPlayer1Mode):
                self.player1Turn = not self.player1Turn
                while(not self.add_Token(random.randint(0, GRILLE_COLS-1))): None
            return isTokenAdded
    def check_winner(self):      
        if((self.isTokenRed and self.winner!=1) or (not self.isTokenRed and self.winner!=2)):                  
            for i in range(GRILLE_ROWS//2):
                for j in range(GRILLE_COLS//2+1):
                    if GRILLE[i][j]!= 0 and GRILLE[i][j]== GRILLE[i+1][j+1] == GRILLE[i+2][j+2] == GRILLE[i+3][j+3]:
                        self.winner= GRILLE[i][j]
                        self.winnerCordination = ((i,j),(i+3,j+3))
                        break
            for i in range(GRILLE_ROWS//2):
                for j in range(GRILLE_COLS//2+1):
                    if GRILLE[i+3][j]!= 0 and GRILLE[i+3][j] == GRILLE[i+2][j+1] == GRILLE[i+1][j+2] == GRILLE[i][j+3]:
                        self.winner= GRILLE[i+3][j]
                        self.winnerCordination = ((i+3,j),(i,j+3))
                        break

            for i in range(GRILLE_ROWS):
                for j in range(GRILLE_COLS//2+1):
                    if GRILLE[i][j]!= 0 and GRILLE[i][j] == GRILLE[i][j+1] == GRILLE[i][j+2] == GRILLE[i][j+3]:
                        self.winner= GRILLE[i][j]
                        self.winnerCordination = ((i,j),(i,j+3))
                        break
        
            for i in range(GRILLE_ROWS//2):
                for j in range(GRILLE_COLS):
                    if GRILLE[i][j]!= 0 and GRILLE[i][j] == GRILLE[i+1][j] == GRILLE[i+2][j] == GRILLE[i+3][j]:
                        self.winner= GRILLE[i][j]
                        self.winnerCordination = ((i,j),(i+3,j))
                        break
        