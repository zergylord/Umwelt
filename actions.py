from cocos import actions
import numpy as np
import globals as g
from collutil import *
def Patrol(pos1,pos2,speed):
    dist = pow(pow(pos1[0]-pos2[0],2)+pow(pos1[1]-pos2[1],2),.5) 
    return actions.Repeat(
        MyMoveTo(pos1,dist/speed) +
        MyMoveTo(pos2,dist/speed)
        )
class ShootAtEnemy(actions.base_actions.IntervalAction):
  spos = 0
  #work around since Init can't handle pointers
  def initVars(self,enemy):
    self.enemy = enemy
    self.heading = np.array((0,1))
  def init(self,dur):
      self.duration = dur
  def start(self):
      pass
  def update(self,t):
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
        bullet.do(MyMoveTo(self.target.position+exactHead*500,1))
        self.target.shootTimer = 100
    else:
        self.target.shootTimer -= 1
'''depreciated
class MyMoveToWhileShooting(actions.base_actions.IntervalAction, tiles.RectMapCollider):
  spos = 0
  def __init__(self,tpos,dur):
    super(MyMoveToWhileShooting,self).__init__()
    self.tpos = np.array(tpos)
    self.duration = dur
    self.heading = np.array((0,1));
  def start(self):
      self.spos = np.array(self.target.position)
      self.delta = self.tpos - self.spos 
      dx = self.delta[0]
      dy = self.delta[1]
      if dy > 0: #moving up
        self.heading = np.array((0,1))
        #self.target.image = self.target.image_seq[1]
        if abs(dx) - abs(dy) > 0:#left
          self.heading = np.array((-1,0))
          #self.target.image = self.target.image_seq[2]
          if dx > 0: #moving right
            self.heading = np.array((1,0))
            #self.target.image = self.target.image.get_transform(flip_x=True)
      else:#moving down
        self.heading = np.array((0,-1))
        #self.target.image = self.target.image_seq[0]
        if abs(dx) - abs(dy) > 0:#left
          self.heading = np.array((-1,0))
          #self.target.image = self.target.image_seq[2]
          if dx > 0:#right
            self.heading = np.array((1,0))
            #self.target.image = self.target.image.get_transform(flip_x=True)
  def update(self,t):
    shoot = True
    if shoot and self.target.shootTimer <= 0:
        bullet = Projectile(g.world,self.target.position+self.heading*40,16)
        g.world.add(bullet)
        g.world.collobjs.add(bullet)
        #bullet.do(RandomController())
        bullet.do(MyMoveTo(self.target.position+self.heading*500,1))
        self.target.shootTimer = 100
    else:
        self.target.shootTimer -= 1
    pos = self.target.position
    dx,dy = (self.spos + self.delta*t) - pos

    #check for slow property
    #get players bounding rectangle
    last = self.target.get_rect()
    new = last.copy()
    new.x += dx
    new.y += dy

    #map collider
    dx, dy = self.collide_map(g.tilemap,last,new,dy,dx)

    #position is the sprite's center
    self.target.last = self.target.position
    self.target.cshape.center = new.center'''
class MyMoveTo(actions.base_actions.IntervalAction):
  spos = 0
  def __init__(self,tpos,dur):
    super(MyMoveTo,self).__init__()
    self.tpos = np.array(tpos)
    self.duration = dur
    self.lastT = 0
  def start(self):
      self.spos = np.array(self.target.position)
      self.delta = self.tpos - self.spos 
  def update(self,t):
    dt = self.lastT - t #hack to use dt
    self.lastT = t
    pos = self.target.position
    #dx,dy = (self.spos + self.delta*t) - pos
    dx,dy = -self.delta*dt
    self.target.movementUpdate(dx,dy)

    #check for slow property

    self.target.dx = dx
    self.target.dy = dy

