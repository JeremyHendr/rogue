from Equipment import Equipment
class Armor(Equipment):
    """
    all armors you can find are an object from this class
    """
    def __init__(self,name,abr=False,incr=0):
        Equipment.__init__(self,name,abr,False)
        self.incr = incr

    def equip(self,creature):
        """
        :param creature: Creature instance, most of the time the Hero
        :return:
        """
        from utiles import theGame
        print("-> In armor equip with", self.name, "actual protection", creature.protection)
        if creature.protection != self:
            #print(self,self.incr)
            theGame().addMessage("The hero equiped a " + self.name + " and gained " + str(self.incr - creature.protection.incr) + " armor")
            creature.armor += self.incr
            creature._inventory.pop(creature._inventory.index(self))
            creature._inventory.append(creature.protection)
            creature.protection = self