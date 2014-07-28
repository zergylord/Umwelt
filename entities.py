from collutil import *
class Being(CSprite):
    maxHealth = 100
    health = maxHealth
    def __init__(self,image,pos,radius):
        super(Being,self).__init__(image,pos[0],pos[1],radius)
    def update(self,dt):
        super(Being,self).update(dt)
        if not self.state == 'kill' and self.health <= 0:
            self.state = 'kill'
            self.stop()
            print 'I died :-('
    def takeHit(self,damage):
        self.health -= damage
