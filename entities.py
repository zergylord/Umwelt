from skills import *
from cocos import collision_model as cm
import numpy as np
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
    for line of sight via object collision. Only uses 4 directional
    heading since collision only supports axis alligned Rects
    """
    def __init__(self,owner,enemy,hWidth,hHeight):
        self.state = 'norm'
        self.active = False
        self.sightWidth = hWidth #off dimension size
        self.sightLength = hHeight #main dimension size (normally bigger)
        self.owner = owner
        self.enemy = enemy
        self.__updatePosition__()
    def __updatePosition__(self):
        self.cshape = cm.AARectShape(self.owner.position+self.owner.heading*self.sightLength,
                abs(self.owner.heading[1])*self.sightWidth 
                + abs(self.owner.heading[0])*self.sightLength,
               abs(self.owner.heading[0])*self.sightWidth 
               + abs(self.owner.heading[1])*self.sightLength)
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

