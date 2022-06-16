from Coord import Coord
import math
class SpecialCoord():
    """this class is a subtitute to the Coord class,
    only used for the bullet it allows to have coords between to coord so that the ullet palcement is indepant from the map matrix"""
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
        imgsize = SpecialCoord.imgsize
        b64tob10 = lambda c: Coord(c.x+(c.decx/imgsize),c.y+(c.decy/imgsize))
        b10tob64 = lambda c: SpecialCoord(int(c.x),int(c.y),(int((c.x-int(c.x))*imgsize)),(int((c.y-int(c.y))*imgsize)))
        a = b64tob10(self)
        b = b64tob10(other)
        return b10tob64(a+b)

    def __sub__(self,other):
        imgsize = SpecialCoord.imgsize
        b64tob10 = lambda c: Coord(c.x+(c.decx/imgsize),c.y+(c.decy/imgsize))
        b10tob64 = lambda c: SpecialCoord(int(c.x),int(c.y),(int((c.x-int(c.x))*imgsize)),(int((c.y-int(c.y))*imgsize)))
        a = b64tob10(self)
        b = b64tob10(other)
        return b10tob64(a-b)


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
        c = other - self
        p = Coord(convDec(c.x,c.decx),convDec(c.y,c.decy))
        # print("distance p",p,self,other,c)
        return math.sqrt((p.x ** 2 + p.y ** 2))

    def __mul__(self, s):
        return SpecialCoord(self.x*s,self.y*s,self.decx*s,self.decy*s).verifCoord()

    def verifCoord(self):
        """make the coordinate are in the right form, decx and decy shall not go over 64,
        if that happens we increment x or y by decx//64 or decy//64"""
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

        return SpecialCoord(x,y,int(round(decx)),int(round(decy)))

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

#<7,28 ; 16,15> <8,32 ; 18,32>
# a = SpecialCoord(7,16,-28,45)
# b = SpecialCoord(8,18,32,32)
# print(a+b)