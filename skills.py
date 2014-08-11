"""
skills can be thought of as the weapons or other abilities units use
to interact with their environment. They differ from actions in that
they typically spawn entities who are in turn controlled by actions.

Current Skill List:
    +Projectile
    +Bomb
"""
import cocos
import globals as g
from cocos import tiles
import cocos.euclid as eu 
import cocos.collision_model as cm
import pyglet.image
from entities import CSprite
import numpy as np
from actions import *
'''Abstract Skill Class'''
class Skill():
    timer = 0
    cooldown = 0 #in seconds
    target = None
    name = 'aSkill'
    def use(self):
        print 'should have overwritten me!'
        if self.timer <= 0:
            self.timer = self.cooldown
            #code performing skill
    #should be called evertime owner (target) updates
    def update(self,dt):
        self.timer -= dt

class MineThrow(Skill):
    def __init__(self):
        self.name = 'mThrow'
        self.timer = 0
        self.cooldown = 1
    def use(self,tpos):
        if self.timer <= 0:
            dx = tpos[0] - self.target.position[0]
            dy = tpos[1] - self.target.position[1]
            self.target.movementUpdate(dx,dy)

            shoot = True
            delta = np.array((dx,dy))
            exactHead = delta/np.linalg.norm(delta)
            self.timer = self.cooldown

            bullet = Mine(g.world,self.target.position+exactHead*50)
            g.world.add(bullet)
            g.world.collobjs.add(bullet)
            bullet.do(MyMoveTo(self.target.position+exactHead*500))

class SpearThrow(Skill):
    def __init__(self):
        self.name = 'sThrow'
        self.timer = 0
        self.cooldown = 1
    def use(self,tpos):
        if self.timer <= 0:
            dx = tpos[0] - self.target.position[0]
            dy = tpos[1] - self.target.position[1]
            self.target.movementUpdate(dx,dy)

            shoot = True
            delta = np.array((dx,dy))
            exactHead = delta/np.linalg.norm(delta)
            self.timer = self.cooldown

            man = pyglet.image.load('man.png')
            seq =  pyglet.image.ImageGrid(man,1,4)
            image = seq[0]
            bullet = Projectile(g.world,self.target.position+exactHead*50,16,image)
            g.world.add(bullet)
            g.world.collobjs.add(bullet)
            bullet.do(MyMoveTo(self.target.position+exactHead*500))

'''interface for entities that can damage Beings on collision'''
class Damaging():
    damage = 0
class Projectile(CSprite,Damaging):
    damage = 25
    speed = 1000
    def __init__(self,world,pos,radius,image):
        #man = pyglet.image.load('man.png')
        #seq =  pyglet.image.ImageGrid(man,1,4)
        #image = seq[0]
        super(Projectile,self).__init__(image,pos[0],pos[1],radius)
        self.world = world
    """overwrite for different kill conditions"""
    def killCond(self):
        return self.actions == [] or self.state == 'coll'
    def update(self,dt):
        if self.killCond():
            self.state = 'kill'
            print 'start kill proc'
            self.stop()
            print 'got here'
        else:
            coll,new = self.resolveMovement()
            if coll:
                self.state = 'kill'
                self.stop()
                print 'died from environment'
            else:
                #---position is the sprite's center
                self.last = self.position
                self.cshape.center = new.center
                self.position = self.cshape.center
class Mine(Projectile):
    damage = 25
    def __init__(self,world,pos):
        man = pyglet.image.load('man.png')
        seq =  pyglet.image.ImageGrid(man,1,4)
        image = seq[0]
        super(Mine,self).__init__(world,pos,16,image)
        self.speed = 100
    def killCond(self):
        return self.state == 'coll'
