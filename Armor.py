from Equipment import Equipment
from utiles import theGame
class Armor(Equipment):
    def __init__(self,name,abr=False,incr=0):
        Equipment.__init__(self,name,abr,False)
        self.incr = incr

    def equip(self,creature):
        print("-> In armor equip with", self.name, "actual protection", creature.protection)
        if creature.protection != self:
            #print(self,self.incr)
            theGame().addMessage("The hero equiped a " + self.name + " and gained " + str(self.incr - creature.protection.incr) + " armor")
            creature.armor += self.incr
            creature._inventory.pop(creature._inventory.index(self))
            creature._inventory.append(creature.protection)
            creature.protection = self