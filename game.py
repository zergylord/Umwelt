import pyglet
from pyglet.window import key

import numpy

import cocos
from cocos import tiles,actions,layer

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
    
    dx = (1+keyboard[key.LSHIFT]*2)*terr*(keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED * dt
    dy = (1+keyboard[key.LSHIFT]*2)*terr*(keyboard[key.UP] - keyboard[key.DOWN]) * self.MOVE_SPEED * dt
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


def main():
  global tilemap, keyboard, scroller,man_seq
  from cocos.director import director
  director.init(width=800,height=600, do_not_scale=True, resizable=True)

  actor_layer = layer.ScrollableLayer()
  man = pyglet.image.load('man.png')
  man_seq = pyglet.image.ImageGrid(man,1,4)
  actor = cocos.sprite.Sprite(man_seq[0])
  actor_layer.add(actor)
  actor.position = (200,100)
  actor.do(ActorController())
  
  #enemy
  enemy = cocos.sprite.Sprite(man_seq[0])
  actor_layer.add(enemy)
  enemy.position = (200,200)
  enemy.do(RandomController())

  scroller = layer.ScrollingManager()
  tilemap = tiles.load('desert.tmx')['Level0']
  tilemap.visible = 1
  scroller.add(tilemap)
  scroller.add(actor_layer)

  main_scene = cocos.scene.Scene(scroller)

  keyboard = key.KeyStateHandler()
  director.window.push_handlers(keyboard)

  director.run(main_scene)

if __name__ == '__main__':
  main()

