import cocos
import cocos.euclid as eu 
import cocos.collision_model as cm
import pyglet.image


class CSprite(cocos.sprite.Sprite):
    def __init__(self,image,center_x,center_y,radius):
        super(CSprite,self).__init__(image)
        self.state = 'norm'
        self.position = (center_x,center_y)
        self.last = (center_x,center_y)
        self.cshape = cm.AARectShape(eu.Vector2(center_x,center_y),radius,radius)
    def update(self,dt):
        if self.state == 'coll':
            self.state = 'norm'
        else:
            self.position = self.cshape.center
class Projectile(CSprite):
    damage = 25
    def __init__(self,world,pos,radius):
        man = pyglet.image.load('man.png')
        seq =  pyglet.image.ImageGrid(man,1,4)
        image = seq[0]
        super(Projectile,self).__init__(image,pos[0],pos[1],radius)
        self.world = world
    def update(self,dt):
        if self.state == 'coll':
            self.state = 'kill'
            print 'start kill proc'
            self.stop()
            print 'got here'
            #self.kill()
            #self.world.collobjs.remove(self)
            #self.world.remove(self)
        else:
            self.position = self.cshape.center


