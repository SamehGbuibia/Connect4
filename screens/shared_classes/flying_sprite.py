
import arcade


class FlyingSprite(arcade.Sprite):  
    position_y=0 
    def copyFromSprite(self,sprite:arcade.Sprite) :
        self.texture = sprite.texture
        self.left=sprite.left
        self.right=sprite.right
        self.center_x=sprite.center_x
        self.top=sprite.top
        self.bottom=sprite.bottom
        self.center_y=sprite.center_y
    def update(self):
        super().update()
        if self.center_y <= self.position_y :
            self.change_y=0