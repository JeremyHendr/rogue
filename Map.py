from Coord import Coord
from Hero import Hero
import random

class Map:
    ground = "."
    empty = " "
    dir = {'z': Coord(0,-1),
                's': Coord(0,1),
                'd': Coord(1,0),
                'q': Coord(-1,0)}

    def __init__(self,size=20,hero=Hero(),nbrooms=7):
        self.nbrooms = nbrooms
        self.size = size
        self._hero = hero
        self._elem = {}
        self._mat = []
        self._roomsToReach = []
        self._rooms = []
        l = [Map.empty for i in range(self.size)]
        self._mat = [l.copy() for j in range(self.size)]
       # self._mat[self.poos.y][self.poos.x] = self._hero
        self.generateRooms(nbrooms)
        self.reachAllRooms()
        self.hidden_elem = []

    def __repr__(self):
        rep = ""
        for y in self._mat:
            for x in y:
                rep += str(x)
            rep+="\n"
        return rep

    def __len__(self):
        return self.size

    def __contains__(self,item):
        if isinstance(item,Coord):
            if item.x < len(self) and item.y < len(self):
                if item.x >= 0 and item.y >= 0:
                    return True
        else:
            for l in self._mat:
                if item in l:
                    return True
        return False

    def checkCoord(self,c):
        if not isinstance(c,Coord):
            raise TypeError('Not a Coord',c)
        if not (0 <= c.x and c.x < self.size and 0 <= c.y and c.y < self.size):
            raise  IndexError('Out of map coord',c)

    def checkElement(self,e):
        from Element import Element
        if not isinstance(e,Element):
            raise TypeError('Not a Element',e)

    def get(self,c):
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self,item):
        self.checkElement(item)
        for i in range(len(self._mat)):
            if item in self._mat[i]:
                return Coord(self._mat[i].index(item),i)
        return None

    def put(self,c,item):
        self.checkCoord(c)
        self.checkElement(item)
        if self._mat[c.y][c.x] != Map.ground:
            raise ValueError('Incorrect cell')
        if item in self._elem:
            raise KeyError('Already placed')

        self._elem[item] = c
        self._mat[c.y][c.x] = item
        return None

    def rm(self,c):
        # self.checkCoord(c)
        del self._elem[self.get(c)]
        self._mat[c.y][c.x] = Map.ground

    def addRoom(self,room1):
        self._roomsToReach.append(room1)
        a=-1
        for i in self._mat:
            a+=1
            b=0
            for k in i:
                if a>=room1.c1.x and a<=room1.c2.x and b>=room1.c1.y and b<=room1.c2.y:
                    self._mat[b][a] = Map.ground
                b+=1

    def findRoom(self,coord):
        for i in self._roomsToReach:
            if coord in i:
                return i
        return False

    def intersectNone(self,room):
        for i in self._roomsToReach:
            if i.intersect(room):
                return False
        return True

    def dig(self,coord):
        self._mat[coord.y][coord.x] = Map.ground
        a = self.findRoom(coord)
        if a != False:
            self._roomsToReach.pop(self._roomsToReach.index(a))
            self._rooms.append(a)

    def corridor(self,start,end):
        coord = start
        while (start.y < end.y and coord.y < end.y) or (start.y > end.y and coord.y > end.y):
            coord += Coord(0, -1 if start.y > end.y else 1)
            self.dig(coord)
        while (start.x < end.x and coord.x <= end.x) or (start.x > end.x and coord.x >= end.x):
            coord += Coord(-1 if start.x > end.x else 1, 0)
            self.dig(coord)

    def reach(self):
        self.corridor(random.choice(self._rooms).center(), random.choice(self._roomsToReach).center())

    def reachAllRooms(self):
        if len(self._roomsToReach) == 0:
            return None
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoomCoord(self):
        """create a room with a random size on random coord"""
        x1 = random.randint(0,len(self) - 3)
        y1 = random.randint(0,len(self) - 3)
        x2 = min(len(self._mat)-1,x1+random.randint(3,8))
        y2 = min(len(self._mat)-1,y1+random.randint(3,8))
        return Coord(x1,y1),Coord(x2,y2)

    def generateRooms(self,n):
        from Room import Room
        from ChestRoom import ChestRoom
        from ShopRoom import ShopRoom
        for i in range(n):
            # print("-> In generateRooms",n)
            choice = random.choices(["room","chest_room","waepon_dealer_room"],[8,2,2])[0]
            # print("choice",choice)
            c = self.randRoomCoord()
            if choice == "room":
                roomido = Room(c[0], c[1])
            elif choice == "chest_room":
                roomido = ChestRoom(c[0], c[1])
            elif choice == "waepon_dealer_room":
                roomido = ShopRoom(c[0], c[1])
            if self.intersectNone(roomido):
                self.addRoom(roomido)

    def move(self,e,way):
        from Creature import Creature
        from Equipment import Equipment
        from utiles import theGame
        """Moves the element e in the direction way."""
        print("-> In move with",e,way,e.state)
        statetodelete = []
        for l in e.state.items():
            # print("state loop",state,state[0])
            if l[0] == "poisoned":
                e.meet(Creature("poison",0,"",l[1]["damage"]+e.armor))
                e.state[l[0]]["damage"] += e.state[l[0]]["damage"]
                if e.state[l[0]]["time"] > 0:
                    e.state[l[0]]["time"] -= 1
                else:
                    statetodelete.append(l[0])
            elif l[0] == "burn":
                e.meet(Creature("fire", 0, "", l[1]["damage"]+e.armor))
                if e.state[l[0]]["time"] > 0:
                    e.state[l[0]]["time"] -= 1
                else:
                    statetodelete.append(l[0])
        for state in statetodelete:
            e.state.pop(state)
        if e.hp <= 0:
            self.rm(e)
            theGame().addMessage("The creature " + str(e) + " is dead")
        else:
            orig = self.pos(e)
            dest = orig + way
            if dest in self and not "frozen" in e.state:
                if self.get(dest) == Map.ground:
                    self._mat[orig.y][orig.x] = Map.ground
                    self._mat[dest.y][dest.x] = e
                    self._elem[e] = dest
                elif self.get(dest) != Map.empty:
                    if self.get(dest).meet(e): #si l'elem a ete mis dans l'inventaire ou le monstre tue
                        if not isinstance(self.get(dest),Creature): #si c'est pas un monstre on suppr la dest puis on bouge
                            self.rm(dest)
                            self._mat[orig.y][orig.x] = Map.ground
                            self._mat[dest.y][dest.x] = e
                            self._elem[e] = dest
                        else: #si c'est un monstre on supprime juste la dest
                            self.rm(dest)
                    elif isinstance(self.get(dest), Equipment):
                        # print("hidden elem append",self.get(dest),type(self.get(dest)),self.get(dest) in self._elem,self._elem)
                        self.hidden_elem.append([dest, self.get(dest)])
                        self._mat[dest.y][dest.x] = Map.ground
                        self._mat[orig.y][orig.x] = Map.ground
                        self._mat[dest.y][dest.x] = e
                        self._elem[e] = dest
                for elem in self.hidden_elem:
                    if self.get(elem[0]) == Map.ground:
                        self._mat[elem[0].y][elem[0].x]=elem[1]
                        self.hidden_elem.pop(self.hidden_elem.index(elem))

    def moveAllMonsters(self):
        from Creature import Creature
        for obj in self._elem:
            if isinstance(obj,Creature) and obj!=self._hero and self._elem[obj].distance(self._elem[self._hero])<=6:
                self.move(obj, self._elem[obj].direction(self._elem[self._hero]))