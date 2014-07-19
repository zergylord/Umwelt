import cocos
import cocos.euclid as eu
import cocos.collision_model as cm

class CSprite(cocos.sprite.Sprite):
    def __init__(self,image,center_x,center_y,radius):
        super(CSprite,self).__init__(image)
        self.state = 'norm'
        self.position = (center_x,center_y)
        self.cshape = cm.CircleShape(eu.Vector2(center_x,center_y),radius)
    def update(self,dt):
        self.cshape.center = eu.Vector2(self.x,self.y)
