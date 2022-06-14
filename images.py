import pygame
class images:
    def __init__(self):
        self.img = {}
        self.buildup()
        
    def buildup(self):
        self.img["heal potion"] = pygame.image.load("64/potionRed.png")
        self.img["gold"] = pygame.image.load("64/coin.png")
        self.img["!"] = pygame.image.load("Silmar/items/potion.gif")
        self.img["stick"] = pygame.image.load("64/upg_spear.png")
        self.img["sword"] = pygame.image.load("64/sword.png")
        self.img["telepotion"] = pygame.image.load("64/potionBlue.png")
        self.img["portoloin"] = pygame.image.load("64/potionGreen.png")
        self.img["axe"] = pygame.image.load("64/axe.png")
        self.img["Hero"] = pygame.image.load("Silmar/monsters/cyclops.gif")
        self.img["dragon"] = pygame.image.load("Monsters/DragonAdultSilver.png") 
        
        self.img["heavy_armor"] = pygame.image.load("64/upg_armor.png")
        self.img["armor"] = pygame.image.load("64/armor.png")
        self.img["hammer"] = pygame.image.load("64/hammer.png")
        self.img["katana"] = pygame.image.load("Katana/Mainkatana.png")
        self.img["glock"] = pygame.image.load("Glock.png")
        self.img["frozone"] = pygame.image.load("64/FreezeAxe.png")
        
        self.img["Stairs"] = pygame.image.load("Silmar/terrain/upExit.gif")
        self.img["chest"] = pygame.image.load("Silmar/chest.gif")
        self.img["chestpresentation1"] = pygame.image.load("test gui/GUI/Maps/3.png")
        self.img["minimap"] = pygame.image.load("test gui/GUI/Maps/1.png")
        self.img["chainmail"] = pygame.image.load("64/upg_armor.png")
        self.img["hand"] = pygame.image.load("Silmar/items/club.gif")
        self.img["imgnotdefined"] = pygame.image.load("Items/Ahammer1.png")
        self.img["orb1"] = pygame.image.load("Orb/itsmars_orb_back1.png")
        self.img["orb2"] = pygame.image.load("Orb/itsmars_orb_back2.png")
        self.img["orb3"] = pygame.image.load("Orb/test.png")
        self.img["orb4"] = pygame.image.load("Orb/DarkOrbBorder.png")
        self.img["orb5"] = pygame.image.load("Orb/itsmars_orb_highlight.png")
        self.img["orb6"] = pygame.image.load("Orb/itsmars_orb_shadow.png")
        self.img["orb7"] = pygame.image.load("Orb/itsmars_scroll_fill.png")
        self.img["orb8"] = pygame.image.load("Orb/itsmars_scroll_lip.png")
        self.img["invplaceholder"] = pygame.image.load("test gui/GUI/Inv sprites/0.gif")
        self.img["invweapon"] = pygame.image.load("test gui/GUI/Inv sprites/21.gif")
        self.img["manabg"] = pygame.image.load("Bar1.png")
        wa = "wall1/"
        fl = "floor1/"
        self.img["║"] = pygame.image.load("test/Concrete/"+wa+"2.png")
        self.img["═"] = pygame.image.load("test/Concrete/"+wa+"10.png")
        self.img["╝"] = pygame.image.load("test/Concrete/"+wa+"9.png")
        self.img["╚"] = pygame.image.load("test/Concrete/"+wa+"8.png")
        self.img["╗"] = pygame.image.load("test/Concrete/"+wa+"1.png")
        self.img["╔"] = pygame.image.load("test/Concrete/"+wa+"0.png")
        self.img["╠"] = pygame.image.load("test/Concrete/"+wa+"11.png")
        self.img["╣"] = pygame.image.load("test/Concrete/"+wa+"12.png")
        self.img["╩"] = pygame.image.load("test/Concrete/"+wa+"4.png")
        self.img["╦"] = pygame.image.load("test/Concrete/"+wa+"3.png")
        self.img["╬"] = pygame.image.load("test/Concrete/"+wa+"7.png")
        self.img["#"] = pygame.image.load("test/Concrete/"+wa+"47.png")
        self.img["¤"] = pygame.image.load("test/Concrete/"+wa+"30.png")
        
        self.img["sol"] = pygame.image.load("test/Concrete/"+fl+"16.png")
        
        self.img["TitleScreen"] = pygame.image.load("UI/TitleScreen.png")
        self.img["frozen"] = pygame.image.load("Particles/Ice/Ice.png")
        self.img["AttackN"] = pygame.image.load("Hero.sprites/Attack/AttackN.png")
        
        
        
        
        