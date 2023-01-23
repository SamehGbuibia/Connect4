import arcade
from logic.game_logic import GameLogic

from resources.constents import *
from screens.shared_classes.flying_sprite import FlyingSprite
from screens.welcome_screen import WelcomeScreen

class MainScreen(arcade.Window):
    def __init__(self,game_logic:GameLogic):
        self.game_logic = game_logic
        self.spirateList = arcade.SpriteList()
        self.tokens = []
        self.buttons = []
        self.spirateListCordination = []
        self.isHomePressed = False
        self.isWinSoundNotPlayed = True
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Main Screen Connect4 (Press any key from 1 to 7 to play)")

    def setup(self):
        self.token_sound = arcade.load_sound(TOKEN_SOUND_PATH)
        self.win_sound = arcade.load_sound(WIN_SOUND_PATH)
        arcade.set_background_color((12,55,205))
        self.tokens = [arcade.Sprite(RED_TOKEN_PATH, TOKEN_TURN_SCALE),
                  arcade.Sprite(YELLOW_TOKEN_PATH,TOKEN_TURN_SCALE ) ]
        self.buttons = [arcade.Sprite(HOME_BUTTON_PATH, TOKEN_TURN_SCALE),
                  arcade.Sprite(RESET_BUTTON_PATH,TOKEN_TURN_SCALE ) ]
        for i in range(len(self.buttons)):
            self.buttons[i].center_x=25
            self.buttons[i].center_y=SCREEN_HEIGHT-75-i*40
            self.buttons[i].draw
        self.spirateList.draw()
        
    def on_draw(self):
        arcade.start_render()
        for i in range(GRILLE_ROWS):
            for j in range(GRILLE_COLS):
                if(GRILLE[i][j]==0):
                    arcade.draw_circle_filled(CELL_SIZE+CELL_SIZE*j,50+i*CELL_SIZE,40,arcade.color.WHITE)
                else:
                    if(GRILLE[i][j]==1):
                        token = FlyingSprite(RED_TOKEN_PATH, TOKEN_SCALE)
                    elif(GRILLE[i][j]==2):
                        token = FlyingSprite(YELLOW_TOKEN_PATH, TOKEN_SCALE)
                    token.center_x=CELL_SIZE+CELL_SIZE*j
                    token.center_y=SCREEN_HEIGHT
                    token.position_y= 50+i*CELL_SIZE
                    token.change_y=-20
                    if(not((token.center_x,token.position_y)in self.spirateListCordination)):
                        self.spirateListCordination.append((token.center_x,token.position_y))
                        self.spirateList.append(token)
        for j in range(7):
            arcade.draw_text(j+1,CELL_SIZE-5+j*CELL_SIZE,SCREEN_HEIGHT-25)
        isYelloTokenTurn = (self.game_logic.player1Turn and not self.game_logic.isTokenRed) or (not self.game_logic.player1Turn and self.game_logic.isTokenRed)
        self.tokens[isYelloTokenTurn].center_x=25
        self.tokens[isYelloTokenTurn].center_y=SCREEN_HEIGHT-25
        self.tokens[isYelloTokenTurn].draw()   
        for i in range(len(self.buttons)):
            self.buttons[i].draw()
        
        self.spirateList.draw() 
        if(self.game_logic.winner!=0):
            arcade.draw_line(CELL_SIZE+CELL_SIZE*self.game_logic.winnerCordination[0][1],
                             50+self.game_logic.winnerCordination[0][0]*CELL_SIZE,
                             CELL_SIZE+CELL_SIZE*self.game_logic.winnerCordination[1][1],
                             50+self.game_logic.winnerCordination[1][0]*CELL_SIZE
                             ,arcade.color.GREEN,7)
            if(self.isWinSoundNotPlayed):
                self.isWinSoundNotPlayed = False
                arcade.play_sound(self.win_sound)
    
    def on_key_press(self, symbol, modifiers):
        if(self.game_logic.winner==0):
            if symbol in range(arcade.key.NUM_1,arcade.key.NUM_1+GRILLE_COLS):
                if(self.game_logic.add_Token(symbol-arcade.key.NUM_1)):
                    self.game_logic.player1Turn = not self.game_logic.player1Turn
                    arcade.play_sound(self.token_sound)
            elif symbol in range(arcade.key.KEY_1,arcade.key.KEY_1+GRILLE_COLS):
                if(self.game_logic.add_Token(symbol-arcade.key.KEY_1)):
                    self.game_logic.player1Turn = not self.game_logic.player1Turn
                    arcade.play_sound(self.token_sound)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        home_start_x = int(self.buttons[0].left)
        home_end_x = int(self.buttons[0].left+self.tokens[0].width)
        home_start_y = int(self.buttons[0].bottom)
        home_end_y = int(self.buttons[0].bottom+self.tokens[0].height)
        reset_start_x = int(self.buttons[1].left)
        reset_end_x = int(self.buttons[1].left+self.tokens[1].width)
        reset_start_y = int(self.buttons[1].bottom)
        reset_end_y = int(self.buttons[1].bottom+self.tokens[1].height)
        if(x in range(home_start_x,home_end_x) 
           and y in range(home_start_y,home_end_y)):
            self.isHomePressed = True
            self.on_close()
            
        if(x in range(reset_start_x,reset_end_x) 
           and y in range(reset_start_y,reset_end_y)):
            self.game_logic.reset()
            self.spirateList.clear()
            self.tokens = []
            self.buttons = []
            self.spirateListCordination = []
            self.setup()
            self.isWinSoundNotPlayed = True
        return super().on_mouse_press(x, y, button, modifiers)
    
    def on_close(self):
        super().on_close()
        if(self.isHomePressed):
            app = WelcomeScreen()
            app.setup()
            arcade.run()
    
    def on_update(self, delta_time: float):
        self.game_logic.check_winner()
        self.spirateList.update()
