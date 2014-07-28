import pyglet
from pyglet.window import key

import numpy as np

import cocos
from cocos import tiles,actions,layer
from collutil import *
import cocos.collision_model as cm

class MyMoveTo(actions.base_actions.IntervalAction, tiles.RectMapCollider):
  spos = 0
  def __init__(self,tpos,dur):
    super(MyMoveTo,self).__init__()
    self.tpos = np.array(tpos)
    self.duration = dur
  def start(self):
    self.spos = np.array(self.target.position)
    self.delta = self.tpos - self.spos 
  def update(self,t):
    global tilemap
    pos = self.target.position
    dx,dy = (self.spos + self.delta*t) - pos

    #check for slow property
    #get players bounding rectangle
    last = self.target.get_rect()
    new = last.copy()
    new.x += dx
    new.y += dy

    #map collider
    dx, dy = self.collide_map(tilemap,last,new,dy,dx)

    #position is the sprite's center
    self.target.last = self.target.position
    self.target.cshape.center = new.center
class SpriteController(actions.Action,tiles.RectMapCollider):
  MOVE_SPEED = 1
  up,left,down,right,run,shoot = (0,0,0,0,0,0)
  def start(self):
    self.target.velocity = (0,0)
    self.shootTimer = 0
    self.heading = np.array((1,0))
  def step(self,dt):
    global tilemap
    dx,dy = self.target.velocity
    pos = self.target.position
    curCell = tilemap.get_at_pixel(pos[0],pos[1])
    if 'speed' in curCell.tile.properties:
      terr = curCell.tile.properties['speed']
    else:
      terr = 100
    #use dt and player facing
    if self.shoot and self.shootTimer <= 0:
        bullet = Projectile(world,man_seq[0],self.target.position+self.heading*40,16)
        world.add(bullet)
        world.collobjs.add(bullet)
        #bullet.do(RandomController())
        bullet.do(MyMoveTo(self.target.position+self.heading*500,1))
        self.shootTimer = 100
    else:
        self.shootTimer -= 1
    dx = (1+self.run*2)*terr*(self.right - self.left) * self.MOVE_SPEED * dt
    dy = (1+self.run*2)*terr*(self.up - self.down) * self.MOVE_SPEED * dt
    if dx != 0 or dy != 0:
      if dy > 0: #moving up
        self.heading = np.array((0,1))
        self.target.image = man_seq[1]
        if abs(dx) - abs(dy) > 0:#left
          self.heading = np.array((-1,0))
          self.target.image = man_seq[2]
          if dx > 0: #moving right
            self.heading = np.array((1,0))
            self.target.image = self.target.image.get_transform(flip_x=True)
      else:#moving down
        self.heading = np.array((0,-1))
        self.target.image = man_seq[0]
        if abs(dx) - abs(dy) > 0:#left
          self.heading = np.array((-1,0))
          self.target.image = man_seq[2]
          if dx > 0:#right
            self.heading = np.array((1,0))
            self.target.image = self.target.image.get_transform(flip_x=True)
    #check for slow property
    #get players bounding rectangle
    last = self.target.get_rect()
    new = last.copy()
    new.x += dx
    new.y += dy

    #collider
    dx, dy = self.target.velocity = self.collide_map(tilemap,last,new,dy,dx)
    
    #position is the sprite's center
    self.target.last = self.target.position
    self.target.cshape.center = new.center

class ActorController(SpriteController, tiles.RectMapCollider):
    def step(self,dt): 
        super(ActorController,self).step(dt)
        scroller.set_focus(self.target.x,self.target.y)
        #check input
        self.run = keyboard[key.LCTRL] 
        self.shoot = keyboard[key.SPACE]
        self.right = keyboard[key.RIGHT]
        self.left = keyboard[key.LEFT]
        self.up = keyboard[key.UP]
        self.down = keyboard[key.DOWN]


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
            print 'asdf'
            move = np.random.randint(4)
            self.right = move == 0
            self.left = move == 1
            self.up = move == 2
            self.down = move == 3

        
class World(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(World,self).__init__()
        self.collobjs = set()
        self.collman = cm.CollisionManagerGrid(-8,tilemap.px_width+8,-8,tilemap.px_height+8,32,32)
        self.schedule(self.update)
    def update(self,dt):
        for objA,objB in self.collman.iter_all_collisions():
            objA.state = 'coll'
            objA.cshape.center = objA.position
            objB.state = 'coll'
            objB.cshape.center = objB.position
            print 'im here'
        self.collman.clear()
        #temp = self.collobjs.__deepcopy__()
        killSet = set()
        for o in self.collobjs:
            o.update(dt)
            if o.state == 'kill':
                #world.remove(o)
                #self.collobjs.remove(o)
                #o.kill()
                killSet.add(o)
                print 'dead'
            else:
                self.collman.add(o)

        for k in killSet:
            world.remove(k)
            self.collobjs.remove(k)
            #k.kill()
        killSet.clear()

def main():
  global tilemap, keyboard, scroller,man_seq,world
  from cocos.director import director
  director.init(width=800,height=600, do_not_scale=True, resizable=True)

  scroller = layer.ScrollingManager()
  tilemap = tiles.load('desert.tmx')['Level0']
  tilemap.visible = 1
  

  world = World()
  man = pyglet.image.load('man.png')
  man_seq = pyglet.image.ImageGrid(man,1,4)
  actor = CSprite(man_seq[0],200,100,16)
  world.add(actor)
  world.collobjs.add(actor)
  actor.do(ActorController())
  #actor.do(SpriteController())
  
  #enemy
  enemy = CSprite(man_seq[0],200,200,16)
  world.add(enemy)
  world.collobjs.add(enemy)
  enemy.do(RandomController())

  scroller.add(tilemap)
  scroller.add(world)

  main_scene = cocos.scene.Scene(scroller)

  keyboard = key.KeyStateHandler()
  director.window.push_handlers(keyboard)

  director.run(main_scene)

if __name__ == '__main__':
  main()

