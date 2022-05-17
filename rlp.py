import random,copy,math
class Element:
    def __init__(self,name,abr=False):
        self.name = name
        if not abr:
            self._abbrv = self.name[0]
        else:
            self._abbrv = abr

    def __repr__(self):
        return self._abbrv

    def description(self):
        return "<"+self.name+">"

    def meet(self,hero):
        raise NotImplementedError("Not implemented yet")


class Creature(Element):
    def __init__(self, name, hp, abr=False, strength=1, armor=0):
        Element.__init__(self, name, abr)
        self.hp = hp
        self.armor = armor
        self._strength = strength

    def description(self):
        s = Element.description(self)
        return s+"("+str(self.hp)+")"

    def meet(self,other):
        # print("meet",self.hp,other._strength,self.armor)
        if other._strength-self.armor > 0:
            self.hp -= other._strength-self.armor
        # print("meet", self.hp)
        theGame().addMessage("The "+str(other.name)+" hits the "+str(self.description()))
        if other.hp <= 0:
            if isinstance(other, Hero):
                cpt, stop = 0, False
                for l in theGame.monsters.values():
                    for creature in l:
                        if self.name == creature.name:
                            stop = True
                            break
                        cpt += 1
                    if stop:
                        break
                other.xp += theGame().monsters.keys()[cpt]
                print("xp", elf.xp)
                theGame().addMessage("The hero gained " + str(theGame().monsters.keys()[cpt]) + " xp")
        if self.hp <= 0:
            return True
        # other.hp -= self._strength
        # theGame().addMessage("The "+str(self.name)+" hits the "+str(other.description()))
        return False

class Hero(Creature):
    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, inventory=None, max_invent=9):
        Creature.__init__(self, name, hp, abbrv, strength)
        if inventory == None:
            self._inventory = []
        else:
            self._inventory = inventory
        self.max_invent = max_invent
        self.base_wapon = Wapon("hand","h",0)
        self.wapon = self.base_wapon
        self.base_protection = Armor("t-shirt","t",0)
        self.protection = self.base_protection
        self.level = 1
        self.xp = 0

    def description(self):
        return " ► "+self.name+" ◄  wapon:"+self.wapon.name+" protection:"+self.protection.name+"\n"+"  Hp:"+str(self.hp)+" Strength:"+str(self._strength)+" Armor:"+str(self.armor)

    def sethp(self,b):
        self.hp = b

    def take(self,elem):
        if not isinstance(elem,Equipment):
            raise TypeError("not an Equipement",elem)
        name_inventory = [x.name for x in self._inventory]
        print(elem,self._inventory,self.wapon,self.protection)
        print(name_inventory,elem.name)
        print("all",elem.unique or (elem.name not in name_inventory and elem.name != self.wapon.name and elem.name != self.protection.name))
        print(elem.unique,elem.name not in name_inventory,elem.name != self.wapon.name, elem.name != self.protection.name)
        if len(name_inventory) < 9:
            if elem.unique or (elem.name not in name_inventory and elem.name != self.wapon.name and elem.name != self.protection.name):
                self._inventory.append(elem)
                return True
        else:
            theGame().addMessage("you dont have place enough in your inventory")
            return False

    def fullDescription(self):
        p = self.__dict__
        a = ""
        for i in p:
            if i != "_inventory" :
                if str(i)[0]=="_":
                    a = a  + "> " + str(i)[1:] + " : " + str(p[i]) + "\n"
                else:
                    a = a + "> " + str(i)[0:] + " : " + str(p[i]) + "\n"
            else:
                if len(p[i])>0:
                    c = []
                    for x in p[i]:
                        c.append(str(x))
                    b ="> " + "INVENTORY" + " : " + str(c)
                else:
                    b ="> " + "INVENTORY" + " : " + "[]"
        a += b
        return a

    def use(self,item):
        print("in hero use, with item",item)
        if item == None:
            return None
        if item not in self._inventory:
            raise ValueError("Not in inventory",item,self._inventory)

        if isinstance(item,Wapon) or isinstance(item,Armor):
            item.equip(self)
        elif isinstance(item,Equipment):
            item.use(self)

    def removeInventory(self,item):
        if item == None:
            return None
        if item.name==self.base_protection.name or item.name==self.base_wapon.name:
            theGame().addMessage("You cant remove this item from your inventory")
            return None
        self._inventory.pop(self._inventory.index(item))
        theGame().addMessage("You removed a"+item.name+" from your inventory")

