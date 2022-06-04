from Coord import Coord
from SpecialCoord import SpecialCoord
class Bullet:
    screen_refresh_rate = 30
    def __init__(self,pos,destination,speed):
        if isinstance(pos,Coord):
            self.pos = SpecialCoord(pos.x,pos.y)
        else:
            self.pos = pos
        self.destination = destination
        self.speed = speed
        # ive got mouse coord and shooter pos so distance between both
        # then ive got the speed of my bullet
        # then ive got the time between origin and click
        # sub both Coord then divide by nb sec and then refresh rate
        dist = self.pos.distance(self.destination)
        timetodest = dist/self.speed
        step = (self.destination-self.pos)*((timetodest*self.screen_refresh_rate)**(-1))
        print(dist,timetodest)
        self.step = step

    def __repr__(self):
        return "<Bullet"+str(self.pos)+" "+str(self.destination)+" "+str(self.speed)+" "+str(self.step)+">"

b = Bullet(SpecialCoord(0,0),SpecialCoord(5,5),2)
print(b)