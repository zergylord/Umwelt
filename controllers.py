from collutil import *
from entities import *
from game import *
from cocos import tiles,actions
import numpy as np
import globals as g
from enemies import *

class SpriteController(actions.Action,tiles.RectMapCollider):
  MOVE_SPEED = 1
  up,left,down,right,run,shoot = (0,0,0,0,0,0)
  def start(self):
    self.target.velocity = (0,0)
    self.shootTimer = 0
    #self.heading = np.array((1,0))
  def step(self,dt):
    dx,dy = self.target.velocity
    pos = self.target.position
    curCell = g.tilemap.get_at_pixel(pos[0],pos[1])
    if 'speed' in curCell.tile.properties:
      terr = curCell.tile.properties['speed']
    else:
      terr = 100
    #use dt and player facing
    if self.shoot and self.shootTimer <= 0:
        bullet = Projectile(g.world,self.target.position+self.target.heading*40,16)
        g.world.add(bullet)
        g.world.collobjs.add(bullet)
        #bullet.do(RandomController())
        bullet.do(MyMoveTo(self.target.position+self.target.heading*500,1))
        self.shootTimer = 100
    else:
        self.shootTimer -= 1
    dx = (1+self.run*2)*terr*(self.right - self.left) * self.MOVE_SPEED * dt
    dy = (1+self.run*2)*terr*(self.up - self.down) * self.MOVE_SPEED * dt
    self.target.movementUpdate(dx,dy)
    '''if dx != 0 or dy != 0:
      if dy > 0: #moving up
        self.heading = np.array((0,1))
        self.target.image = self.target.image_seq[1]
        if abs(dx) - abs(dy) > 0:#left
          self.heading = np.array((-1,0))
          self.target.image = self.target.image_seq[2]
          if dx > 0: #moving right
            self.heading = np.array((1,0))
            self.target.image = self.target.image.get_transform(flip_x=True)
      else:#moving down
        self.heading = np.array((0,-1))
        self.target.image = self.target.image_seq[0]
        if abs(dx) - abs(dy) > 0:#left
          self.heading = np.array((-1,0))
          self.target.image = self.target.image_seq[2]
          if dx > 0:#right
            self.heading = np.array((1,0))
            self.target.image = self.target.image.get_transform(flip_x=True)
    '''
    self.target.dx = dx
    self.target.dy = dy
    '''#check for slow property
    #get players bounding rectangle
    last = self.target.get_rect()
    new = last.copy()
    new.x += dx
    new.y += dy

    #collider
    dx, dy = self.target.velocity = self.collide_map(g.tilemap,last,new,dy,dx)
    
    #position is the sprite's center
    self.target.last = self.target.position
    self.target.cshape.center = new.center
    '''
class ActorController(SpriteController, tiles.RectMapCollider):
    controlCooldown = 2
    curConCool = controlCooldown
    def step(self,dt): 
        super(ActorController,self).step(dt)
        #check input
        self.run = g.keyboard[key.LCTRL] 
        self.shoot = g.keyboard[key.SPACE]
        self.right = g.keyboard[key.RIGHT]
        self.left = g.keyboard[key.LEFT]
        self.up = g.keyboard[key.UP]
        self.down = g.keyboard[key.DOWN]
        if not isinstance(self.target,BasicEnemy):
            g.scroller.set_focus(self.target.x,self.target.y)
            self.curConCool -= dt
            if self.curConCool <= 0 and g.keyboard[key.C]:
                self.curConCool = self.controlCooldown
                self.target.state = 'control_target'
                print 'im controling!'

class RandomController(SpriteController, tiles.RectMapCollider):
    decisionTime = 2
    decisionTimeLeft = decisionTime
    def step(self,dt):
        super(RandomController,self).step(dt)
        self.run = 0 
        self.shoot = 1
        self.decisionTimeLeft -= dt
        if self.decisionTimeLeft <= 0: #change move
            self.decisionTimeLeft = self.decisionTime 
            move = np.random.randint(4)
            self.right = move == 0
            self.left = move == 1
            self.up = move == 2
            self.down = move == 3
