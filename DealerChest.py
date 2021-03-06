from Chest import Chest
class DealerChest(Chest):
    """
    a special chest that contains three Equipment instance, you can withdraw one of them against gold
    """
    def __init__(self,name="Chest",abbr=False,content=[]):
        Chest.__init__(self,name,abbr,content)

    def meet(self,creature):
        """
        rewriting of the meet methode to have a special interaction with this chest
        :param creature:
        :return:
        """
        from Hero import Hero
        from utiles import theGame
        from Element import Element
        if isinstance(creature,Hero):
            print("Prices are: "+"  ".join([x.name+": "+str(self.price(x)) for x in self.content])) #laisser ce print
            elem = theGame().select(self.content)
            if isinstance(elem,Element) and creature.gold-self.price(elem)>= 0 and creature.take(elem):
                self.content.pop(self.content.index(elem))
                theGame()._floor.rm(theGame()._floor.pos(self))
                creature.gold -= self.price(elem)
            else:
                print("already in inventory or not enough gold")

    def price(self,e):
        from utiles import theGame
        """
        return the price of the element e, supposed to be in self.content
        price based on rarity +1 *10
        """
        for l in theGame().equipments.items():
            for obj in l[1]:
                if type(e)==type(obj):
                    return (l[0]+1)*10