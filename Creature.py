from Element import Element
import math
class Creature(Element):
    def __init__(self, name, hp, abr=False, strength=10, armor=0, damagetype=None):
        Element.__init__(self, name, abr)
        self.hp = hp
        self.armor = armor
        self._strength = strength
        self.xp_value = self.hp*self._strength
        self.state = {}
        self.damage_type = damagetype

    def description(self):
        s = Element.description(self)
        return s+"("+str(self.hp)+")"

    def meet(self,other):
        from utiles import theGame
        from Hero import Hero
        print("-> In meet",self,other)
        print(other.damage_type,self.state)
        if other._strength-self.armor > 0:
            self.hp -= other._strength-self.armor
            theGame().addMessage("The "+str(other.name)+" hits the "+str(self.description()))
        if other.damage_type != None:
            self.state[other.damage_type[0]]=other.damage_type[1]
            theGame().addMessage(self.name+" is "+" ".join([x for x in self.state.keys()]))
        print(self.state)
        if self.hp <= 0:
            if isinstance(other, Hero):
                other.updateXp(self.xp_value)
                other.updateMana(int(math.log(self.xp_value/100)*2))
            return True
        return False