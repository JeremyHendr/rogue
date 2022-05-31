from Equipment import Equipment
from Weapon import Weapon
from Armor import Armor
from Creature import Creature
from Coord import Coord
from Hero import Hero
from Classes import *
import random,copy,math
from touches import touches
from mainloop import mainloop
class Game():

    def __init__(self,hero=Hero(), level=1, floor=None):
        from utiles import heal, teleport, cheat_hp, cheat_str
        self.equipments = {0: [Equipment("gold", "o"),Equipment("heal potion", "!", True, lambda creature, rv=False: heal(creature, 30)),Equipment("telepotion", "!", True, lambda creature, rv=False: teleport(creature))],
                        1: [Weapon("stick", "|", 10)],
                        2: [Weapon("axe", "a", 20)],
                        3: [Equipment("portoloin", "p", False, lambda creature, rv=False: teleport(creature)),Weapon("sword", "s", 40), Armor("chainmail", "c", 5)],
                        5: [Weapon("chainBraker","§",15,armorpene=0.5),Weapon("frostBlade","f",15,damagetype=["frozen", {"time": 3, "damage": 0}])],
                        10: [Weapon("katana", "k", 60), Armor("himo", "h", 10)]}
        self.monsters = {0: [Creature("Goblin", 40), 
                             Creature("Bat", 20, "W")],
                    1: [Creature("Ork", 60, strength=20),
                        Creature("Blob", 100),
                        Creature("Spyder", 20, "S", 10, damagetype=["poisoned", {"time": 3, "damage": 5}])],
                    3: [Creature("Ice Golem",300,"I",2, damagetype=["frozen", {"time":3,"damage":0}])],
                    5: [Creature("Stone Dragon", 200, "D", strength=20, armor=20),
                        Creature("Fire Dragon", 200, "F", 10, damagetype=["burning", {"time": 5, "damage": 10}])],
                    50: [Creature("Zeus", 1000, strength=50)]}
        self._actions = { "z": lambda hero: self._floor.move(hero, Coord(0, -1)),
                        "s": lambda hero: self._floor.move(hero, Coord(0, 1)),
                        "q": lambda hero: self._floor.move(hero, Coord(-1, 0)),
                        "d": lambda hero: self._floor.move(hero, Coord(1, 0)),
                        "i": lambda hero: self.addMessage(hero.fullDescription()),
                        "k": lambda hero: hero.sethp(0),
                        " ": lambda hero: None,
                        "u": lambda hero: hero.use(self.select(hero._inventory)),
                        "y": lambda hero: hero.removeInventory(self.select(hero._inventory)),
                        "a": lambda hero: hero.healSkill(),
                        "e": lambda hero: hero.damageSkill(),
                        "r": lambda hero: hero.classSkill(),
                        "b": lambda hero: cheat_hp(hero),
                        "n": lambda hero: cheat_str(hero),
                        "v": lambda hero: self._floor.put(self._floor._rooms[0].randEmptyCoord(self._floor),self.randEquipment()),
                        "c": lambda hero: self._floor.put(self._floor._rooms[0].randEmptyCoord(self._floor),self.randMonster()),}
        self.level_bonus = {3000: {"max_hp": 10, "_strength": 0, "armor": 0},
                       6000: {"max_hp": 10, "_strength": 0, "armor": 0},
                       9000: {"max_hp": 10, "_strength": 0, "armor": 0},
                       15000: {"max_hp": 10, "_strength": 0, "armor": 0},
                       30000: {"max_hp": 20, "_strength": 5, "armor": 0},
                       50000: {"max_hp": 20, "_strength": 5, "armor": 5},
                       80000: {"max_hp": 20, "_strength": 10, "armor": 5}}

        self._hero = hero
        self._level = level
        self._floor = floor
        self._message = []
        self.ml  = ""

    def buildFloor(self):
        from Map import Map
        from Stairs import Stairs
        print("Xp at new lvl buil",self._hero.xp,"lvl:",self._level)
        self._floor = Map(hero=self._hero)
        self._floor.put(self._floor._rooms[0].center(), self._floor._hero)
        self._floor.put(self._floor._rooms[-1].center(), Stairs())
        for room in self._floor._rooms:
            room.decorate(self._floor)
        mainloop.carte = self._floor

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

        # waepon_rarety_list = [x for x in collection.keys() if x <= self._level]
        # weight_list = [1/(1+x) for x in collection.keys() if x <= self._level]
        # print(collection,waepon_rarety_list,weight_list)
        # return random.choice(copy.deepcopy(collection[random.choices(waepon_rarety_list,weight_list)[0]]))

    def randEquipment(self):
        return self.randElement(self.equipments)

    def randMonster(self):
        return self.randElement(self.monsters)

    def select(self,l):
        return self.ml.chestselect(l)

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        self.touches = touches()
        self.addMessage("test")
        self.ml = mainloop(self._floor)
        while self._hero.hp > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._hero.sethp(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_souris = event.pos
                    self.touches.pressed["click"] = position_souris
                    print("pos = ", position_souris)
                if event.type == pygame.KEYDOWN:
                    self.touches.pressed[event.key] = True

            self.ml.animation(self.readMessages(), self.touches)
            self.ml.realtime()
        print("--- Game Over ---")