class Equipment(Element):
    def __init__(self,name,abr=False,unique=True,usage=None):
        Element.__init__(self,name,abr)
        self.usage = usage
        self.unique = unique

    def meet(self,hero):
        if self._abbrv != Map.ground and isinstance(hero,Hero):
            if hero.take(self):
                theGame().addMessage("You pick up a "+self.name)
                return True
        return False

    def use(self,creature):
        print("-> In item use, with item",self.name,"unique:",self.unique,"avec creature",creature)

        if self.usage != None:
            if self.unique:
                creature._inventory.pop(creature._inventory.index(self))
            theGame().addMessage("The " + str(creature.name) +" uses the " + str(self.name))
            self.usage(creature)
            return True

        else:
            theGame().addMessage("The "+str(self.name)+" is not usable")
            return False

class Wapon(Equipment):
    def __init__(self,name,abr=False,incr=0):
        Equipment.__init__(self,name,abr,False)
        self.incr = incr

    def equip(self, creature):
        print("-> In wapon equip with",self.name,"actual wapon",creature.wapon)
        if creature.wapon != self:
            theGame().addMessage("The hero equiped a " + self.name+" and gained "+str(self.incr-creature.wapon.incr)+" strength")
            creature._strength += self.incr
            creature._inventory.pop(creature._inventory.index(self))
            creature._inventory.append(creature.wapon)
            creature.wapon = self

    # def unequip(self,creature): #a verifier
    #     print("-> In wapon unequip with", self.name, "actual wapon", creature.wapon)
    #     if creature.wapon == self:
    #         theGame().addMessage("The hero unequiped a " + self.name+" and lost "+str(self.incr)+" strength")
    #         creature._strength -= self.incr
    #         creature._inventory.pop(creature._inventory.index(creature.bare_hand))
    #         creature._inventory.append(creature.wapon)
    #         creature.wapon = creature.bare_hand

class Armor(Equipment):
    def __init__(self,name,abr=False,incr=0):
        Equipment.__init__(self,name,abr,False)
        self.incr = incr

    def equip(self,creature):
        print("-> In armor equip with", self.name, "actual protection", creature.protection)
        if creature.protection != self:
            print(self,self.incr)
            theGame().addMessage("The hero equiped a " + self.name + " and gained " + str(self.incr - creature.protection.incr) + " armor")
            creature.armor += self.incr
            creature._inventory.pop(creature._inventory.index(self))
            creature._inventory.append(creature.protection)
            creature.protection = self

class Stairs(Element):
    def __init__(self,name="Stairs",abr="E"):
        Element.__init__(self,name,abr)

    def meet(self,hero):
        if isinstance(hero,Hero):
            theGame()._level += 1
            theGame().buildFloor()
            theGame().addMessage("The "+hero.name+" goes down")

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
        self.put(self._rooms[0].center(),self._hero)
        for room in self._rooms:
            room.decorate(self)


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

    def corridor(self, start, end):
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

    def randRoom(self):
        """create a room with a random size on random coord"""
        x1 = random.randint(0,len(self) - 3)
        y1 = random.randint(0,len(self) - 3)
        x2 = min(len(self._mat)-1,x1+random.randint(3,8))
        y2 = min(len(self._mat)-1,y1+random.randint(3,8))
        return Room(Coord(x1,y1),Coord(x2,y2))

    def generateRooms(self,n):
        for i in range(n):
            roomido = self.randRoom()
            if self.intersectNone(roomido):
                self.addRoom(roomido)

    def move(self, e, way):
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        dest = orig + way
        if dest in self:
            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
            elif self.get(dest) != Map.empty and self.get(dest).meet(e) and self.get(dest) != self._hero:
                self.rm(dest)

    def moveAllMonsters(self):
        for obj in self._elem:
            if isinstance(obj,Creature) and obj!=self._hero and self._elem[obj].distance(self._elem[self._hero])<=6:
                self.move(obj, self._elem[obj].direction(self._elem[self._hero]))

