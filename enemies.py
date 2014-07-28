from collutil import *
from entities import *
class BasicEnemy(Being):
    def __init__(self,image,pos):
        super(BasicEnemy,self).__init__(image,pos,16)
class Hero(Being):
    def __init__(self,image,pos):
        super(Hero,self).__init__(image,pos,16)
