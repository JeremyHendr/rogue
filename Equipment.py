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