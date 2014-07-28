from collutil import *
class Being(CSprite):
    maxHealth = 100
    health = maxHealth
    image_seq = ()
    def __init__(self,image_seq,pos,radius):
        self.image_seq = image_seq
        image = image_seq[0]
        super(Being,self).__init__(image,pos[0],pos[1],radius)
    def update(self,dt):
        super(Being,self).update(dt)
        if not self.state == 'kill' and self.health <= 0:
            self.state = 'kill'
            self.stop()
            print 'I died :-('
    def takeHit(self,damage):
        self.health -= damage
