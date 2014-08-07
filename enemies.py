from collutil import *
from entities import *
from game import *
import globals as g
class BasicEnemy(Being):
    def __init__(self,image,pos):
        self.bState = 'random'
        self.shootTimer = 100;
        self.controlled = False
        super(BasicEnemy,self).__init__(image,pos,16)
    def update(self,dt):
        super(BasicEnemy,self).update(dt)
        if self.bState == 'alert':
            fancyAction = self.do(ShootAtEnemy(50))
            fancyAction.initVars(g.player)
            self.bState = 'attacking'
        #TODO: add second sight box; stop attaccking when player doesn't collide
        #elif and self.bState == 'attacking'
        if self.state == 'take_control':
            print 'im being controled :-('
            self.controlled = True
            self.state = 'norm'
            self.stop()
            self.do(ActorController())
        elif self.state == 'release_control':
            self.controlled = False
            self.state = 'norm'
            self.stop()
            self.do(RandomController())
class Hero(Being):
    def __init__(self,image,pos):
        super(Hero,self).__init__(image,pos,16)
from controllers import *