##                                     ROOM
class Room:
    def __init__(self,cc1,cc2):
        self.c1=cc1
        self.c2=cc2

    def __repr__(self):
        return "["+str(self.c1)+", "+str(self.c2)+"]"

    def __contains__(self,a):
        return a.x>=self.c1.x and a.y>=self.c1.y and a.x<=self.c2.x and a.y<=self.c2.y

    def center(self):
        return Coord(((self.c2.x+self.c1.x)//2),((self.c2.y+self.c1.y)//2))

    def intersect(self,other):
       return (other.c1 in self) or (Coord(other.c1.x+(other.c2.x-other.c1.x), other.c1.y) in self) or (other.c2 in self) or (Coord(other.c2.x-(other.c2.x-other.c1.x), other.c2.y) in self) or (self.c1 in other) or (Coord(self.c1.x+(self.c2.x-self.c1.x), self.c1.y) in other) or (self.c2 in other) or (Coord(self.c2.x-(self.c2.x-self.c1.x), self.c2.y) in other)

    def randCoord(self):
        return Coord(random.randint(self.c1.x,self.c2.x),random.randint(self.c1.y,self.c2.y))

    def randEmptyCoord(self,map):
        a = self.randCoord()
        while True:
            if (map.get(a) == map.ground and a != self.center()):
                break
            a = self.randCoord()
        return a

    def decorate(self,map):
        hero_pos = map.pos(map._hero)
        while True:
            c = self.randEmptyCoord(map)
            print(hero_pos.distance(c))
            if hero_pos.distance(c) > 1:
                break
        map.put(c, theGame().randEquipment())
        while True:
            c = self.randEmptyCoord(map)
            if hero_pos.distance(c) > 1:
                break
        map.put(c, theGame().randMonster())

##                                     GAME
class Game():
    equipments = {  0: [Equipment("gold","o"),Equipment("heal potion","!",True,lambda creature,rv=False: heal(creature)), Equipment("telepotion","!",True,lambda creature,rv=False: teleport(creature))],
                    1: [Wapon("stick","|",1)],
                    2: [Wapon("axe","a",2)],
                    3: [Equipment("portoloin","p",False,lambda creature,rv=False: teleport(creature)), Wapon("sword","s",4),Armor("chainmail","c",1)]}
    monsters = {0: [ Creature("Goblin",4), Creature("Bat",2,"W") ],
                1: [ Creature("Ork",6,strength=2), Creature("Blob",10)],
                5: [ Creature("Dragon",20,strength=3) ]}
    _actions = {"z": lambda hero: theGame()._floor.move(hero, Coord(0,-1)),
                "s": lambda hero: theGame()._floor.move(hero, Coord(0,1)),
                "q": lambda hero: theGame()._floor.move(hero, Coord(-1,0)),
                "d": lambda hero: theGame()._floor.move(hero, Coord(1,0)),
                "i": lambda hero: theGame().addMessage(hero.fullDescription()),
                "k": lambda hero: hero.sethp(0),
                " ": lambda hero: None,
                "u": lambda hero: hero.use(theGame().select(hero._inventory)),
                "y": lambda hero: hero.removeInventory(theGame().select(hero._inventory)),
                "b": lambda hero: cheat_hp(hero),
                "n": lambda hero: cheat_str(hero),
                "v": lambda hero: theGame()._floor.put(theGame()._floor._rooms[0].randEmptyCoord(theGame()._floor),theGame().randEquipment()),
                "c": lambda hero: theGame()._floor.put(theGame()._floor._rooms[0].randEmptyCoord(theGame()._floor),theGame().randMonster())}

    def __init__(self,hero=Hero(), level=1, floor=None):
        self._hero = hero
        self._level = level
        self._floor = floor
        self._message = []

    def buildFloor(self):
        self._floor = Map(hero=self._hero)
        self._floor.put(self._floor._rooms[-1].center(),Stairs())

    def addMessage(self,msg):
        self._message.append(msg)

    def readMessages(self):
        rep = ""
        for m in self._message:
            rep+=m+". "
        self._message = []
        return rep

    def randElement(self,collection):
        rnd_exp = int(random.expovariate(1/self._level))
        while not rnd_exp in collection and rnd_exp>=0:
            rnd_exp -= 1
        return random.choice(copy.deepcopy(collection[rnd_exp]))

    def randEquipment(self):
        return self.randElement(self.equipments)

    def randMonster(self):
        return self.randElement(self.monsters)

    def select(self,l):
        p=[]
        for i in range(len(l)):
            if l[i].usage != None or isinstance(l[i],Wapon) or isinstance(l[i],Armor):
                p.append(str(i)+": "+l[i].name)
        print("Choose item>", p)
        a = getch()
        if a.isdigit() and int(a)<len(l):
            print(l[int(a)],type(l[int(a)]))
            return l[int(a)]
        return None

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self._hero.hp > 0:
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            print("entree getch",c)
            if c in Game._actions:
                if c == "y":
                    print("Be careful if you REMOVE an item from your inventory you CANT get it back")
                Game._actions[c](self._hero)
                self._floor.moveAllMonsters()
        print("--- Game Over ---")

def heal(creature):
    print("-> In heal")
    creature.hp += 3
    return True

def teleport(creature):
    print("-> In teleport")
    loc = random.choices(theGame()._floor._rooms)[0].randEmptyCoord(theGame()._floor)
    theGame().addMessage("The hero is now at "+str(loc))
    theGame()._floor.rm(theGame()._floor.pos(creature))
    theGame()._floor.put(loc,creature)


def cheat_hp(hero):
    print("CHEATING hp")
    hero.hp = 100000
def cheat_str(hero):
    print("CHEATING strength")
    hero._strength = 1000

##
def getch():
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')

def theGame(game = Game()):
    return game

#inventaire limité en sah le test


theGame().play()

