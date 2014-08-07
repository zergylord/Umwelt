import pyglet
from pyglet.window import key

import numpy as np
import globals as g

import cocos
from cocos import tiles,actions,layer
from collutil import *
from enemies import *
from entities import *
import cocos.collision_model as cm

def Patrol(pos1,pos2,speed):
    dist = pow(pow(pos1[0]-pos2[0],2)+pow(pos1[1]-pos2[1],2),.5) 
    return actions.Repeat(
        MyMoveTo(pos1,dist/speed) +
        MyMoveTo(pos2,dist/speed)
        )
class ShootAtEnemy(actions.base_actions.IntervalAction, tiles.RectMapCollider):
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
    self.target.cshape.center = new.center
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
    self.target.cshape.center = new.center


def symColl(o1,o2):
    coll(o1,o2)
    coll(o2,o1)
def coll(o1,o2):
    if isinstance(o1,CSprite) and isinstance(o2,CSprite): #change to a more general 'collidable interface
        o1.state = 'coll'
        o1.cshape.center = o1.position
    if isinstance(o1,Projectile) and isinstance(o2,Being):
        o2.health -= o1.damage
    if isinstance(o1,SightBox): 
        if o2 == o1.enemy:
            o1.state = 'foundEnemy'
            print 'rarrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'
        
class World(cocos.layer.ScrollableLayer):
    controlNext = False
    def __init__(self):
        super(World,self).__init__()
        self.collobjs = set()
        self.collman = cm.CollisionManagerGrid(-8,g.tilemap.px_width+8,-8,g.tilemap.px_height+8,32,32)
        self.schedule(self.update)
    def update(self,dt):
        for objA,objB in self.collman.iter_all_collisions():
            symColl(objA,objB)
        self.collman.clear()
        #temp = self.collobjs.__deepcopy__()
        killSet = set()
        colremSet = set()
        for o in self.collobjs:
            if self.controlNext and isinstance(o,BasicEnemy):
                self.controlNext = False
                print 'controling enemy'
                o.state = 'take_control'
            o.update(dt)
            if o.state == 'control_target':
                print 'world got control signal!'
                self.controlNext = True
                o.state = 'norm'
            if o.state == 'kill':
                killSet.add(o)
                print 'dead'
            elif o.state == 'colrem':
                colremSet.add(o)
            else:
                self.collman.add(o)

        for k in colremSet:
            self.collobjs.remove(k)
        colremSet.clear()
        for k in killSet:
            g.world.remove(k)
            self.collobjs.remove(k)
        killSet.clear()

def makeEnemy(images,pos):
  enemy = BasicEnemy(images,pos)
  g.world.add(enemy)
  g.world.collobjs.add(enemy)
  return enemy

def main():
  from cocos.director import director
  director.init(width=800,height=600, do_not_scale=True, resizable=True)

  g.scroller = layer.ScrollingManager()
  g.tilemap = tiles.load('desert.tmx')['Level0']
  g.tilemap.visible = 1

  g.world = World()
  man = pyglet.image.load('man.png')
  man_seq = pyglet.image.ImageGrid(man,1,4)
  actor = Hero(man_seq,(200,100))
  g.player = actor
  g.world.add(actor)
  g.world.collobjs.add(actor)
  actor.do(ActorController())
  
  #enemy
  enemy = makeEnemy(man_seq,(200,200))
  enemy.do(Patrol((1000,100),(100,100),100))
  #TODO: do shoot enemy if bState = 'alert'
  #fancyAction = enemy.do(ShootAtEnemy(50))
  #fancyAction.initVars(g.player)
  
  #enemy vision box
  sBox = SightBox(enemy,g.player,(200,200),50,50)
  #g.world.add(vBox)
  g.world.collobjs.add(sBox)

  '''#enemy
  enemy = makeEnemy(man_seq,(200,300))
  enemy.do(Patrol((1000,200),(100,200),100))
  fancyAction = enemy.do(ShootAtEnemy(50))
  fancyAction.initVars(g.player)

  #enemy
  enemy = makeEnemy(man_seq,(200,400))
  enemy.do(Patrol((1000,300),(100,300),100))
  fancyAction = enemy.do(ShootAtEnemy(50))
  fancyAction.initVars(g.player)
  '''
  g.scroller.add(g.tilemap)
  g.scroller.add(g.world)

  main_scene = cocos.scene.Scene(g.scroller)

  g.keyboard = key.KeyStateHandler()
  director.window.push_handlers(g.keyboard)

  director.run(main_scene)

if __name__ == '__main__':
  main()

