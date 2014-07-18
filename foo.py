import pyglet
from pyglet.window import key

import cocos
from cocos import tiles,actions,layer

class ActorController(actions.Action, tiles.RectMapCollider):
  MOVE_SPEED = 200

  def start(self):
    self.target.velocity = (0,0)
  def step(self,dt):
    global keyboard, tilemap, scroller
    dx,dy = self.target.velocity

    dx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED * dt
    dy = (keyboard[key.UP] - keyboard[key.DOWN]) * self.MOVE_SPEED * dt
    
    pos = self.target.position
    curCell = tilemap.get_at_pixel(pos[0],pos[1])
    for i in range(39):
      for j in range(39):
        print tilemap.get_cell(i,j).properties
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

    #move camera
    scroller.set_focus(*new.center)


def main():
  global tilemap, keyboard, scroller
  from cocos.director import director
  director.init(width=800,height=600, do_not_scale=True, resizable=True)

  actor_layer = layer.ScrollableLayer()
  actor = cocos.sprite.Sprite('car.png')
  actor_layer.add(actor)
  actor.position = (200,100)
  actor.do(ActorController())

  scroller = layer.ScrollingManager()
  tilemap = tiles.load('desert.tmx')['Ground']
  scroller.add(tilemap)
  scroller.add(actor_layer)

  main_scene = cocos.scene.Scene(scroller)

  keyboard = key.KeyStateHandler()
  director.window.push_handlers(keyboard)

  director.run(main_scene)

if __name__ == '__main__':
  main()

