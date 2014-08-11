import cocos
import globals as g
from cocos import tiles
import cocos.euclid as eu 
import cocos.collision_model as cm
import pyglet.image

class CSprite(cocos.sprite.Sprite,tiles.RectMapCollider):
    speed = 100
    def __init__(self,image,center_x,center_y,radius):
        super(CSprite,self).__init__(image)
        self.dx = 0
        self.dy = 0
        self.state = 'norm'
        self.position = (center_x,center_y)
        self.last = (center_x,center_y)
        self.cshape = cm.AARectShape(eu.Vector2(center_x,center_y),radius,radius)
    def update(self,dt):
        """check for object collision, if not then apply movement and check for
        grid collision"""
        #object collider
        if self.state == 'coll':
            self.state = 'norm'
            self.cshape.center = self.position #revert collision body back to prev pos
        else:
            self.position = self.cshape.center #accept collision body as the new pos
            #map collider
            last = self.get_rect()
            new = last.copy()
            new.x += self.dx
            new.y += self.dy
            self.collide_map(g.tilemap,last,new,self.dy,self.dx)
            self.dx = 0
            self.dy = 0

            #---position is the sprite's center
            self.last = self.position
            self.cshape.center = new.center
            #self.position = self.cshape.center
        
class Projectile(CSprite):
    damage = 25
    def __init__(self,world,pos,radius):
        man = pyglet.image.load('man.png')
        seq =  pyglet.image.ImageGrid(man,1,4)
        image = seq[0]
        super(Projectile,self).__init__(image,pos[0],pos[1],radius)
        self.world = world
        self.speed = 1000
    """for consistancy with Beings who use actions to update heading"""
    def movementUpdate(self,dx,dy):
        pass
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
            #self.position = self.cshape.center
            #map collider
            last = self.get_rect()
            new = last.copy()
            new.x += self.dx
            new.y += self.dy
            curDelta = (self.dx,self.dy)
            dx,dy = self.collide_map(g.tilemap,last,new,self.dy,self.dx)
            self.dx = 0
            self.dy = 0
            #if collision, then dx or dy would be modified
            if curDelta[0] != dx or curDelta[1] != dy:
                self.state = 'kill'
                self.stop()
                print 'died from environment'
            else:
                #---position is the sprite's center
                self.last = self.position
                self.cshape.center = new.center
                self.position = self.cshape.center


