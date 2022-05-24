from Creature import Creature
from Weapon import Weapon
from Armor import Armor
from Equipment import Equipment
from utiles import theGame,heal
class Hero(Creature):
    def __init__(self, name="Hero", abbrv="@", hp=100, maxhp=100, strength=20, inventory=None, max_invent=10, maxmana=20):
        Creature.__init__(self, name, hp, abbrv, strength)
        if inventory == None:
            self._inventory = []
        else:
            self._inventory = inventory
        self.max_hp = maxhp
        self.max_invent = max_invent
        self.base_weapon = Weapon("hand","h",0)
        self.Weapon = self.base_weapon
        self.base_protection = Armor("t-shirt","t",0)
        self.protection = self.base_protection
        self.level = 0
        self.xp = 0
        self.max_mana = maxmana
        self.mana = 20
        self.gold = 20

    def playDescription(self):
        return " ► "+self.name+" ◄  Weapon:"+self.Weapon.name+" protection:"+self.protection.name+"\n"+"  Hp:"+str(self.hp)+" Strength:"+str(self._strength)+" Armor:"+str(self.armor)+" Mana:"+str(self.mana)+"/"+str(self.max_mana)+" gold:"+str(self.gold)+"\n"+str(self._inventory)

    def sethp(self,b):
        self.hp = b

    def take(self,elem):
        if not isinstance(elem,Equipment):
            raise TypeError("not an Equipement",elem)
        name_inventory = [x.name for x in self._inventory]
        # print(elem,self._inventory,self.Weapon,self.protection)
        # print(name_inventory,elem.name)
        # print("all",elem.unique or (elem.name not in name_inventory and elem.name != self.Weapon.name and elem.name != self.protection.name))
        # print(elem.unique,elem.name not in name_inventory,elem.name != self.Weapon.name, elem.name != self.protection.name)
        if elem.name == "gold":
            self.gold += 20
            return True
        elif len(name_inventory) < 9:
            if elem.unique or (elem.name not in name_inventory and elem.name != self.Weapon.name and elem.name != self.protection.name):
                self._inventory.append(elem)
                # theGame()._floor.rm(theGame()._floor.pos(self))
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

        if isinstance(item,Weapon) or isinstance(item,Armor):
            item.equip(self)
        elif isinstance(item,Equipment):
            item.use(self)

    def removeInventory(self,item):
        if item == None:
            return None
        if item.name==self.base_protection.name or item.name==self.base_weapon.name:
            theGame().addMessage("You cant remove this item from your inventory")
            return None
        self._inventory.pop(self._inventory.index(item))
        theGame().addMessage("You removed a"+item.name+" from your inventory")

    def updateLvl(self,incr):
        self.level += incr
        self.hp = self.max_hp

    def updateXp(self,incr):
        print("-> In update XP  enter hero",self.xp,self.level)
        self.xp += incr
        list_key = [key for key in theGame().level_bonus.keys()]
        print(self.level < len(theGame().level_bonus.keys()))
        if self.level < len(theGame().level_bonus.keys()) and self.xp >= list_key[self.level]:
            for item in theGame().level_bonus[list_key[self.level]].items():
                print("attr",item[0],self.__getattribute__(item[0]),item[1])
                self.__setattr__(item[0],self.__getattribute__(item[0])+item[1])
                print(item[1],"added to",self.__getattribute__(item[0]))
            self.updateLvl(1)
            theGame().addMessage("The hero gained " + str(incr) + " xp and gained one level")
        else:
            theGame().addMessage("The hero gained " + str(incr) + " xp")
        print("exit hero", self.xp, self.level)

    def updateMana(self,incr):
        print("-> In updateMana  enter hero", self.mana,"/",self.max_mana)
        if self.mana+incr <= self.max_mana:
            self.mana += incr
            if incr > 0:
                theGame().addMessage("The hero gained " + str(incr) + " mana he has now"+str(self.mana)+"/"+str(self.max_mana))
            else:
                theGame().addMessage("The hero used " + str(incr) + " mana he has now"+str(self.mana)+"/"+str(self.max_mana))

    def healSkill(self):
        if self.mana >= 10:
            self.mana -= 10
            heal(self,50)
            for x in range(3):
                theGame()._floor.moveAllMonsters()

    def damageSkill(self):
        if self.mana >= 10:
            self.mana -= 10
            hero_pos = theGame()._floor.pos(self)
            for room in theGame()._floor._rooms:
                if hero_pos in room:
                    for monster in theGame()._floor._elem.items():
                        # print(type(monster[0]),type(monster[1]),monster)
                        # print(isinstance(monster[0],Creature) and not isinstance(monster[0],Hero) and monster[1] in room,isinstance(monster,Creature),not isinstance(monster,Hero),monster[1] in room)
                        if isinstance(monster[0],Creature) and not isinstance(monster[0],Hero) and monster[1] in room:
                            theGame().addMessage(str(monster)+"lost 10 hp")
                            monster[0].hp -= 10
                            # verifier si mort-

    def classSkill(self):
        if self.mana >= 20:
            self.mana -= 20