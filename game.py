import pyglet
from pyglet.window import key

import numpy

import cocos
from cocos import tiles,actions,layer
from collutil import *
import cocos.collision_model as cm

class ActorController(actions.Action, tiles.RectMapCollider):
  MOVE_SPEED = 1
  def start(self):
    self.target.velocity = (0,0)
  def step(self,dt):
    global keyboard, tilemap, scroller
    dx,dy = self.target.velocity
    pos = self.target.position
    curCell = tilemap.get_at_pixel(pos[0],pos[1])
    if 'speed' in curCell.tile.properties:
      terr = curCell.tile.properties['speed']
    else:
      terr = 100
    run = keyboard[key.LCTRL] 
    shoot = keyboard[key.SPACE]
    if shoot:
        bullet = cocos.sprite.Sprite(man_seq[0])
        world.add(bullet)
        bullet.position = self.target.position
        bullet.do(actions.MoveTo((self.target.x+100,self.target.y),6))
    dx = (1+run*2)*terr*(keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED * dt
    dy = (1+run*2)*terr*(keyboard[key.UP] - keyboard[key.DOWN]) * self.MOVE_SPEED * dt
    if self.target.state == 'coll':
        self.target.state = 'norm'
        dx = -dx
        dy = -dy
    #print keyboard
    if dx != 0 or dy != 0:
      if dy > 0:
        self.target.image = man_seq[1]
        if abs(dx) - abs(dy) > 0:
          self.target.image = man_seq[2]
          if dx > 0:
            self.target.image = self.target.image.get_transform(flip_x=True)
      else:
        self.target.image = man_seq[0]
        if abs(dx) - abs(dy) > 0:
          self.target.image = man_seq[2]
          if dx > 0:
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
    self.target.position = new.center
    scroller.set_focus(self.target.x,self.target.y)


class RandomController(actions.Action, tiles.RectMapCollider):
  MOVE_SPEED = 1
  rl = 1
  ud = 1
  def start(self):
    self.target.velocity = (0,0)
  def step(self,dt):
    global keyboard, tilemap, scroller
    dx,dy = self.target.velocity
    pos = self.target.position
    curCell = tilemap.get_at_pixel(pos[0],pos[1])
    if 'speed' in curCell.tile.properties:
      terr = curCell.tile.properties['speed']
    else:
      terr = 100
    if numpy.random.rand() > .95:
      self.rl = numpy.random.randint(3) - 1
      self.ud = numpy.random.randint(3) - 1
    dx = terr*(self.rl) * self.MOVE_SPEED * dt
    dy = terr*(self.ud) * self.MOVE_SPEED * dt
    if self.target.state == 'coll':
        self.target.state = 'norm'
        dx = -dx
        dy = -dy
    if dx != 0 or dy != 0:
      if dy > 0:
        self.target.image = man_seq[1]
        if abs(dx) - abs(dy) > 0:
          self.target.image = man_seq[2]
          if dx > 0:
            self.target.image = self.target.image.get_transform(flip_x=True)
      else:
        self.target.image = man_seq[0]
        if abs(dx) - abs(dy) > 0:
          self.target.image = man_seq[2]
          if dx > 0:
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
    self.target.position = new.center

class World(cocos.layer.ScrollableLayer):
    def __init__(self):
        super(World,self).__init__()
        self.collobjs = set()
        self.collman = cm.CollisionManagerGrid(-8,800+8,-8,600+8,40.0,40.0)
        self.schedule(self.update)
    def update(self,dt):
        self.collman.clear()
        for o in self.collobjs:
            o.update(dt)
            self.collman.add(o)
        for objA,objB in self.collman.iter_all_collisions():
            objA.state = 'coll'
            objB.state = 'coll'
            print 'im here'

def main():
  global tilemap, keyboard, scroller,man_seq,world
  from cocos.director import director
  director.init(width=800,height=600, do_not_scale=True, resizable=True)

  world = World()
  man = pyglet.image.load('man.png')
  man_seq = pyglet.image.ImageGrid(man,1,4)
  actor = CSprite(man_seq[0],200,100,10)
  world.add(actor)
  world.collobjs.add(actor)
  actor.do(ActorController())
  
  #enemy
  enemy = CSprite(man_seq[0],200,200,10)
  world.add(enemy)
  world.collobjs.add(enemy)
  enemy.do(RandomController())

  scroller = layer.ScrollingManager()
  tilemap = tiles.load('desert.tmx')['Level0']
  tilemap.visible = 1
  scroller.add(tilemap)
  scroller.add(world)

  main_scene = cocos.scene.Scene(scroller)

  keyboard = key.KeyStateHandler()
  director.window.push_handlers(keyboard)

  director.run(main_scene)

if __name__ == '__main__':
  main()

