from collutil import *
from entities import *
class BasicEnemy(Being):
    def __init__(self,image,pos):
        self.controlled = False
        super(BasicEnemy,self).__init__(image,pos,16)
    def update(self,dt):
        super(BasicEnemy,self).update(dt)
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
