from Room import Room
from Map import Map
from DealerChest import DealerChest
from utiles import theGame
class ShopRoom(Room):
    def __init__(self,cc1,cc2):
        Room.__init__(self,cc1,cc2)

    def decorate(self,map):
        if map.get(self.center()) == Map.ground:
            map.put(self.center(),DealerChest("weapon dealer", "&", [theGame().randEquipment() for x in range(3)]))
        else:
            print("center not empty for chest room")