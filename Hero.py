from Creature import Creature
from time import *

class Hero(Creature):
    def __init__(self, name="Hero", abbrv="@", hp=100, maxhp=100, strength=20, inventory=None, max_invent=10, maxmana=20):
        from Weapon import Weapon
        from Armor import Armor
        Creature.__init__(self, name, hp, abbrv, strength)
        if inventory == None:
            self._inventory = []
        else:
            self._inventory = inventory
        self.max_hp = maxhp
        self.max_invent = max_invent
        self.base_weapon = Weapon("wooden_stick","h",0)
        self.weapon = self.base_weapon
        self.base_protection = Armor("helmet","t",0)
        self.protection = self.base_protection
        self.level = 0
        self.xp = 1
        self.game_state = "Idle"
        self.attackdir = None
        self.walkingcoord = "E"
        self.wkcd = time()
        self.max_mana = maxmana
        self.mana = 20
        self.gold = 20
        self.armor_penetration = self.weapon.armor_penetration
        self.damage_type = self.weapon.damage_type

    def playDescription(self):
        return " ► "+self.name+" ◄  Weapon:"+self.weapon.name+" protection:"+self.protection.name+"\n"+"  Hp:"+str(self.hp)+" Strength:"+str(self._strength)+" Armor:"+str(self.armor)+" Mana:"+str(self.mana)+"/"+str(self.max_mana)+" gold:"+str(self.gold)+"\n"+str(self._inventory)

    def sethp(self,b):
        self.hp = b

    def take(self,elem):
        """
        :param elem: Element instance
        :return: True if the element has been taken, False else
        """
        from Equipment import Equipment
        from utiles import theGame
        if not isinstance(elem,Equipment):
            raise TypeError("not an Equipement",elem)
        name_inventory = [x.name for x in self._inventory]
        if elem.name == "gold":
            self.gold += 20
            return True
        elif len(name_inventory) < 7:
            if elem.unique or (elem.name not in name_inventory and elem.name != self.weapon.name and elem.name != self.protection.name):
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
        """
        use or equip an Equipement
        :param item: Equipement instance
        """
        from Weapon import Weapon
        from Armor import Armor
        from Equipment import Equipment
        # print("in hero use, with item",item)
        if item == None:
            return None
        if item not in self._inventory:
            raise ValueError("Not in inventory",item,self._inventory)

        if isinstance(item,Weapon) or isinstance(item,Armor):
            item.equip(self)
        elif isinstance(item,Equipment):
            item.use(self)

    def removeInventory(self,item):
        """
        remove the item from the inventory
        :param item: Equipement instance
        :return: None if the item hasnt been removed
        """
        from utiles import theGame
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
        """
        add xp to the hero when he kills a monster
        :param incr: integer, how many exp should be added
        """
        from utiles import theGame
        self.xp += incr
        list_key = [key for key in theGame().level_bonus.keys()]
        if self.level < len(theGame().level_bonus.keys()) and self.xp >= list_key[self.level]:
            for item in theGame().level_bonus[list_key[self.level]].items():
                self.__setattr__(item[0],self.__getattribute__(item[0])+item[1])
            self.updateLvl(1)
            theGame().addMessage("The hero gained " + str(incr) + " xp and gained one level")
        else:
            theGame().addMessage("The hero gained " + str(incr) + " xp")

    def updateMana(self,incr):
        """
        add or remove mana to the hero when he kills a monster or use a skill
        :param incr: integer, how many mana should be added or removed
        """
        from utiles import theGame
        # print("-> In updateMana  enter hero", self.mana,"/",self.max_mana)
        if self.mana+incr <= self.max_mana:
            self.mana += incr
            if incr > 0:
                theGame().addMessage("The hero gained " + str(incr) + " mana he has now"+str(self.mana)+"/"+str(self.max_mana))
            else:
                theGame().addMessage("The hero used " + str(incr) + " mana he has now"+str(self.mana)+"/"+str(self.max_mana))

    def healSkill(self):
        """first skill from the Hero"""
        from utiles import theGame,heal
        if self.mana >= 10:
            self.mana -= 10
            self.game_state = "Spell"
            heal(self,50)
            self.state["healing"] = {"dontworryaboutme"}
            for x in range(3):
                theGame()._floor.moveAllMonsters()

    def damageSkill(self):
        """seconde skill from the Hero"""
        from utiles import theGame
        if self.mana >= 10:
            self.mana -= 10
            self.game_state = "Spell"
            hero_pos = theGame()._floor.pos(self)
            todellist=[]
            for monster in theGame()._floor._elem.items():
                if isinstance(monster[0],Creature) and not isinstance(monster[0],Hero) and monster[1].distance(hero_pos)<=6:
                    monster[0].meet(Creature("Magic",40,"~"))
                    monster[0].state["decaying"] = {"dontworryaboutme"}
                    if monster[0].hp<=0:
                        todellist.append(monster[0])
            for i in todellist:
                del theGame()._floor._elem[i]
    def classSkill(self):
        """Special skill from the Hero"""
        from utiles import theGame
        if self.mana >= 10:
            self.mana -= 10
            self.game_state = "Spell"
            hero_pos = theGame()._floor.pos(self)
            for monster in theGame()._floor._elem.items():
                if isinstance(monster[0],Creature) and not isinstance(monster[0],Hero) and monster[1].distance(hero_pos)<=6:
                    monster[0].meet(Creature("Magic fire",0,"~",damagetype=["burning",{"damage":4,"time":3}]))
