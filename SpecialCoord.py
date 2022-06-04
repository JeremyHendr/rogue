from Coord import Coord
import math
class SpecialCoord():
    imgsize = 64
    def __init__(self,x,y,decx=0,decy=0):
        self.x = x
        self.y = y
        self.decx = decx
        self.decy = decy

    def __eq__(self,other):
        if self.x==other.x and self.y==other.y and self.decx==other.decx and self.decy==other.decy:
            return True
        return False

    def __add__(self,other):
        if self.decy+other.decy >= SpecialCoord.imgsize:
            repy = self.y + other.y + 1
            repdecy = self.decy+other.decy-SpecialCoord.imgsize
        else:
            repy = self.y + other.y
            repdecy = self.decy + other.decy
        if self.decx+other.decx >= SpecialCoord.imgsize:
            repx = self.x + other.x + 1
            repdecx = self.decx + other.decx - SpecialCoord.imgsize
        else:
            repx = self.x + other.x
            repdecx = self.decx + other.decx
        return SpecialCoord(repx,repy,repdecx,repdecy)

    def __sub__(self,other):
        if self.decy - other.decy < 0:
            repy = self.y - other.y - 1
            repdecy = SpecialCoord.imgsize + (self.decy - other.decy)
        else:
            repy = self.y - other.y
            repdecy = self.decy - other.decy
        if self.decx - other.decx < 0:
            repx = self.x - other.x - 1
            repdecx = SpecialCoord.imgsize + (self.decx - other.decx)
        else:
            repx = self.x - other.x
            repdecx = self.decx-other.decx
        return SpecialCoord(repx, repy, repdecx, repdecy)

    def __repr__(self):
        return "<"+str(self.x)+"."+str(self.decx)+" , "+str(self.y)+"."+str(self.decy)+">"

    def distance(self,other):
        """
        :param other: SpecialCoord object
        :return: distance between self and other
        convDec = lambda c,dec: c+(dec/64)
        print(convDec(1,32))
        > 1.5
        """
        convDec = lambda c,dec: c+(dec/SpecialCoord.imgsize)
        c = self - other
        p = Coord(convDec(c.x,c.decx),convDec(c.y,c.decy))
        return math.sqrt((p.x ** 2 + p.y ** 2))

    def __mul__(self, s):
        return SpecialCoord(self.x*s,self.y*s,self.decx*s,self.decy*s)

    def direction(self):
        pass

# a = SpecialCoord(2,2)
# b = SpecialCoord(0,0,32,32)
# print(a,b)
# print(a-b)
# print(a+b)
# print(a==b)
# print(a.distance(b))
# <2.0 , 2.0> <0.32 , 0.32>
# <1.32 , 1.32>
# <2.32 , 2.32>
# False
# 2.1213203435596424