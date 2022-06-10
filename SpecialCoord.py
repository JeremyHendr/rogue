from Coord import Coord
import math
class SpecialCoord():
    imgsize = 64
    def __init__(self,x,y,decx=0,decy=0):
        self.x = x
        self.y = y
        self.decx = decx
        self.decy = decy
        # if type(x)!="int" or type(y)!="int" or type(decy)!="int" or type(decx)!="int":
        #     print("not integer given in SpecialCoord object")

    def __eq__(self,other):
        if isinstance(other,SpecialCoord):
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
        # print(self,other,SpecialCoord(repx,repy,repdecx,repdecy))
        return SpecialCoord(repx,repy,repdecx,repdecy)

    def __sub__(self,other):
        if self.decy - other.decy < 0:
            repy = self.y - other.y - 1
            repdecy = SpecialCoord.imgsize + (self.decy - other.decy)
        else:
            repy = self.y - other.y
            repdecy = self.decy - other.decy
        if self.decx - other.decx < 0:
            repx = self.x - other.x
            repdecx = SpecialCoord.imgsize + (self.decx - other.decx)
        else:
            repx = self.x - other.x
            repdecx = self.decx-other.decx
        return SpecialCoord(repx, repy, repdecx, repdecy)

    def __repr__(self):
        return "<"+str(self.x)+","+str(self.decx)+" ; "+str(self.y)+","+str(self.decy)+">"

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
        return SpecialCoord(self.x*s,self.y*s,self.decx*s,self.decy*s).verifCoord()

    def verifCoord(self):
        x_int_part = int(self.x)
        x_dec_part = self.x-x_int_part
        x = x_int_part
        decx = int(x_dec_part*SpecialCoord.imgsize)+self.decx
        if decx >= SpecialCoord.imgsize:
            x += decx//SpecialCoord.imgsize
            decx = decx%64

        y_int_part = int(self.y)
        y_dec_part = self.y - y_int_part
        y = y_int_part
        decy = int(y_dec_part * SpecialCoord.imgsize) + self.decy
        if decy >= SpecialCoord.imgsize:
            y += decy // SpecialCoord.imgsize
            decy = decy % 64

        return SpecialCoord(x,y,decx,decy)


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