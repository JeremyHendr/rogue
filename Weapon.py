from Equipment import Equipment
from Bullet import Bullet

class Weapon(Equipment):
    def __init__(self,name,abr=False,incr=0,armorpene=0,damagetype=None,range=False,blspeed=0,):
        Equipment.__init__(self,name,abr,False)
        self.strength = incr
        self.armor_penetration = armorpene
        self.damage_type = damagetype
        self.range = range
        if range:
            self.bulletspeed = blspeed


    def equip(self, creature):
        from utiles import theGame
        print("-> In Weapon equip with",self.name,"actual Weapon",creature.weapon)
        if creature.weapon != self:
            theGame().addMessage("The hero equiped a " + self.name+" and gained "+str(self.strength-creature.weapon.strength)+" strength")
            creature._strength -= creature.weapon.strength
            creature._strength += self.strength
            creature._inventory.pop(creature._inventory.index(self))
            creature._inventory.append(creature.weapon)
            creature.weapon = self
            creature.armor_penetration = creature.weapon.armor_penetration
            creature.damage_type = creature.weapon.damage_type

    # def unequip(self,creature): #a verifier
    #     print("-> In Weapon unequip with", self.name, "actual Weapon", creature.weapon)
    #     if creature.weapon == self:
    #         theGame().addMessage("The hero unequiped a " + self.name+" and lost "+str(self.incr)+" strength")
    #         creature._strength -= self.incr
    #         creature._inventory.pop(creature._inventory.index(creature.bare_hand))
    #         creature._inventory.append(creature.weapon)
    #         creature.weapon = creature.bare_hand