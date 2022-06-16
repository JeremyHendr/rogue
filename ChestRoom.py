from Room import Room
from Map import Map

class ChestRoom(Room):
    def __init__(self,cc1,cc2):
        """
        :param cc1: Coord instance, top left coord
        :param cc2:  Coord instance,  bottom right coord
        """
        Room.__init__(self,cc1,cc2)

    def decorate(self,map):
        """
        re-writing of the decorate methode from room, because they are no monster or equipement placed on those rooms
        :param map: Map instance
        """
        from utiles import theGame
        from Chest import Chest
        if map.get(self.center()) == Map.ground:
            map.put(self.center(),Chest("Chest","▄",[theGame().randEquipment() for x in range(1)]))
        else:
            print("center not empty for chest room")