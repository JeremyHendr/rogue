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
#En clair, theGame().templist t'associes les cases de la map montrée à leur coordonnées
#Et dans Map, il y a self.currentFoGMap qui te donne toutes les cases montrées
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
        self.touches = ""

    def animation(self):  # la boucle principale qui reprint tout
        pygame.display.init()
        tc = self.touches
        self.screen = pygame.display.set_mode(self.screencoords)
        #self.screen.blit(self.bg1test, (0, 0))
        # self.chat(ms)
        self.background()
        self.foreground()
        self.action(tc.pressed)
        self.inventory_ui()
        self.health_bar()
        self.mana_bar()
        self.exp_bar()
        self.ui()
        pygame.display.update()
        
    def deathanimation(self):
        t = time()
        while time()-t<=1:
            pygame.display.init()
            self.screen = pygame.display.set_mode(self.screencoords)
            self.background()
            self.health_bar()
            self.mana_bar()
            self.exp_bar()
            self.ui()
        
    def realtime(self):
        from utiles import theGame
        from Bullet import Bullet
        timer = self.timers[0]
        if time()-timer >= 0.7:
            self.timers[0] = time()
            self.carte.moveAllMonsters()
            for monster in self.carte._elem:
                if isinstance(monster, Creature):
                    monster.updateState()


        if self.carte._hero.game_state == "Attack" and time()-self.timers[1] > 1.05:
            self.timers[1] = time()
            if self.carte._hero.weapon.isrange:
                bl = theGame()._hero.weapon.bullet
                hpos = theGame()._floor.pos(theGame()._hero)
                dest = Coord(pygame.mouse.get_pos()[0]-16,pygame.mouse.get_pos()[1]-16).toSpecialCoord()
                # print("adding bullet to list",hpos,theGame()._hero,dest,bl.speed,bl.damage,bl.armor_pene,bl.damage_type)
                theGame().bullet_list.append(Bullet(hpos,theGame()._hero,dest,bl.speed,bl.damage,bl.armor_pene,bl.damage_type))
                # print("last bl added:",theGame().bullet_list[-1].__dict__)
                # print(theGame().templist[0])
            else:
                direc = (pygame.mouse.get_pos()[0] > self.screencoords[0]/2)
                if not direc:
                    direc = -1
                pos = self.carte.pos(self.carte._hero) + Coord(direc, 0)
                if isinstance(self.carte.get(pos), Creature):
                    self.carte.get(pos).meet(self.carte._hero)

    def foreground(self):
        from utiles import theGame
        from SpecialCoord import SpecialCoord
        for bullet in theGame().bullet_list:
            bullet.updatePos()
            # print(bullet)
            for couple in theGame().templist:
                if couple[0] == Coord(int(bullet.pos.x), int(bullet.pos.y)):
                    c = SpecialCoord(couple[1].x, couple[1].y, bullet.pos.decx, bullet.pos.decy)
                    x = int(c.x + c.decx)
                    y = int(c.y + c.decy)
                    # print("couple", c, x, y) # couple, c,
                    BarreVie1 = pygame.Rect(x, y, 20, 20)
                    pygame.draw.rect(self.screen, (255, 0, 0), BarreVie1)

                    #self.screen.blit(self.pictures["stick"], (x, y))
                    break


    def ui(self):
        pygame.mouse.set_visible(False)
        cursorsp = pygame.image.load('test gui/GUI/Mouse pointer/Mpointer.png')
        cursor_rect = cursorsp.get_rect()
        a,b = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
        cursor_rect.center = (a,b)
        self.screen.blit(cursorsp,cursor_rect)
        pygame.display.update()

    def background(self):
        from utiles import theGame
        # self.screen.set_colorkey([128,0,128]) # don't copy color [0,0,0] on screen
        imgsize = 64
        basex = self.screencoords[0]/2 - 288
        x, y = basex, self.screencoords[1]/4
        theGame().templist = []
        self.startingaxis = Coord(x,y)
        finishingx = 0
        a = -1
        for k in self.carte.fogOfWar():
            for i in k:
                a+=1
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
                c = self.carte.currentFoGMap[a]
                x += imgsize
                theGame().templist.append((Coord(c[1],c[0]),Coord(x,y)))

            finishingx = x
            x = basex
            y += imgsize
        self.finishingaxis = Coord(finishingx,y)

    def checking(self, i, x, y):
        from Chest import Chest
        img = self.pictures["sol"]
        img = pygame.transform.scale(img, (64, 64))
        self.screen.blit(img, (x, y))
        # print("pct",self.pictures)
        if i.name in self.pictures and i.name != "Hero":
            self.screen.blit(self.pictures[i.name], (x, y))
        elif i.name == "Hero":
            im = self.anim_lib.anim_hero(i.game_state,i.walkingcoord)
            img, i.game_state = im[0], im[1]
            img = pygame.transform.scale(img, (64, 64))
            if i.game_state != "Walking":
                direc = (pygame.mouse.get_pos()[0] < self.screencoords[0]/2)
                img = pygame.transform.flip(img, direc, 0)
            self.screen.blit(img, (x, y))

        elif i.name == "Bat":
            img, act = self.anim_lib.anim_bat(
                i.game_state)[0], self.anim_lib.anim_bat(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
        elif i.name == "Goblin":
            img, act = self.anim_lib.anim_goblin(
                i.game_state)[0], self.anim_lib.anim_goblin(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "Ork":
            img, act = self.anim_lib.anim_orc(
                i.game_state)[0], self.anim_lib.anim_orc(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "Snake":
            img, act = self.anim_lib.anim_snake(
                i.game_state)[0], self.anim_lib.anim_snake(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "Blob":
            img, act = self.anim_lib.anim_Blob(
                i.game_state)[0], self.anim_lib.anim_Blob(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "Stone Minotaur":
            img, act = self.anim_lib.anim_Stone_Minotaur(
                i.game_state)[0], self.anim_lib.anim_Stone_Minotaur(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "Rat":
            img, act = self.anim_lib.anim_Rat(
                i.game_state)[0], self.anim_lib.anim_Rat(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif isinstance(i, Chest):
            img = self.pictures["chest"]
            img = pygame.transform.scale(img, (64, 64))
            self.screen.blit(img, (x, y))

        else:
            self.screen.blit(self.pictures["imgnotdefined"], (x, y))
        if isinstance(i,Creature) or isinstance(i,Hero):
            for st in i.state:
                # print(st)
                if st == "poisoned":
                    im = self.anim_lib.anim_state()
                    im = pygame.transform.scale(im, (64, 64))
                    self.screen.blit(im,(x,y))

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
        
    def chestselect(self,l):
        self.background()
        font=pygame.font.SysFont("sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner", 30)
        while True:
            x, y = self.screencoords[0]/2-210, self.screencoords[1]/2-300
            a = -1
            imgsize = 64
            hitbox = []
            img1 = self.pictures["chestpresentation1"]
            img1 = pygame.transform.scale(img1, (420, 600))
            self.screen.blit(img1,(x,y))
            x, y = self.screencoords[0]/2-64, self.screencoords[1]/2
            text=font.render("Un coffre! Il contient: ",1,[255,255,255])
            self.screen.blit(text,  (x-80,y-200))
            basex = x
            
            for i in range(2):
                for k in range(3):
                    a+=1
                    if len(l)>a:
                        hitbox.append(Coord(x,y))
                        img = self.pictures[l[a].name]
                        img = pygame.transform.scale(img, (64, 64))
                        self.screen.blit(img, (x, y))
                    x+=imgsize
                x = basex
                y+=imgsize
            self.ui()
        
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._hero.sethp(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position_souris = event.pos
                    a = 0
                    for i in hitbox:
                        if position_souris[0]>=i.x and position_souris[0]<i.x+imgsize and position_souris[1]>=i.y and position_souris[1]<i.y+imgsize:
                            return l[a]
                        else:
                            a+=1
    
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
        if self.carte._hero.mana == 0:
            return None
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
#        print(self.carte._hero.wkcd)
#        if time() - self.carte._hero.wkcd >= 0.2:
#            self.carte._hero.wkcd = time()

        if 122 in pressed and pressed[122]:
            self.carte._hero.walkingcoord = "N"
            self.anim_lib.hero_anim_time = time()
            theGame()._actions["z"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[122] = False

        if 113 in pressed and pressed[113]:
            self.carte._hero.walkingcoord = "W"
            self.anim_lib.hero_anim_time = time()
            theGame()._actions["q"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[113] = False

        if 115 in pressed and pressed[115]:
            self.carte._hero.walkingcoord = "S"
            self.anim_lib.hero_anim_time = time()
            theGame()._actions["s"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[115] = False

        if 100 in pressed and pressed[100]:
            self.carte._hero.walkingcoord = "E"
            self.anim_lib.hero_anim_time = time()
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

        # if 117 in pressed and pressed[117]:
        #     theGame()._actions["u"](self.carte._hero)
        #     pressed[117] = False
            
        if 97 in pressed and pressed[97]:
            theGame()._actions["a"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[97] = False

        if 101 in pressed and pressed[101]:
            theGame()._actions["e"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[101] = False

        if 114 in pressed and pressed[114]:
            theGame()._actions["r"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[114] = False

        if mainloop.inv:
            sacado = self.carte._hero._inventory
            for i in range(len(sacado)):
                if 49+i in pressed and pressed[49+i]:
                    self.carte._hero.use(sacado[i])
                    pressed[49+i] = False