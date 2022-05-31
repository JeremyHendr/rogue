import pygame
from time import *
from Classes import *
from images import images
from touches import touches
from Coord import Coord
from Map import Map
from Creature import Creature 
from Hero import Hero
from PIL import Image

class mainloop:
    inv = True
    carte = ""

    def __init__(self, carte):
        mainloop.carte = carte
        self.page_actuelle = 1  # 1 étant le ² principal, 0 le menu et 2 l'inventaire
        self.nb_fps = 30
        self.nbtimers = 2  # on aura besoin de bcp de timers
        self.timers = [time() for i in range(self.nbtimers)]
        self.font = pygame.font.SysFont("Arial", 30)
        self.bg1test = pygame.image.load("Menu-Background.png")
        self.screencoords = (pygame.display.Info().current_w,
                             pygame.display.Info().current_h)
        self.imgsetter = images()
        self.pictures = self.imgsetter.img
        self.anim_lib = anim_total()
        self.anim_mat = {}
        self.startingaxis = None
        self.finishingaxis = None

    def animation(self, ms, tc):  # la boucle principale qui reprint tout
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.screencoords)
        #self.screen.blit(self.bg1test, (0, 0))
        # self.chat(ms)
        self.background()
        # self.foreground()
        self.action(tc.pressed)
        if self.inv:
            self.inventory_ui()
        self.health_bar()
        self.mana_bar()
        self.exp_bar()
        self.ui()
        pygame.display.update()

    def realtime(self):
        timer = self.timers[0]
        if time()-timer >= 0.7:
            self.timers[0] = time()
            self.carte.moveAllMonsters()
            for monster in self.carte._elem:
                if isinstance(monster, Creature):
                    monster.updateState()


        if self.carte._hero.game_state == "Attack" and time()-self.timers[1] > 1:
            self.timers[1] = time()
            direc = (pygame.mouse.get_pos()[0] > self.screencoords[0]/2)
            if not direc:
                direc = -1
            pos = self.carte.pos(self.carte._hero) + Coord(direc, 0)
            if isinstance(self.carte.get(pos), Creature):
                self.carte.get(pos).meet(self.carte._hero)
                if self.carte.get(pos).hp <= 0:
                    self.carte.get(pos).game_state = "Death"
                   # self.anim_mat[(pos.x,pos.y)] = [self.anim_mat[(pos.x,pos.y)],self.carte.get(pos)]
                    del self.carte._elem[self.carte.get(pos)]

    def foreground(self):
        for i in self.anim_mat:
            if len(self.anim_mat[i]) != 1:
                self.checking(
                    self.anim_mat[i][1], self.anim_mat[i][0], self.anim_mat[i][1])
                
    def ui(self):
        pygame.mouse.set_visible(False)
        cursorsp = pygame.image.load('test gui/GUI/Mouse pointer/Mpointer.png')
        cursor_rect = cursorsp.get_rect()
        a,b = pygame.mouse.get_pos()[0]-32,pygame.mouse.get_pos()[1]
        cursor_rect.center = (a,b)
        self.screen.blit(cursorsp,cursor_rect)

    def background(self):
        # self.screen.set_colorkey([128,0,128]) # don't copy color [0,0,0] on screen
        imgsize = 64
        basex = self.screencoords[0]/2 - 288
        x, y = basex, self.screencoords[1]/4
        self.startingaxis = Coord(x,y)
        finishingx = 0
        for k in self.carte.fogOfWar():
            for i in k:
                if i == Map.empty:
                    pass
                elif type(i) != str:
                    self.checking(i, x, y)
                else:
                        
                    if i in Map.walllist:
                        img = self.pictures[i]
                        img = pygame.transform.scale(img, (64, 64))
                        self.screen.blit(img, (x, y))
                    else:
                        img = self.pictures["sol"]
                        img = pygame.transform.scale(img, (64, 64))
                        self.screen.blit(img, (x, y))
                x += imgsize
            finishingx = x
            x = basex
            y += imgsize
        self.finishingaxis = Coord(finishingx,y)

    def checking(self, i, x, y):
        from Chest import Chest
        img = self.pictures["sol"]
        img = pygame.transform.scale(img, (64, 64))
        self.screen.blit(img, (x, y))

        if i.name in self.pictures and i.name != "Hero":
            self.screen.blit(self.pictures[i.name], (x, y))
        elif i.name == "Hero":
            direc = (pygame.mouse.get_pos()[0] < self.screencoords[0]/2)
            im = self.anim_lib.anim_hero(i.game_state)
            img, i.game_state = im[0], im[1]
            img = pygame.transform.scale(img, (64, 64))
            img = pygame.transform.flip(img, direc, 0)
            self.screen.blit(img, (x, y))

        elif i.name == "Bat":
            img, act = self.anim_lib.anim_bat(
                i.game_state)[0], self.anim_lib.anim_bat(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
        elif i.name == "Goblin":
            img, act = self.anim_lib.anim_goblin(
                i.game_state)[0], self.anim_lib.anim_goblin(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
        elif isinstance(i, Chest):
            img = self.pictures["chest"]
            img = pygame.transform.scale(img, (64, 64))
            self.screen.blit(img, (x, y))

        else:
            self.screen.blit(self.pictures["imgnotdefined"], (x, y))

    def inventory_ui(self):
        x, y = self.screencoords[0]/2, self.screencoords[1]/8
        im = self.pictures["invplaceholder"]
        im = pygame.transform.scale(im, (64, 64))
        basex = x
        a = -1
        sacado = self.carte._hero._inventory
        imgsize = 64
        for i in range(2):
            for k in range(3):
                self.screen.blit(im,(x,y))
                a+=1
                if len(sacado)>a:
                    img = self.pictures[sacado[a].name]
                    img = pygame.transform.scale(img, (64, 64))
                    self.screen.blit(img, (x, y))
                x+=imgsize
            x = basex
            y+=imgsize
        self.weapon_ui(basex,y)
        
    def weapon_ui(self,x,y):
        im2 = self.pictures["invweapon"]
        im2 = pygame.transform.scale(im2, (64, 64))
        img = self.pictures[self.carte._hero.weapon.name]
        img = pygame.transform.scale(img, (64, 64))
        self.screen.blit(im2,(x+32*4,y))
        self.screen.blit(img,(x+32*4,y))
        
    def health_bar(self):
        x, y = self.screencoords[0]/8, self.screencoords[1]/4
        BarreVie1 = pygame.Rect(x, y, 108, 105)
        BarreVie2 = pygame.Rect(x, y, 108, 105*(self.carte._hero.max_hp-self.carte._hero.hp)/self.carte._hero.max_hp)
        pygame.draw.rect(self.screen, (255, 0, 0), BarreVie1)
        pygame.draw.rect(self.screen, (0, 0, 0), BarreVie2)
        
        self.screen.blit(pygame.transform.scale(self.pictures["orb1"], (115, 54)), (x, y+55))
        self.screen.blit(pygame.transform.scale(self.pictures["orb3"], (110, 110)), (x, y))
        self.screen.blit(pygame.transform.scale(self.pictures["orb5"], (110, 110)), (x, y))
        self.screen.blit(pygame.transform.scale(self.pictures["orb6"], (110, 110)), (x, y))
        
    def mana_bar(self):
        #im = self.pictures["manaplaceholder"]
        x,y = self.screencoords[0]/3,self.screencoords[1]/5
        im = self.pictures["manabg"]
        self.screen.blit(im,(self.screencoords[0]/3,self.screencoords[1]/5))

        im = Image.open('Blue_bar.png')
        im = im.crop((0,0,128 - 128*((self.carte._hero.max_mana-self.carte._hero.mana)/self.carte._hero.max_mana),128))
        im.save("testmana.png")
        im = pygame.image.load("testmana.png")
        self.screen.blit(im,(self.screencoords[0]/3,self.screencoords[1]/5))
        
    def exp_bar(self):
        from utiles import theGame
        a = self.carte._hero.level
        b = 0
        for i in theGame().level_bonus:
            if b==a:
                currentrequiredxp = i
            b+=1
        x,y = self.screencoords[0]/3,self.screencoords[1]/6
        im = self.pictures["manabg"]
        self.screen.blit(im,(self.screencoords[0]/3,self.screencoords[1]/6))
        
        im = Image.open('Green_bar.png')
        if (self.carte._hero.xp/currentrequiredxp)*128<1:
            g = 1
        else:
            g = (self.carte._hero.xp/currentrequiredxp)*128
        im = im.crop((0,0,g,128))
        im.save("testxp.png")
        img = pygame.image.load("testxp.png")
        self.screen.blit(img,(self.screencoords[0]/3,self.screencoords[1]/6))
        
    def chat(self, ms):
        self.screen.blit(self.font.render(
            (str(ms)), 1, [255, 255, 255]),  (0, 0))
        pygame.display.update()

    def action(self, pressed):
        # print(pressed)
        from utiles import theGame
        if 27 in pressed:
            pygame.quit()
            self.carte._hero.hp = 0

        if 122 in pressed and pressed[122]:
            theGame()._actions["z"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[122] = False

        if 113 in pressed and pressed[113]:
            theGame()._actions["q"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[113] = False

        if 115 in pressed and pressed[115]:
            theGame()._actions["s"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[115] = False

        if 100 in pressed and pressed[100]:
            theGame()._actions["d"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[100] = False
        if 98 in pressed and pressed[98]:
            theGame()._actions["b"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[98] = False
        if 110 in pressed and pressed[110]:
            theGame()._actions["n"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[110] = False

        if "click" in pressed and pressed["click"] != False:
            self.carte._hero.game_state = "Attack"
            pressed["click"] = False

        if 117 in pressed and pressed[117]:
            theGame()._actions["u"](self.carte._hero)
            pressed[117] = False
            
        if 97 in pressed and pressed[97]:
            theGame()._actions["a"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[97] = False

        if mainloop.inv:
            sacado = self.carte._hero._inventory
            for i in range(len(sacado)):
                if 49+i in pressed and pressed[49+i]:
                    self.carte._hero.use(sacado[i])
                    pressed[49+i] = False