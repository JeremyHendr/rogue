from Equipment import Equipment

class Weapon(Equipment):
    def __init__(self,name,abr=False,incr=0):
        Equipment.__init__(self,name,abr,False)
        self.incr = incr

    def equip(self, creature):
        from utiles import theGame
        print("-> In Weapon equip with",self.name,"actual Weapon",creature.Weapon)
        if creature.Weapon != self:
            theGame().addMessage("The hero equiped a " + self.name+" and gained "+str(self.incr-creature.Weapon.incr)+" strength")
            creature._strength += self.incr
            creature._inventory.pop(creature._inventory.index(self))
            creature._inventory.append(creature.Weapon)
            creature.Weapon = self

    # def unequip(self,creature): #a verifier
    #     print("-> In Weapon unequip with", self.name, "actual Weapon", creature.Weapon)
    #     if creature.Weapon == self:
    #         theGame().addMessage("The hero unequiped a " + self.name+" and lost "+str(self.incr)+" strength")
    #         creature._strength -= self.incr
    #         creature._inventory.pop(creature._inventory.index(creature.bare_hand))
    #         creature._inventory.append(creature.Weapon)
    #         creature.Weapon = creature.bare_hand