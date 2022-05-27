from Coord import Coord
from Hero import Hero
import random

class Map:
    # https://theasciicode.com.ar/extended-ascii-code/box-drawings-double-line-vertical-left-character-ascii-code-185.html
    #alt+ 200:╚ 201:╔  196─ '┬┬┴ 192└ 191┐ ¢ 188╝ 187╗ 186║  █ 219, ▄ 220, ▬ 22
    ground = "."
    empty = " "
    walllist = ["║", "═", "╝", "╚", "╗", "╔", "╠", "╣", "╩", "╦", "╬", "#","¤"]
    dir = {'z': Coord(0,-1),
                's': Coord(0,1),
                'd': Coord(1,0),
                'q': Coord(-1,0)}

    def __init__(self,size=23,hero=Hero(),nbrooms=7):
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
        self.putWalls()
        self.hidden_elem = []
        self.damage_done = []

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

    def addRoom(self,room):
        # self._roomsToReach.append(room1)
        # a=-1
        # for lines in self._mat:
        #     a+=1
        #     b=0
        #     for case in lines:
        #         if a>=room1.c1.x and a<=room1.c2.x and b>=room1.c1.y and b<=room1.c2.y:
        #             self._mat[b][a] = Map.ground
        #         b+=1
        self._roomsToReach.append(room)
        for x in range(len(self)):
            for y in range(len(self)):
                if Coord(x,y) in room:
                    self._mat[y][x] = Map.ground

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
        """used to link all rooms with corridors"""
        if len(self._roomsToReach) == 0:
            return None
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoomCoord(self):
        """create a room with a random size on random coord"""
        x1 = random.randint(1,len(self)-5)
        y1 = random.randint(1,len(self)-5)
        x2 = min(len(self)-2,x1+random.randint(3,8))
        y2 = min(len(self)-2,y1+random.randint(3,8))
        print(Coord(x1,y1),Coord(x2,y2))
        return Coord(x1,y1),Coord(x2,y2)

    def generateRooms(self,n):
        """
        Add between 0 and n rooms to roomsToReach
        :param n: maximum number of rooms
        """
        from Room import Room
        from ChestRoom import ChestRoom
        from ShopRoom import ShopRoom
        from Coord import Coord
        # print("-> In generateRooms",n)
        c = self.randRoomCoord()
        spawnroom = ChestRoom(c[0], Coord(min(c[1].x,c[0].x+2), min(c[1].y,c[0].y+2)))
        if self.intersectNone(spawnroom):
            self.addRoom(spawnroom)
        for i in range(n-1):
            choice = random.choices(["room","chest_room","waepon_dealer_room"],[10,1,1])[0]
            # print("choice",choice)
            c = self.randRoomCoord()
            if choice == "room":
                roomido = Room(c[0], c[1])
            elif choice == "chest_room":
                roomido = ChestRoom(c[0], Coord(c[0].x+2,c[0].y+2))
            elif choice == "waepon_dealer_room":
                roomido = ShopRoom(c[0], Coord(c[0].x+2,c[0].y+2))
            if self.intersectNone(roomido):
                self.addRoom(roomido)
        for x in range(100):
            c = self.randRoomCoord()
            stairsroom = ChestRoom(c[0], Coord(c[0].x + 2, c[0].y + 2))
            if self.intersectNone(stairsroom):
                self.addRoom(stairsroom)
                break

    def surroundingElementsCoord(self,c):
        from Coord import Coord
        for x in (c.x-1,c.x+1):
            for y in (c.y-1,c.y+1):
                if Coord(x,y) in self and not Coord(x,y) == c and self.get(Coord(x,y)) != Map.empty and self.get(Coord(x,y)) != "#":
                    return True

    def surroundingWallsCardinal(self,c):
        from Coord import Coord
        l = []
        # print("-> In suroundingwall with",c,self.get(c))
        card_coord = [Coord(c.x-1,c.y),Coord(c.x+1,c.y),Coord(c.x,c.y-1),Coord(c.x,c.y+1)]
        for coord in card_coord:
            if coord in self and self.get(coord) in Map.walllist:
                dir_coord = coord-c
                if  dir_coord == Coord(1,0):
                    l.append("E")
                elif dir_coord == Coord(-1,0):
                    l.append("O")
                elif dir_coord == Coord(0,1):
                    l.append("S")
                elif dir_coord == Coord(0,-1):
                    l.append("N")
        return l

    def putWalls(self):
        from Coord import Coord
        for x in range(len(self)):
            for y in range(len(self)):
                if self.get(Coord(x,y)) == Map.empty and self.surroundingElementsCoord(Coord(x,y)):
                    self._mat[y][x] = "#"

        for x in range(len(self)):
            for y in range(len(self)):
                if self.get(Coord(x,y)) == "#":
                    card_point_list = self.surroundingWallsCardinal(Coord(x,y))
                    # print(Coord(x,y),self.get(Coord(x,y)),card_point_list)
                    if len(card_point_list) == 2:
                        if "S" in card_point_list and "N" in card_point_list:
                            self._mat[y][x] = "║"
                        elif "O" in card_point_list and "E" in card_point_list:
                            self._mat[y][x] = "═"
                        elif "N" in card_point_list and "O" in card_point_list:
                            self._mat[y][x] = "╝"
                        elif "N" in card_point_list and "E" in card_point_list:
                            self._mat[y][x] = "╚"
                        elif "S" in card_point_list and "O" in card_point_list:
                            self._mat[y][x] = "╗"
                        elif "S" in card_point_list and "E" in card_point_list:
                            self._mat[y][x] = "╔"
                    elif len(card_point_list) == 3:
                        if "S" in card_point_list and "N" in card_point_list and "E" in card_point_list:
                            self._mat[y][x] = "╠"
                        elif "S" in card_point_list and "N" in card_point_list and "O" in card_point_list:
                            self._mat[y][x] = "╣"
                        elif "E" in card_point_list and "O" in card_point_list and "N" in card_point_list:
                            self._mat[y][x] = "╩"
                        elif "E" in card_point_list and "O" in card_point_list and "S" in card_point_list:
                            self._mat[y][x] = "╦"
                    elif len(card_point_list)==4:
                        self._mat[y][x] = "╬"
                    else:
                        self._mat[y][x] = "¤"
                    # if self.get(Coord(x,y)) =="¤":
                    #     print(self.get(Coord(x,y)))

    def move(self,e,way):
        from Creature import Creature
        from Equipment import Equipment
        from utiles import theGame
        """Moves the element e in the direction way."""
        # print("-> In move with",e,way,e.state)
        orig = self.pos(e)
        dest = orig + way
        if dest in self and not self.get(dest) in Map.walllist:
            if self.get(dest) == Map.ground and not "frozen" in e.state:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
            elif self.get(dest) != Map.empty and not "frozen" in e.state:
                if self.get(dest).meet(e) : #si l'elem a ete mis dans l'inventaire ou le monstre tue
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
            elif isinstance(self.get(dest),Creature) and "frozen" in e.state:
                if self.get(dest).meet(e):
                    self.rm(dest)

            for elem in self.hidden_elem:
                if self.get(elem[0]) == Map.ground:
                    self._mat[elem[0].y][elem[0].x]=elem[1]
                    self.hidden_elem.pop(self.hidden_elem.index(elem))

    def moveAllMonsters(self):
        from Creature import Creature
        for obj in self._elem:
            if isinstance(obj,Creature) and obj!=self._hero and self._elem[obj].distance(self._elem[self._hero])<=6:
                self.move(obj, self._elem[obj].direction(self._elem[self._hero]))