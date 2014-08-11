#Keep using Action or switch to InstantAction and then Repeat?
from cocos import actions
import numpy as np
import globals as g
from collutil import *
def Patrol(pos1,pos2):
    return actions.Repeat(
        MyMoveTo(pos1) +
        MyMoveTo(pos2)
        )
class ShootAtEnemy(actions.base_actions.Action):
    #work around since Init can't handle pointers
    def initVars(self,enemy):
        self.enemy = enemy
        self.heading = np.array((0,1))
    def start(self):
        pass
    def done(self):
        return False
    def step(self,dt):
        dx = self.enemy.position[0] - self.target.position[0]
        dy = self.enemy.position[1] - self.target.position[1]
        self.target.movementUpdate(dx,dy)

        shoot = True
        delta = np.array((dx,dy))
        exactHead = delta/np.linalg.norm(delta)
        if shoot and self.target.shootTimer <= 0:
            bullet = Projectile(g.world,self.target.position+exactHead*50,16)
            g.world.add(bullet)
            g.world.collobjs.add(bullet)
            #bullet.do(RandomController())
            bullet.do(MyMoveTo(self.target.position+exactHead*500))
            self.target.shootTimer = 100
        else:
            self.target.shootTimer -= 1
class FollowBeing(actions.base_actions.Action):
    def initVars(self,tBeing):
        self.tBeing = tBeing
    def start(self):
        pass

    def done(self):
        '''dx = self.tBeing.position[0] - self.target.position[0]
        dy = self.tBeing.position[1] - self.target.position[1]
        return np.linalg.norm((dx,dy)) < .01*self.target.speed
        '''
        #keep following regardless of proximinity
        return False

    def step(self,dt):
        dx = self.tBeing.position[0] - self.target.position[0]
        dy = self.tBeing.position[1] - self.target.position[1]
        delta = np.array((dx,dy))
        exactHead = delta/np.linalg.norm(delta)


        #dx,dy = delta*dt*100 #nice for rubberband following
        dx,dy = exactHead*dt*self.target.speed
        self.target.movementUpdate(dx,dy)

        #check for slow property

        self.target.dx = dx
        self.target.dy = dy
class MyMoveTo(actions.base_actions.Action):
  def __init__(self,tpos):
    super(MyMoveTo,self).__init__()
    self.tpos = np.array(tpos)
  def start(self):
      pass
  #needed since non-interval action
  def done(self):
    delta = self.tpos - self.target.position
    return np.linalg.norm(delta) < .01*self.target.speed

  def step(self,dt):
    delta = self.tpos - self.target.position
    exactHead = delta/np.linalg.norm(delta)

    dx,dy = exactHead*dt*self.target.speed
    self.target.movementUpdate(dx,dy)

    #check for slow property

    self.target.dx = dx
    self.target.dy = dy

