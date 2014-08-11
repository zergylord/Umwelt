from skills import *
from entities import *
from game import *
import globals as g
class BasicEnemy(Being):
    def __init__(self,image,pos):
        self.bState = 'looking'
        self.shootTimer = 100;
        self.controlled = False
        super(BasicEnemy,self).__init__(image,pos,16)
        self.addSkill(SpearThrow())
    def update(self,dt):
        super(BasicEnemy,self).update(dt)
        if self.bState == 'alert':
            self.stop()
            #shoot
            fancyAction = self.do(ShootAtEnemy(50))
            fancyAction.initVars(g.player)
            #follow
            fancyMove = self.do(FollowBeing())
            fancyMove.initVars(g.player)
            self.bState = 'attacking'

        elif self.bState == 'unalert':
            self.stop()
            #TODO: save a patrol route
            #go back to patrol route
            self.do(Patrol((1000,100),(200,100)))
            self.bState = 'looking'

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
