import cocos
import globals as g
from cocos import tiles
import cocos.euclid as eu 
import cocos.collision_model as cm
import pyglet.image
from entities import CSprite


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
