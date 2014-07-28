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
    o1.state = 'coll'
    o1.cshape.center = o1.position
    if isinstance(o1,Projectile) and isinstance(o2,Being):
        o2.health -= o1.damage
        
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
            print 'im here'
        self.collman.clear()
        #temp = self.collobjs.__deepcopy__()
        killSet = set()
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
                #world.remove(o)
                #self.collobjs.remove(o)
                #o.kill()
                killSet.add(o)
                print 'dead'
            else:
                self.collman.add(o)

        for k in killSet:
            g.world.remove(k)
            self.collobjs.remove(k)
            #k.kill()
        killSet.clear()
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
  g.world.add(actor)
  g.world.collobjs.add(actor)
  actor.do(ActorController())
  
  #enemy
  enemy = BasicEnemy(man_seq,(200,200))
  g.world.add(enemy)
  g.world.collobjs.add(enemy)
  enemy.do(RandomController())

  g.scroller.add(g.tilemap)
  g.scroller.add(g.world)

  main_scene = cocos.scene.Scene(g.scroller)

  g.keyboard = key.KeyStateHandler()
  director.window.push_handlers(g.keyboard)

  director.run(main_scene)

if __name__ == '__main__':
  main()

