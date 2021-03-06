from Coord import Coord
from Hero import Hero
from Creature import Creature
import random

class Map:
    """the main matrix where all elements of the game are stored"""
    # https://theasciicode.com.ar/extended-ascii-code/box-drawings-double-line-vertical-left-character-ascii-code-185.html
    #alt+ 200:╚ 201:╔  196─ '┬┬┴ 192└ 191┐ ¢ 188╝ 187╗ 186║  █ 219, ▄ 220, ▬ 22
    ground = "."
    empty = " "
    walllist = ["║", "═", "╝", "╚", "╗", "╔", "╠", "╣", "╩", "╦", "╬", "#","¤"]
    dir = {'z': Coord(0,-1),
                's': Coord(0,1),
                'd': Coord(1,0),
                'q': Coord(-1,0)}

    def __init__(self,size=22,hero=Hero(),nbrooms=7):
        self.nbrooms = nbrooms
        self.size = size
        self._hero = hero
        self._elem = {}
        self._mat = []
        self._roomsToReach = []
        self._rooms = []
        l = [Map.empty for i in range(self.size)]
        self._mat = [l.copy() for j in range(self.size)]
        self.generateRooms(nbrooms)
        self.reachAllRooms()
        self.putWalls()
        self.hidden_elem = []
        self.damage_done = []
        self.fov = 4
        self.to_delete_list = []
        self.currentFoGMap = []

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
        """make sure the coordinates c are in the matrix"""
        if not isinstance(c,Coord):
            raise TypeError('Not a Coord',c)
        if not (0 <= c.x and c.x < self.size and 0 <= c.y and c.y < self.size):
            raise  IndexError('Out of map coord',c)

    def checkElement(self,e):
        """make sure the element e is an Element instance"""
        from Element import Element
        if not isinstance(e,Element):
            raise TypeError('Not a Element',e)

    def get(self,c):
        """
        :param c: Coord instance
        :return: the item on the coordinate c
        """
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self,item):
        """
        :param item: Element instance
        :return: an Coord instance of the coordinate from item in the map
        """
        self.checkElement(item)
        for i in range(len(self._mat)):
            if item in self._mat[i]:
                return Coord(self._mat[i].index(item),i)
        return None

    def put(self,c,item):
        """
        places the item on the coordinate c in the map
        :param c: Coord instance
        :param item: Element instance
        :return: None
        """
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
        """
        remove the element on the coordinate c
        :param c: Coord instance
        """
        # self.checkCoord(c)
        del self._elem[self.get(c)]
        self._mat[c.y][c.x] = Map.ground

    def addRoom(self,room):
        """
        add room in the map
        :param room: Room instance
        """
        self._roomsToReach.append(room)
        for x in range(len(self)):
            for y in range(len(self)):
                if Coord(x,y) in room:
                    self._mat[y][x] = Map.ground

    def findRoom(self,coord):
        """
        :param coord: Coord instance
        :return: the room that contains the coordinate c
        """
        for i in self._roomsToReach:
            if coord in i:
                return i
        return False

    def intersectNone(self,room):
        """
        make sure that there is enough space for the room in the map
        :param room:
        :return: True if it intersects with no other rooms, False else
        """
        for i in self._roomsToReach:
            if i.intersect(room):
                return False
        return True

    def dig(self,coord):
        """
        replace the coord in map with Map.ground
        :param coord: Coord instance
        """
        self._mat[coord.y][coord.x] = Map.ground
        a = self.findRoom(coord)
        if a != False:
            self._roomsToReach.pop(self._roomsToReach.index(a))
            self._rooms.append(a)

    def corridor(self,start,end):
        """
        make a corridor between start and end
        :param start: Room instance
        :param end: Room instance
        """
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
            choice = random.choices(["room","chest_room","waepon_dealer_room"],[15,1,1])[0]
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
        """
        :param c: Coord instance
        :return: return True if there is anything else than Map.empty around the coordinate c, False else
        """
        from Coord import Coord
        for x in (c.x-1,c.x+1):
            for y in (c.y-1,c.y+1):
                if Coord(x,y) in self and not Coord(x,y) == c and self.get(Coord(x,y)) != Map.empty and self.get(Coord(x,y)) != "#":
                    return True

    def surroundingWallsCardinal(self,c):
        """
        :param c: Coord instance
        :return: a list of cardinal point (N,S,E,O) indicating where the surrounding walls are
        """
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
        """places walls all around the rooms and corridors"""
        from Coord import Coord
        #self._mat.insert(0,[Map.empty for i in range(self.size)])
        
        for x in range(len(self)):
            for y in range(len(self)):
                if self.get(Coord(x,y)) == Map.empty and self.surroundingElementsCoord(Coord(x,y)):
                    self._mat[y][x] = "#"

        for x in range(len(self)):
            for y in range(len(self)):
                if self.get(Coord(x,y)) == "#":
                    card_point_list = self.surroundingWallsCardinal(Coord(x,y))
                    # print(Coord(x,y),self.get(Coord(x,y)),card_point_list)
                    if len(card_point_list) == 1:
                        if "S" in card_point_list or "N" in card_point_list:
                            self._mat[y][x] = "║"
                        elif "E" in card_point_list or "O" in card_point_list:
                            self._mat[y][x] = "═"
                    elif len(card_point_list) == 2:
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

    def move(self, e, way):
        """
        Moves the element e in the direction way
        :param e: Element instance
        :param way: Coord instance, direction where the element should move
        """
        from Equipment import Equipment
        from Creature import Creature
        
        # print("-> In move with",e,way,e.state)
        orig = self.pos(e)
        dest = orig + way
        
        if dest in self and not self.get(dest) in Map.walllist:
            if self.get(dest) == Map.ground and not "frozen" in e.state:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
                e.game_state = "Walking"
            elif self.get(dest) != Map.empty and not "frozen" in e.state:
                # si l'elem a ete mis dans l'inventaire ou le monstre tue
                if self.get(dest).meet(e):
                    e.game_state = "Attack"
                    # si c'est pas un monstre on suppr la dest puis on bouge
                    if not isinstance(self.get(dest), Creature):
                        self.rm(dest)
                        self._mat[orig.y][orig.x] = Map.ground
                        self._mat[dest.y][dest.x] = e
                        self._elem[e] = dest
                        e.game_state = "Walking"
                    # else:  # si c'est un monstre on supprime juste la dest
                    #     self.rm(dest)
                elif isinstance(self.get(dest), Equipment):
                    # print("hidden elem append",self.get(dest),type(self.get(dest)),self.get(dest) in self._elem,self._elem)
                    self.hidden_elem.append([dest, self.get(dest)])
                    self._mat[dest.y][dest.x] = Map.ground
                    self._mat[orig.y][orig.x] = Map.ground
                    self._mat[dest.y][dest.x] = e
                    self._elem[e] = dest
                    e.game_state = "Walking"
                    


            for elem in self.hidden_elem:
                if self.get(elem[0]) == Map.ground:
                    self._mat[elem[0].y][elem[0].x] = elem[1]
                    self.hidden_elem.pop(self.hidden_elem.index(elem))

    def moveAllMonsters(self):
        """moves all the monsters on the map if they are at less than 6 block away"""
        from Creature import Creature
        global rep
        temp = self._elem.copy()
        for obj in temp:
            if obj in self._elem and self.pos(obj) not in self.to_delete_list and isinstance(obj,Creature) and obj!=self._hero and self._elem[obj].distance(self._elem[self._hero])<=6:
                self.move(obj, self._elem[obj].direction(self._elem[self._hero]))
        # print("todellist",self.to_delete_list)
        for c in self.to_delete_list:
            self.rm(c)
            self.to_delete_list.pop(self.to_delete_list.index(c))
            
    def fogOfWar(self):
        """
        :return:  a matrix of the blocks surrounding the Hero
        """
        from Coord import Coord
        self.currentFoGMap = []
        x, y = self.pos(self._hero).x, self.pos(self._hero).y
        coingauche = Coord(x-self.fov, y+self.fov)
        coindroit = Coord(x+self.fov, y - self.fov)
        a, b = -1, -1
        # print(coingauche,coindroit,x,y)
        c = []
        for i in self._mat:
            b += 1
            d = []
            for k in i:
                a += 1
             #   print("a = ",a,"b = ",b, d)
                if a >= coingauche.x and a <= coindroit.x and b >= coindroit.y and b <= coingauche.y:
                    d.append(k)
                    self.currentFoGMap.append([b,a])
                    #print("a = ",a,b,d)
                    # sleep(2)
            a = -1
            if len(d) > 0:
                c.append(d)
        return c