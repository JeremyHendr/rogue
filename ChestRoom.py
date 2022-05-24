from Room import Room
from Map import Map

class ChestRoom(Room):
    def __init__(self,cc1,cc2):
        Room.__init__(self,cc1,cc2)

    def decorate(self,map):
        from utiles import theGame
        from Chest import Chest
        if map.get(self.center()) == Map.ground:
            map.put(self.center(),Chest("Chest","▄",[theGame().randEquipment() for x in range(1)]))
        else:
            print("center not empty for chest room")