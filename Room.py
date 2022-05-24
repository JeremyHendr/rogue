from Coord import Coord
import random
class Room:
    def __init__(self,cc1,cc2):
        self.c1=cc1
        self.c2=cc2

    def __repr__(self):
        return "["+str(self.c1)+", "+str(self.c2)+"]"

    def __contains__(self,a):
        return a.x>=self.c1.x and a.y>=self.c1.y and a.x<=self.c2.x and a.y<=self.c2.y

    def center(self):
        return Coord(((self.c2.x+self.c1.x)//2),((self.c2.y+self.c1.y)//2))

    def intersect(self,other):
       return (other.c1 in self) or (Coord(other.c1.x+(other.c2.x-other.c1.x), other.c1.y) in self) or (other.c2 in self) or (Coord(other.c2.x-(other.c2.x-other.c1.x), other.c2.y) in self) or (self.c1 in other) or (Coord(self.c1.x+(self.c2.x-self.c1.x), self.c1.y) in other) or (self.c2 in other) or (Coord(self.c2.x-(self.c2.x-self.c1.x), self.c2.y) in other)

    def randCoord(self):
        return Coord(random.randint(self.c1.x,self.c2.x),random.randint(self.c1.y,self.c2.y))

    def randEmptyCoord(self,map):
        a = self.randCoord()
        while True:
            if (map.get(a) == map.ground and a != self.center()):
                break
            a = self.randCoord()
        return a

    def decorate(self,map):
        from utiles import theGame
        hero_pos = map.pos(map._hero)
        c = self.randEmptyCoord(map)
        map.put(c, theGame().randEquipment())
        c = self.randEmptyCoord(map)
        while hero_pos.distance(c) < 3:
            c = self.randEmptyCoord(map)
        map.put(c,theGame().randMonster())