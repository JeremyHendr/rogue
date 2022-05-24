
class Coord:
    def __init__(self,x,y):
        # print("in coord")
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