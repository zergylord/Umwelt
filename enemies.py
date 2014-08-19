from skills import *
from entities import *
from game import *
from pyglet.event import EventDispatcher
from cocos.audio.effect import Effect
import globals as g
class BasicEnemy(Being,EventDispatcher):
    def __init__(self,image,pos,patEnd):
        self.noise = .1
        self.lastKnownLoc = [] #when set, will goto here when investigating
        self.patA = pos
        self.patB = patEnd
        self.bState = 'looking'
        self.shootTimer = 100;
        self.controlled = False
        self.alertSound = Effect('Alert.wav')
        super(BasicEnemy,self).__init__(image,pos,16)
        self.team = 1
        for a in g.team[self.team]:
            self.push_handlers(a)#a should recieve my events
            a.push_handlers(self)#I should receive a's events
        g.team[self.team].add(self)
        self.addSkill(SpearThrow())
        self.curMov = self.do(Patrol(self.patB,self.patA,self.noise))
    def on_alert(self,ally):
        '''respond to an ally becoming alert'''
        if self.bState == 'looking':
            self.bState = 'investigating'
            self.lastKnownLoc = ally.position
            print 'your alert!'
    def update(self,dt):
        super(BasicEnemy,self).update(dt)
        if self.bState == 'alert':
            self.alertSound.play()
            self.stop()
            #shoot
            fancyAction = self.do(ShootAtEnemy(50))
            fancyAction.initVars(g.player)
            #follow
            fancyMove = self.do(FollowBeing())
            fancyMove.initVars(g.player)
            self.bState = 'attacking'
            self.dispatch_event('on_alert',self)

        elif self.bState == 'attacking':
            self.lastKnownLoc = g.player.position 

        elif self.bState == 'unalert':
            self.stop()
            if self.lastKnownLoc:
                self.bState = 'investigating'
                self.curMov = self.do(MyMoveTo(self.lastKnownLoc,self.noise))
                print 'investigating!'
            else:
                self.bState = 'uninvestigate'
        elif self.bState == 'investigating':
            if self.curMov.done():
                print 'I give up...'
                self.lastKnownLoc = []
                self.bState = 'uninvestigate'
        elif self.bState == 'uninvestigate':
            self.stop()
            #go back to patrol route
            print 'back to the ole route'
            self.bState = 'looking'
            self.curMov = self.do(Patrol(self.patB,self.patA,self.noise))


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
    def takeHit(self,damage):
        super(BasicEnemy,self).takeHit(damage)
        if self.bState == 'looking':
            self.bState = 'investigating'
#events generated:
BasicEnemy.register_event_type('on_alert')
#don't remember why, but I need this...
from controllers import *
