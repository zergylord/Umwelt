from collutil import *
from entities import *
from game import *
import globals as g
class BasicEnemy(Being):
    def __init__(self,image,pos):
        self.curAtk = None
        self.curMov = None
        self.bState = 'looking'
        self.shootTimer = 100;
        self.controlled = False
        super(BasicEnemy,self).__init__(image,pos,16)
    #TODO:override default 'do' function s.t. curAtk/Mov are set automatically
    def update(self,dt):
        super(BasicEnemy,self).update(dt)
        if self.bState == 'alert':
            #shoot
            fancyAction = self.do(ShootAtEnemy(50))
            fancyAction.initVars(g.player)
            self.curAtk = fancyAction
            #follow
            fancyAction = self.do(FollowBeing(100))
            fancyAction.initVars(g.player)
            self.curMov = fancyAction

            self.bState = 'attacking'
        elif self.bState == 'unalert':
            self.remove_action(self.curAtk)
            self.remove_action(self.curMov)
            #TODO: save a patrol route
            #go back to patrol route
            self.curMove = self.do(Patrol((1000,100),(200,100),100))
            self.curAtk = None
            self.bState = 'looking'

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
from controllers import *
