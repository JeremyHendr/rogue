class Stairs(Element):
    def __init__(self,name="Stairs",abr="E"):
        Element.__init__(self,name,abr)

    def meet(self,hero):
        if isinstance(hero,Hero):
            theGame()._level += 1
            theGame().buildFloor()
            theGame().addMessage("The "+hero.name+" goes down")