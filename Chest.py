from Element import Element
class Chest(Element):
    """
    a chest than can be opened by the hero and contains one item
    herits from the Element class
    """
    def __init__(self,name="Chest",abbr=False,content=[]):
        Element.__init__(self,name,abbr)
        self.content=content
        print("chest contains",content)

    def description(self):
        return "<"+self.name+" "+str(el.name for el in self.content)+">"

    def meet(self,creature):
        """
        add the content to the creature inventory is the conditions are satisfied
        :param creature: Hero instance
        """
        from Hero import Hero
        from utiles import theGame
        if isinstance(creature,Hero):
            elem = theGame().select(self.content)
            if isinstance(elem,Element) and creature.take(elem):
                self.content.pop(self.content.index(elem))
                theGame()._floor.rm(theGame()._floor.pos(self))