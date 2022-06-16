import pygame
class images:
    def __init__(self):
        self.img = {}
        self.buildup()
        
    def buildup(self):
        self.img["heal potion"] = pygame.image.load("Assets/potionRed.png")
        self.img["gold"] = pygame.image.load("Assets/coin.png")
        self.img["stick"] = pygame.image.load("Assets/upg_spear.png")
        self.img["sword"] = pygame.image.load("Assets/sword.png")
        self.img["telepotion"] = pygame.image.load("Assets/potionBlue.png")
        self.img["portoloin"] = pygame.image.load("Assets/potionGreen.png")
        self.img["axe"] = pygame.image.load("Assets/axe.png")

        
        self.img["heavy_armor"] = pygame.image.load("Assets/upg_armor.png")
        self.img["armor"] = pygame.image.load("Assets/armor.png")
        self.img["hammer"] = pygame.image.load("Assets/hammer.png")
        self.img["katana"] = pygame.image.load("Assets/Mainkatana.png")
        self.img["glock"] = pygame.image.load("Assets/Glock.png")
        self.img["frozone"] = pygame.image.load("Assets/FreezeAxe.png")
        
        self.img["Stairs"] = pygame.image.load("Assets/upExit.gif")
        self.img["chest"] = pygame.image.load("Assets/chest.gif")
        self.img["chestpresentation1"] = pygame.image.load("Assets/Maps/3.png")
        self.img["minimap"] = pygame.image.load("Assets/Maps/1.png")
        self.img["chainmail"] = pygame.image.load("Assets/upg_armor.png")
        self.img["wooden_stick"] = pygame.image.load("Assets/club.gif")
        self.img["imgnotdefined"] = pygame.image.load("Assets/Ahammer1.png")
        self.img["helmet"] = pygame.image.load("Assets/helmet.png")
        self.img["orb1"] = pygame.image.load("Assets/Orb/itsmars_orb_back1.png")
        self.img["orb2"] = pygame.image.load("Assets/Orb/itsmars_orb_back2.png")
        self.img["orb3"] = pygame.image.load("Assets/Orb/test.png")
        self.img["orb4"] = pygame.image.load("Assets/Orb/DarkOrbBorder.png")
        self.img["orb5"] = pygame.image.load("Assets/Orb/itsmars_orb_highlight.png")
        self.img["orb6"] = pygame.image.load("Assets/Orb/itsmars_orb_shadow.png")
        self.img["orb7"] = pygame.image.load("Assets/Orb/itsmars_scroll_fill.png")
        self.img["orb8"] = pygame.image.load("Assets/Orb/itsmars_scroll_lip.png")
        self.img["invplaceholder"] = pygame.image.load("Assets/Inv sprites/0.gif")
        self.img["invweapon"] = pygame.image.load("Assets/Inv sprites/21.gif")
        self.img["invarmor"] = pygame.image.load("Assets/Inv sprites/39.gif")
        self.img["manabg"] = pygame.image.load("Assets/Bar1.png")
        self.img["gamebg"] = pygame.image.load("Assets/background.png")
        wa = "wall1/"
        fl = "floor1/"
        self.img["║"] = pygame.image.load("Assets/Concrete/"+wa+"2.png")
        self.img["═"] = pygame.image.load("Assets/Concrete/"+wa+"10.png")
        self.img["╝"] = pygame.image.load("Assets/Concrete/"+wa+"9.png")
        self.img["╚"] = pygame.image.load("Assets/Concrete/"+wa+"8.png")
        self.img["╗"] = pygame.image.load("Assets/Concrete/"+wa+"1.png")
        self.img["╔"] = pygame.image.load("Assets/Concrete/"+wa+"0.png")
        self.img["╠"] = pygame.image.load("Assets/Concrete/"+wa+"11.png")
        self.img["╣"] = pygame.image.load("Assets/Concrete/"+wa+"12.png")
        self.img["╩"] = pygame.image.load("Assets/Concrete/"+wa+"4.png")
        self.img["╦"] = pygame.image.load("Assets/Concrete/"+wa+"3.png")
        self.img["╬"] = pygame.image.load("Assets/Concrete/"+wa+"7.png")
        self.img["#"] = pygame.image.load("Assets/Concrete/"+wa+"47.png")
        self.img["¤"] = pygame.image.load("Assets/Concrete/"+wa+"30.png")
        
        self.img["sol"] = pygame.image.load("Assets/Concrete/"+fl+"16.png")
        
        self.img["TitleScreen"] = pygame.image.load("Assets/UI/TitleScreen.png")
        self.img["frozen"] = pygame.image.load("Particles/Ice/Ice.png")
        self.img["AttackN"] = pygame.image.load("Hero.sprites/Attack/AttackN.png")
        
        
        
        
        