from Coord import Coord
from SpecialCoord import SpecialCoord

class Bullet:
    screen_refresh_rate = 30
    def __init__(self,pos=SpecialCoord(0,0),shooter=None,destination=SpecialCoord(1,1),speed=2,damage=10,armorpene=0,damagetype=None):
        if isinstance(pos,Coord):
            self.pos = SpecialCoord(pos.x,pos.y)
        else:
            self.pos = pos
        self.destination = destination
        self.speed = speed
        dist = self.pos.distance(self.destination)
        timetodest = dist/self.speed
        step = (self.destination-self.pos)*((timetodest*self.screen_refresh_rate)**(-1))
        print(dist,timetodest)
        self.step = step
        self.damage = damage
        self.shooter = shooter
        self.armor_pene = armorpene
        self.damage_type = damagetype

    def __repr__(self):
        return "<Bullet"+str(self.pos)+" dest:"+str(self.destination)+" speed"+str(self.speed)+" step"+str(self.step)+">"

    def updatePos(self):
        from utiles import theGame
        from Creature import Creature
        from Hero import Hero
        from Map import Map
        self.pos += self.step
        obj = theGame()._floor.get(Coord(self.pos.x,self.pos.y))
        print("-> In updatePos Bullet with:", self.pos + self.step, obj, self.damage)
        if isinstance(self.shooter,Hero):
            if isinstance(obj,Creature) and not isinstance(obj,Hero):
                obj.meet(Creature("bullet",0,"b",self.damage,0,self.armor_pene,self.damage_type))
        if obj in Map.walllist:
            theGame().bullet_list.pop(theGame().bullet_list.index(self))


# b = Bullet(SpecialCoord(0,0),SpecialCoord(5,5),2)
# print(b)