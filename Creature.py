from Element import Element
import math,copy
from time import *
class Creature(Element):
    def __init__(self, name, hp, abr=False, strength=10, armor=0, armorpene=0.0, damagetype=None):
        Element.__init__(self, name, abr)
        self.hp = hp
        self.armor = armor
        self._strength = strength
        self.xp_value = self.hp*self._strength
        self.state = {}
        self.damage_type = damagetype
        self.game_state = "Idle"
        if armorpene > 1:
            armorpene = 1
        self.armor_penetration = armorpene

    def description(self):
        s = Element.description(self)
        return s+"("+str(self.hp)+")"

    def meet(self,other):
        from utiles import theGame
        from Hero import Hero
        if isinstance(other,Hero):
            if other.game_state == "Walking" or self.game_state == "Walking":
               return False
        # print("-> In meet",self,other)
        if other._strength-self.armor > 0:
            self.hp -= other._strength-(self.armor*(1-other.armor_penetration))
            theGame()._floor.damage_done.append({"coord":theGame()._floor.pos(self),"damage":other._strength-self.armor})
            theGame().addMessage("The "+str(other.name)+" hits the "+str(self.description()))
            theGame().damage_done.append({"coord":theGame()._floor.pos(self),"damage":other._strength-(self.armor*(1-other.armor_penetration)),"who":self})
            other.game_state = "Attack"
        if other.damage_type != None:
            self.state[other.damage_type[0]]=copy.deepcopy(other.damage_type[1])
            theGame().addMessage(self.name+" is "+" ".join([x for x in self.state.keys()]))
        if self.hp <= 0:
            # print("     dead",self)
            self.game_state = "Death"
            if isinstance(other, Hero):
                other.updateXp(self.xp_value)
                other.updateMana(int(math.log(self.xp_value/100)*2))
            return True
        return False

    def updateState(self):
        statetodelete = []
        for dic in self.state.items():
            print(dic)
            # print("state loop",state,state[0])
            if dic[0] == "poisoned":
                if self.meet(Creature("poison", 0, "", dic[1]["damage"] + self.armor)):
                    self.game_state = "Death"
                self.state[dic[0]]["damage"] += self.state[dic[0]]["damage"]
                if self.state[dic[0]]["time"] > 0:
                    self.state[dic[0]]["time"] -= 1
                else:
                    statetodelete.append(dic[0])
            elif dic[0] == "burning":
                if self.meet(Creature("fire", 0, "", dic[1]["damage"] + self.armor)):
                    self.game_state = "Death"
            elif dic[0] == "frozen":
                if self.state[dic[0]]["time"] > 0:
                    self.state[dic[0]]["time"] -= 1
                else:
                    statetodelete.append(dic[0])
        for state in statetodelete:
            self.state.pop(state)