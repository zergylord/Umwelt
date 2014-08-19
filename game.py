#!/usr/bin/python
"""
contains the main game loop, as well as the obj collision loop. In this loop
all collidable objects are updated.
"""

import pyglet
from pyglet.window import key

import numpy as np
import globals as g

import cocos
from cocos import tiles,actions,layer
from skills import *
from enemies import *
from entities import *
from actions import *
import cocos.collision_model as cm

def symColl(o1,o2):
    coll(o1,o2)
    coll(o2,o1)
def coll(o1,o2):
    if isinstance(o1,CSprite) and isinstance(o2,CSprite): #change to a more general 'collidable interface
        o1.state = 'coll'
        o1.cshape.center = o1.position - np.array((o1.dx,o1.dy))*2
        if isinstance(o1,Being) and isinstance(o2,Being):
            o1.takeHit(0)#hack for alerting enemies
    if isinstance(o1,Damaging) and isinstance(o2,Being):
        print 'took damage'
        o2.takeHit(o1.damage)
    if isinstance(o1,SightBox): 
        if o2 == o1.enemy:
            o1.state = 'foundEnemy'
        
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
            k.kill()
            #g.world.remove(k)
            self.collobjs.remove(k)
        killSet.clear()

def makeEnemy(images,pos,patEnd):
    enemy = BasicEnemy(images,pos,patEnd)
    g.world.add(enemy)
    g.world.collobjs.add(enemy)
    #enemy vision box
    sBox = SightBox(enemy,g.player,20,100)
    g.world.collobjs.add(sBox)
    lBox = SightLimitBox(enemy,g.player,200,200)
    g.world.collobjs.add(lBox)
    return enemy

class MainLayer(layer.ScrollingManager):
    '''Pyglet already handles keypresses, but meh'''
    is_event_handler = True
    def on_key_press(self,key,modifiers):
        g.pressed[key] = True
    def on_key_release(self,key,modifiers):
        g.pressed[key] = False
        g.released[key] = True #controller must reset to False upon using
def main():
    from cocos.director import director
    director.init(width=800,height=600, do_not_scale=False, resizable=True,audio_backend='sdl')

    g.pressed = dict()
    g.released = dict()
    g.team = []
    g.team.append(set())#team 0 is the player/pet
    g.team.append(set())#team 1 are the 'intelligent' enemies
    g.team.append(set())#team 2 attack everything e.g. beasts
    g.team.append(set())#team 3 attack nothing unless provoked (then switch teams?)

    g.scroller = MainLayer()
    g.scroller.set_scale(2)
    g.tilemap = tiles.load_tmx('desert.tmx')['Level0']
    g.tilemap.visible = 1

    g.world = World()
    man = pyglet.image.load('man.png')
    man_seq = pyglet.image.ImageGrid(man,1,4)
    actor = Hero(man_seq,(50,50))
    g.player = actor
    g.team[0].add(actor)
    g.world.add(actor)
    g.world.collobjs.add(actor)
    actor.do(ActorController())

    #enemy
    enemy = makeEnemy(man_seq,(200,100),(1000,100))
    enemy = makeEnemy(man_seq,(1000,200),(200,200))

    '''
    #enemy
    enemy = makeEnemy(man_seq,(100,200))
    enemy.do(Patrol((1000,200),(100,200),100))
    #enemy vision box
    sBox = SightBox(enemy,g.player,50,50)
    g.world.collobjs.add(sBox)

    #enemy
    enemy = makeEnemy(man_seq,(50,300))
    enemy.do(Patrol((1000,300),(50,300),100))
    #enemy vision box
    sBox = SightBox(enemy,g.player,50,50)
    g.world.collobjs.add(sBox)
    '''
    g.scroller.add(g.tilemap)
    g.scroller.add(g.world)

    main_scene = cocos.scene.Scene(g.scroller)

    g.keyboard = key.KeyStateHandler()
    director.window.push_handlers(g.keyboard)

    director.run(main_scene)

if __name__ == '__main__':
    main()

