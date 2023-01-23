import arcade
from logic.game_logic import GameLogic

from resources.constents import *
from screens.shared_classes.flying_sprite import FlyingSprite


class WelcomeScreen(arcade.Window):   
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,"Welcome To Connect4")
        self.counter=0
        self.spriteList = arcade.SpriteList()
        self.tokens = [arcade.Sprite(RED_TOKEN_PATH, TOKEN_SCALE),
                  arcade.Sprite(YELLOW_TOKEN_PATH,TOKEN_SCALE ) ]
        self.name="CONNECT4"
        self.modeTirangleCenter_x=SCREEN_WIDTH/4+75
        self.modeTirangleCenter_y=SCREEN_HEIGHT/2-70+50
        self.isPlayer1Mode = True
        self.isTokenRed = True
        self.isPlayPressed = False
    
    def _add_Lettre(self, delta_time: float):
        if(self.counter<len(self.name)): 
            sprite = arcade.create_text_sprite(self.name[self.counter],SCREEN_WIDTH/4+self.counter*50,SCREEN_HEIGHT,font_size=SCREEN_HEIGHT/10,color=arcade.color.ALLOY_ORANGE)
            flyingSprite = FlyingSprite()
            flyingSprite.copyFromSprite(sprite)
            flyingSprite.change_y=-5
            flyingSprite.position_y = SCREEN_HEIGHT/2+50
            self.spriteList.append(flyingSprite)
            self.counter+=1
            
    def _add_buttons(self,delta_time: float):
        if(self.counter==len(self.name)):
            player1 = arcade.create_text_sprite("1 Player",SCREEN_WIDTH/4+25,SCREEN_HEIGHT/2-100+50,font_size=SCREEN_HEIGHT/30,color=arcade.color.ALLOY_ORANGE)
            self.spriteList.append(player1)
            player2 = arcade.create_text_sprite("2 Player",SCREEN_WIDTH/4+275,SCREEN_HEIGHT/2-100+50,font_size=SCREEN_HEIGHT/30,color=arcade.color.ALLOY_ORANGE)
            self.spriteList.append(player2)
            text = arcade.create_text_sprite("Press a Token to choose your color and start the game",SCREEN_WIDTH/4-100,SCREEN_HEIGHT/2-175+50,font_size=SCREEN_HEIGHT/30,color=arcade.color.ALLOY_ORANGE)
            self.spriteList.append(text)
            self.tokens[0].center_x=SCREEN_WIDTH/4+70
            self.tokens[1].center_x=SCREEN_WIDTH/4+320
            for token in self.tokens:
                token.center_y=SCREEN_HEIGHT/2-175
                self.spriteList.append(token)
            self.counter+=1
        
    def setup(self):
        arcade.schedule(self._add_Lettre, 0.3)
        arcade.schedule(self._add_buttons, 4)
        arcade.set_background_color(arcade.color.ANDROID_GREEN)
        
    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_text("Welcome To",SCREEN_WIDTH/5,(SCREEN_HEIGHT/5)*3+50,font_size=SCREEN_HEIGHT/10)
        self.spriteList.draw()
        if(self.counter>len(self.name)):
            arcade.draw_triangle_filled(x1=self.modeTirangleCenter_x,y1=self.modeTirangleCenter_y,x2=self.modeTirangleCenter_x-10,
                                            y2=self.modeTirangleCenter_y+15,x3=self.modeTirangleCenter_x+10,y3=self.modeTirangleCenter_y+15,color=arcade.color.ALLOY_ORANGE)
            
        arcade.finish_render() 
        
    def on_update(self, delta_time: float):
        
        self.spriteList.update()
        return super().on_update(delta_time)
    
    def on_key_press(self, symbol: int, modifiers: int):
        if(symbol == arcade.key.LEFT):
            if(not(self.isPlayer1Mode)):
                self.isPlayer1Mode=not self.isPlayer1Mode
                self.modeTirangleCenter_x-=250
        if(symbol==arcade.key.RIGHT):
            if(self.isPlayer1Mode):
                self.isPlayer1Mode=not self.isPlayer1Mode
                self.modeTirangleCenter_x+=250
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        red_token_start_x = int(self.tokens[0].left)
        red_token_end_x = int(self.tokens[0].left+self.tokens[0].width)
        red_token_start_y = int(self.tokens[0].bottom)
        red_token_end_y = int(self.tokens[0].bottom+self.tokens[0].height)
        yellow_token_start_x = int(self.tokens[1].left)
        yellow_token_end_x = int(self.tokens[1].left+self.tokens[1].width)
        yellow_token_start_y = int(self.tokens[1].bottom)
        yellow_token_end_y = int(self.tokens[1].bottom+self.tokens[1].height)
        if(x in range(red_token_start_x,red_token_end_x) 
           and y in range(red_token_start_y,red_token_end_y)):
            self.isPlayPressed = True
            self.on_close()
            
        if(x in range(yellow_token_start_x,yellow_token_end_x) 
           and y in range(yellow_token_start_y,yellow_token_end_y)):
            self.isTokenRed = False
            self.isPlayPressed = True
            self.on_close()
        return super().on_mouse_press(x, y, button, modifiers)
        
    def on_close(self):
        super().on_close()
        if(self.isPlayPressed):
            game_logic = GameLogic(isPlayer1Mode=self.isPlayer1Mode,isTokenRed=self.isTokenRed)
            app = MainScreen(game_logic=game_logic)
            app.setup()
            arcade.run()
from screens.main_screen import MainScreen