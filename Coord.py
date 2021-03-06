import math
class Coord:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def set_y(self,x):
        self.x = x

    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __en__(self,other):
        if self.x != other.x and self.y != other.y:
            return True
        return False

    def __add__(self,other):
        return Coord(self.x+other.x, self.y+other.y)

    def __sub__(self,other):
      return Coord(self.x-other.x,self.y-other.y)

    def __repr__(self):
        return "<"+str(self.x)+","+str(self.y)+">"

    def distance(self,other):
      c = self-other
      return math.sqrt((c.x**2 + c.y**2))

    def direction(self,other):
      c = self-other
      cos = c.x/self.distance(other)
      if cos > 1/(2**0.5):
        return Coord(-1,0)
      elif cos < -1/(2**0.5):
          return Coord(1,0)
      elif c.y > 0:
        return Coord(0,-1)
      return Coord(0,1)

    def toSpecialCoord(self):
        """
        converts a Coord in pixel (pygame) in Coord with a integer part that corrspond to the Map coord
        then a decimal part between 0 to 64 pixels
        exemple:
         SpecialCoord(2,5,32,32) is (2.5;5.5) on the Map
        :return: SpecialCoord instance
        """
        from utiles import theGame
        from SpecialCoord import SpecialCoord
        mapc1 = theGame().templist[0][0]
        cartec1 = theGame().templist[0][1]
        x = mapc1.x+(self.x-cartec1.x)//64
        y = mapc1.y+(self.y-cartec1.y)//64
        decx = (self.x-cartec1.x)%64
        decy = (self.y-cartec1.y)%64
        return SpecialCoord(int(x),int(y),int(decx),int(decy))
