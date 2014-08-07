from collutil import *
from cocos import collision_model as cm
import numpy as np
class HasHeading():
    """Interface that gives a class a heading property, and
    the ability to recalculate heading given dx,dy
    A class must inherent this if it wants to use sight boxes,etc."""
    heading = np.array((1,0))
    def changeHeading(self,dx,dy):
        if dy != 0 or dx != 0:
            if dy > 0: #moving up
                self.heading = np.array((0,1))
                if abs(dx) - abs(dy) > 0:#left
                  self.heading = np.array((-1,0))
                  if dx > 0: #moving right
                    self.heading = np.array((1,0))
            else:#moving down
                self.heading = np.array((0,-1))
                if abs(dx) - abs(dy) > 0:#left
                  self.heading = np.array((-1,0))
                  if dx > 0:#right
                    self.heading = np.array((1,0))
    
class Being(CSprite,HasHeading):
    maxHealth = 100
    health = maxHealth
    image_seq = ()
    def __init__(self,image_seq,pos,radius):
        self.image_seq = image_seq
        image = image_seq[0]
        super(Being,self).__init__(image,pos[0],pos[1],radius)
    """called by (all?) actions executed by Being"""
    def movementUpdate(self,dx,dy):
        self.changeHeading(dx,dy)
        if all(self.heading == (0,1)):#up
            self.image = self.image_seq[1]
        elif all(self.heading == (-1,0)):#left
            self.image = self.image_seq[2]
        elif all(self.heading == (0,-1)):#down
            self.image = self.image_seq[0]
        elif all(self.heading == (1,0)):#right
            self.image = self.image_seq[2]
            self.image = self.image.get_transform(flip_x=True)
    def update(self,dt):
        super(Being,self).update(dt)
        if not self.state == 'kill' and self.health <= 0:
            self.state = 'kill'
            self.stop()
            print 'I died :-('
    def takeHit(self,damage):
        self.health -= damage
class SightBox():
    def __init__(self,owner,enemy,pos,hWidth,hHeight):
        self.state = 'norm'
        self.cshape = cm.AARectShape(pos,hWidth,hHeight) 
        self.owner = owner
        self.enemy = enemy
    def update(self,dt):
        #heading = np.array((1,0))#placeholder until beings contain their heading
        sightLength = 100 #size of sight field along heading axis
        sightWidth = 30 #size of nondirected portion (e.g. tunnel vision-ness) 
        self.cshape = cm.AARectShape(self.owner.position+self.owner.heading*sightLength,
                sightWidth + abs(self.owner.heading[0])*sightLength,
                sightWidth + abs(self.owner.heading[1])*sightLength)
        #self.cshape.center = self.owner.position
        if self.state == 'foundEnemy':
            self.state = 'colrem'
            self.owner.bState = 'alert'
            print 'I see you!'
