from collutil import *
from cocos import collision_model as cm
import numpy as np
class Being(CSprite):
    maxHealth = 100
    health = maxHealth
    image_seq = ()
    def __init__(self,image_seq,pos,radius):
        self.image_seq = image_seq
        image = image_seq[0]
        super(Being,self).__init__(image,pos[0],pos[1],radius)
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
        heading = np.array((1,0))#placeholder until beings contain their heading
        sightLength = 100 #size of sight field along heading axis
        sightWidth = 30 #size of nondirected portion (e.g. tunnel vision-ness) 
        self.cshape = cm.AARectShape(self.owner.position+heading*sightLength,
                sightWidth + abs(heading[0])*sightLength,
                sightWidth + abs(heading[1])*sightLength)
        '''self.cshape = cm.AARectShape(self.owner.position+self.owner.heading*50,
                30 + self.owner.heading[0]*50,
                30 + self.owner.heading[1]*50)'''
        #self.cshape.center = self.owner.position
        if self.state == 'foundEnemy':
            self.state = 'colrem'
            self.owner.bState = 'alert'
            print 'I see you!'
#how to handle directed sight boxes? probably can't change cshape... 
