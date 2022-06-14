from Coord import Coord
from SpecialCoord import SpecialCoord

class Bullet:
    screen_refresh_rate = 30
    id = 0
    def __init__(self,pos=SpecialCoord(0,0),shooter=None,destination=SpecialCoord(1,1),speed=5,damage=10,armorpene=0,damagetype=None):
        if isinstance(pos,Coord):
            self.pos = SpecialCoord(pos.x,pos.y,32,32)
        else:
            self.pos = pos
        self.destination = destination
        self.speed = speed
        dist = self.pos.distance(self.destination)
        timetodest = dist/self.speed
        step = (self.destination-self.pos)*((timetodest*self.screen_refresh_rate)**(-1))
        self.step = step
        # print("step:",self.destination-self.pos,timetodest*self.screen_refresh_rate,((timetodest*self.screen_refresh_rate)**(-1)),(self.destination-self.pos)*((timetodest*self.screen_refresh_rate)**(-1)))
        # print("created bullet with:",self.pos,self.destination,self.step," dist:",dist," time:",timetodest)
        self.damage = damage
        self.shooter = shooter
        self.armor_pene = armorpene
        self.damage_type = damagetype
        self.ide = Bullet.id
        Bullet.id += 1


    def __repr__(self):
        return "<Bullet:"+str(self.ide)+" pos:"+str(self.pos)+" dest:"+str(self.destination)+" speed:"+str(self.speed)+" step:"+str(self.step)+">"

    def updatePos(self):
        from utiles import theGame
        from Creature import Creature
        from Hero import Hero
        from Map import Map
        if not self in theGame().log_update_pos_bullet.keys():
            theGame().log_update_pos_bullet[self] = [self]
        self.pos += self.step
        obj = theGame()._floor.get(Coord(int(self.pos.x),int(self.pos.y)))
        theGame().log_update_pos_bullet[self].append("updatePos: old:"+str(self.pos)+"new"+str(self.pos + self.step)+" step:"+str(self.step)+" "+str(obj))
        if isinstance(self.shooter,Hero):
            if isinstance(obj,Creature) and not isinstance(obj,Hero):
                obj.meet(Creature("bullet",0,"b",self.damage,0,self.armor_pene,self.damage_type))
                theGame().bullet_list.pop(theGame().bullet_list.index(self))
                # print("LOG",theGame().log_update_pos_bullet[self])
        if obj in Map.walllist:
            theGame().bullet_list.pop(theGame().bullet_list.index(self))
            # print("LOG",theGame().log_update_pos_bullet[self])

# b = Bullet(SpecialCoord(0,0),SpecialCoord(5,5),2)
# print(b)