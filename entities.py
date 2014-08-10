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
    """fundamental entity that has a sprite seequence
    hp, and a heading
    """
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
class Hero(Being):
    def __init__(self,image,pos):
        super(Hero,self).__init__(image,pos,16)
class SightBox():
    """ fundamental entity that isn't rendered and is currently used
    for line of sight via object collision.
    """
    def __init__(self,owner,enemy,hWidth,hHeight):
        self.state = 'norm'
        self.active = False
        self.sightWidth = hWidth #off dimension size
        self.sightLength = hHeight #main dimension size (normally bigger)
        self.owner = owner
        self.enemy = enemy
        self.cshape = cm.AARectShape(self.owner.position+self.owner.heading*self.sightLength,
                self.sightWidth + abs(self.owner.heading[0])*self.sightLength,
                self.sightWidth + abs(self.owner.heading[1])*self.sightLength)
    def __updatePosition__(self):
        self.cshape = cm.AARectShape(self.owner.position+self.owner.heading*self.sightLength,
                self.sightWidth + abs(self.owner.heading[0])*self.sightLength,
                self.sightWidth + abs(self.owner.heading[1])*self.sightLength)
    def update(self,dt):
        self.__updatePosition__()
        self.active = self.owner.bState == 'looking'
        if self.active:
            #print 'active sight!'
            if self.state == 'foundEnemy':
                self.state = 'notFoundEnemy'
                self.owner.bState = 'alert'
                print 'I see you!'

class SightLimitBox(SightBox):
    """same as the sightbox, but sets owners state from alert to normal once the enemy
    ISNT colliding with it. Typically used in conjunction with a smaller sightbox to determine
    when the owner has lost track of its enemy
    """
    timeLost = 0
    def update(self,dt):
        self.__updatePosition__()
        
        self.active = self.owner.bState == 'attacking'
        if self.active:
            #print 'active sight limit!'
            if self.state == 'foundEnemy':
                self.state = 'notFoundEnemy' #collision must set foundEnemy everyframe
            else:
                self.timeLost += 1
                #TODO:have this activate 'searching' behavior
                print 'where are you?'
                if self.timeLost >= 10:
                    self.timeLost = 0
                    self.owner.bState = 'unalert'
                    print 'I lost you! :-('

