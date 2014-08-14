#TODO: update controllers s.t. being speed is used
from skills import *
from entities import *
from game import *
from cocos import tiles,actions
import numpy as np
import globals as g
from enemies import *

class SpriteController(actions.Action):
  MOVE_SPEED = 1
  up,left,down,right,run,shoot,throwMine,explode = (0,0,0,0,0,0,0,0)
  def start(self):
    self.target.addSkill(SpearThrow())
    self.target.addSkill(MineThrow())
    self.target.addSkill(Explode(96))
    self.target.velocity = (0,0)
  def step(self,dt):
    dx,dy = self.target.velocity
    pos = self.target.position
    curCell = g.tilemap.get_at_pixel(pos[0],pos[1])
    if 'speed' in curCell.tile.properties:
      terr = curCell.tile.properties['speed']
    else:
      terr = 100
    #use dt and player facing
    if self.shoot:
        self.target.skill['sThrow'].use(self.target.position+self.target.heading*500)
    if self.throwMine:
        self.target.skill['mThrow'].use(self.target.position+self.target.heading*500)
    if self.explode:
        self.target.skill['explode'].use()
    dx = (1+self.run*2)*terr*(self.right - self.left) * self.MOVE_SPEED * dt
    dy = (1+self.run*2)*terr*(self.up - self.down) * self.MOVE_SPEED * dt
    self.target.movementUpdate(dx,dy)
    self.target.dx = dx
    self.target.dy = dy
class ActorController(SpriteController):
    controlCooldown = 2
    curConCool = controlCooldown
    def step(self,dt): 
        super(ActorController,self).step(dt)
        #check input
        self.run = g.keyboard[key.LCTRL] 
        self.shoot = g.keyboard[key.SPACE]
        self.throwMine = g.keyboard[key.M]
        self.explode = g.keyboard[key.X]
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

'''DEPRECIATED
class RandomController(SpriteController):
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
'''
