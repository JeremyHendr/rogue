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
    #font = pygame.font.SysFont("Arial", 30)
    def __init__(self, carte): #constructeur de mainloop
        mainloop.carte = carte
        self.nb_fps = 30
        self.nbtimers = 3  # on aura besoin de bcp de timers
        self.timers = [time() for i in range(self.nbtimers)]
        self.screencoords = (pygame.display.Info().current_w,
                             pygame.display.Info().current_h) #la taille de l'écran
        self.imgsetter = images()
        self.pictures = self.imgsetter.img
        self.anim_lib = anim_total()
        self.anim_mat = {}
        self.startingaxis = None
        self.finishingaxis = None
        self.touches = ""
        
    def deathanimation(self):
        """display when the hero dies"""
        t = time()
        while time()-t<=1:
            pygame.display.init()
            self.screen = pygame.display.set_mode(self.screencoords)
            self.background()
            self.health_bar()
            self.mana_bar()
            self.exp_bar()
            self.mouseui()
        
    def realtime(self):
        #fonction gérant la partie 'temps réel' du jeu, i-e les mouvements des monstres, le mouvement des projectiles et l'attaque du héros 
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
                mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                hx,hy = self.screencoords[0]/2,self.screencoords[1]/2
                if mx>hx-64 and mx<hx+64:
                    if my<hy:
                        dire = Coord(0,-1)
                    else:
                        dire = Coord(0,1)
                else:
                    if mx>hx:
                        dire = Coord(1,0)
                    else:
                        dire = Coord(-1,0)
                    
                pos = self.carte.pos(self.carte._hero) + dire
                print(pos)
                print(self.carte.pos(self.carte._hero))
                self.carte._hero.attackdir = None
                if isinstance(self.carte.get(pos), Creature):
                    self.carte.get(pos).meet(self.carte._hero)

    def foreground(self):
        """displays the bullets for the range weapons"""
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
                    BarreVie1 = pygame.Rect(x, y, 15, 15)
                    pygame.draw.rect(self.screen, (0, 0, 0), BarreVie1)

                    #self.screen.blit(self.pictures["stick"], (x, y))
                    break
    def backgroundui(self): 
        #La fonction appelant quasiment toutes les méthodes de mainloop
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.screencoords)
        tc = self.touches
        sx,sy = self.screencoords[0],self.screencoords[1]
        mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
        img = self.pictures["gamebg"]
        img = pygame.transform.scale(img, (sx, sy))
        self.screen.blit(img, (0, 0))
        #self.screen.blit(self.bg1test, (0, 0))
        # self.chat(ms)
        self.background()
        self.foreground()
        self.action(tc.pressed)
        self.inventory_ui()

        self.spell_ui()

        self.health_bar()
        self.mana_bar()
        self.exp_bar()
        self.minimap_ui()
        self.mouseui()

    def mouseui(self): #remplace le curseur basique par un plus fantaisiste
        pygame.mouse.set_visible(False)
        cursorsp = pygame.image.load('Assets/Mpointer.png')
        cursor_rect = cursorsp.get_rect()
        a,b = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
        cursor_rect.center = (a,b)
        self.screen.blit(cursorsp,cursor_rect)
        pygame.display.update()
    
    
    def minimap_ui(self): #affiche une minimap dans le coin haut gauche de l'écran
        """displays the minimap"""
        basex = 50
        x, y = basex, self.screencoords[1]/8
        img = self.pictures["minimap"]
        img = pygame.transform.scale(img, (270, 190))
        self.screen.blit(img, (x, y))
        pixelsize = 4
        basex += 100
        x = basex
        y += 50
        a = -1
        for k in self.carte._mat:
            for i in k:
                a+=1
                if isinstance(i,Hero):
                    pixel = pygame.Rect(x, y, pixelsize, pixelsize)
                    pygame.draw.rect(self.screen, (0, 0, 255), pixel)
                # elif  i == Map.empty or type(i) != str or i == Map.ground:
                #     pixel = pygame.Rect(x, y, pixelsize, pixelsize)
                #     pygame.draw.rect(self.screen, (0, 0, 0), pixel)
                
                else:
                    if i in Map.walllist:
                        pixel = pygame.Rect(x, y, pixelsize, pixelsize)
                        pygame.draw.rect(self.screen, (255, 255, 255), pixel)
                x += pixelsize
            x = basex
            y += pixelsize
            
        
    def background(self):#affiche la partie actuelle (au milieu de l'écran)
        from utiles import theGame
        # self.screen.set_colorkey([128,0,128]) # don't copy color [0,0,0] on screen
        imgsize = 64
        basex = self.screencoords[0]/2 - 288
        x, y = basex, self.screencoords[1]/4-96
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
                theGame().templist.append((Coord(c[1], c[0]), Coord(x, y)))
                x += imgsize


            finishingx = x
            x = basex
            y += imgsize
        self.finishingaxis = Coord(finishingx,y)

    def checking(self, i, x, y): #méthode d'aide à background, lui affiche l'image associée à la créature envoyée
        """verifying and adjusting all the monster animations"""
        from Chest import Chest
        img = self.pictures["sol"]
        img = pygame.transform.scale(img, (64, 64))
        self.screen.blit(img, (x, y))
        creaturetohero_pos = (self.carte.pos(i).x < self.carte.pos(self.carte._hero).x)
        if i.name in self.pictures and i.name != "Hero":
            self.screen.blit(self.pictures[i.name], (x, y))
        elif i.name == "Hero":
            # if i.attackdir == None:
            
            # else:
            # im = self.pictures["Attack" + str(i.attackdir)]
            if i.game_state == "Attack":
                mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                hx,hy = self.screencoords[0]/2,self.screencoords[1]/2
                
                if mx>hx-64 and mx<hx+64:
                    if time()-self.timers[2]>1:
                            self.timers[2] = time()
                    if time()-self.timers[2]>0.5:
                        i.game_state = "Idle"
                    if my<hy:
                        i.attackdir = "N"
                    else:
                        i.attackdir = "S"
                    im = self.anim_lib.anim_hero(i.game_state,i.attackdir) 
                    img, i.game_state = im[0], im[1]
                    
                else:
                    direc = (pygame.mouse.get_pos()[0] < self.screencoords[0]/2)
                    if self.carte._hero.weapon.isrange:
                        im = self.pictures["AttackR"]
                        img = pygame.transform.flip(im, direc, 0)
                    else:
                        i.attackdir = None
                        im = self.anim_lib.anim_hero(i.game_state,None)
                        img, i.game_state = im[0], im[1]
                        img = pygame.transform.flip(img, direc, 0)
            else:
                im = self.anim_lib.anim_hero(i.game_state,i.walkingcoord)
                img, i.game_state = im[0], im[1]
            img = pygame.transform.scale(img, (64, 64))
            self.screen.blit(img, (x, y))
            
            

        elif i.name == "Bat":
            img, act = self.anim_lib.anim_bat(
                i.game_state)[0], self.anim_lib.anim_bat(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                img = pygame.transform.flip(img, creaturetohero_pos, 0)
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
                img = pygame.transform.flip(img, not creaturetohero_pos, 0)
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
                img = pygame.transform.flip(img, not creaturetohero_pos, 0)
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
                img = pygame.transform.flip(img, creaturetohero_pos, 0)
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
                img = pygame.transform.flip(img, creaturetohero_pos, 0)
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
                img = pygame.transform.flip(img, creaturetohero_pos, 0)
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
                img = pygame.transform.flip(img, creaturetohero_pos, 0)
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "Statue":
            img, act = self.anim_lib.anim_Statue(
                i.game_state)[0], self.anim_lib.anim_Statue(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                img = pygame.transform.flip(img, not creaturetohero_pos, 0)
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif i.name == "The_Abomination":
            img, act = self.anim_lib.anim_TA(
                i.game_state)[0], self.anim_lib.anim_TA(i.game_state)[1]
            if act == "Live":
                img = pygame.transform.scale(img, (64, 64))
                img = pygame.transform.flip(img, not creaturetohero_pos, 0)
                self.screen.blit(img, (x, y))
            else:
                # print("killed?")
                self.carte._elem[i] = ""
                self.carte.rm(self.carte.pos(i))
                
        elif isinstance(i, Chest):
            img = self.pictures["chest"]
            img = pygame.transform.scale(img, (64, 64))
            self.screen.blit(img, (x, y))


        if isinstance(i,Creature) or isinstance(i,Hero): #affiche les effets spéciaux (poison,gel,soin,decay)
            dellist = []
            for st in i.state:
                # print(st)
                if st == "frozen":
                    im = self.pictures["frozen"]
                    im = pygame.transform.scale(im, (64, 64))
                    self.screen.blit(im,(x,y))
                else:
                    im = self.anim_lib.anim_state(st)
                    img = im[0]
                    img = pygame.transform.scale(img, (64, 64))
                    self.screen.blit(img,(x,y))
                    if im[1]:
                        dellist.append(st)
            for victim in dellist:
                del i.state[victim]
                    


    def inventory_ui(self): #affiche l'inventaire et ce qui va avec
        """displays the inventory"""
        x, y = self.screencoords[0]-264, self.screencoords[1]*(1/3)
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
        
    def spell_ui(self): #affiche les sorts
        x, y = self.screencoords[0]-312, self.screencoords[1]*(2/3)
        font=pygame.font.SysFont("sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner", 30)
        
        im = self.pictures["Impending_Terror"]
        im = pygame.transform.scale(im, (64, 64))
        self.screen.blit(im, (x, y))
        text=font.render("E",1,[255,255,255])
        self.screen.blit(text,  (x+32,y+72))
        
        x+=88
        im = self.pictures["Jolt_of_light"]
        im = pygame.transform.scale(im, (64, 64))
        self.screen.blit(im, (x, y))
        text=font.render("A",1,[255,255,255])
        self.screen.blit(text,  (x+32,y+72))
        
        x+=88
        im = self.pictures["Request_from_the_fire_God"]
        im = pygame.transform.scale(im, (64, 64))
        self.screen.blit(im, (x, y))
        text=font.render("R",1,[255,255,255])
        self.screen.blit(text,  (x+32,y+72))
        
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

    def chestselect(self,l): #popup quand on ouvre un coffre
        """displays the popup window when the hero opens a chest"""
        from utiles import theGame
        font=pygame.font.SysFont("sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner", 30)
        while True:
            self.screen = pygame.display.set_mode(self.screencoords)
            self.background()
            x, y = self.screencoords[0]/2-210, self.screencoords[1]/2-300
            a = -1
            imgsize = 64
            hitbox = []
            img1 = self.pictures["chestpresentation1"]
            img1 = pygame.transform.scale(img1, (420, 600))
            self.screen.blit(img1,(x,y))
            x, y = self.screencoords[0]/2-64, self.screencoords[1]/2
            if len(l) == 1:
                text = font.render("Un coffre! Il contient: ", 1, [255, 255, 255])
                self.screen.blit(text, (x - 80, y - 200))
            else:
                text = font.render("Un marchand "+"Les prix sont: ", 1, [255, 255, 255])
                self.screen.blit(text, (x - 80, y - 200))
                text = font.render(" ".join([x.name + ": " + str(self.price(x)) for x in l]), 1, [255, 255, 255])
                self.screen.blit(text, (x - 80, y - 180))
                text = font.render("tu as: "+str(theGame()._hero.gold)+" or", 1, [255, 255, 255])
                self.screen.blit(text, (x - 80, y - 160))
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
            self.mouseui()
        
                
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
        """displays the equiped weapon,armor,droporuse slot"""
        im2 = self.pictures["invweapon"]
        im2 = pygame.transform.scale(im2, (64, 64))
        img = self.pictures[self.carte._hero.weapon.name]
        img = pygame.transform.scale(img, (64, 64))
        self.screen.blit(im2,(x+32*4,y))
        self.screen.blit(img,(x+32*4,y))
        im2 = self.pictures["invarmor"]
        im2 = pygame.transform.scale(im2, (64, 64))
        img = self.pictures[self.carte._hero.protection.name]
        img = pygame.transform.scale(img, (64, 64))
        self.screen.blit(im2,(x+32*2,y))
        self.screen.blit(img,(x+32*2,y))
        im2 = self.pictures["invonoff"]
        im2 = pygame.transform.scale(im2, (64, 64))
        self.screen.blit(im2,(x,y))
        if mainloop.inv:
            font=pygame.font.SysFont("sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner", 30)
            text=font.render("Use",1,[255,255,255])
            self.screen.blit(text,  (x+5,y+32))
        else:
            font=pygame.font.SysFont("sitkasmallsitkatextsitkasubheadingsitkaheadingsitkadisplaysitkabanner", 30)
            text=font.render("Drop",1,[255,255,255])
            self.screen.blit(text,  (x+5,y+32))
        text=font.render("Y",1,[255,255,255])
        self.screen.blit(text,  (x+25,y+64))
        
        
        
        
    def health_bar(self):
        """displays the health bar"""
        x, y = self.screencoords[0]-200, self.screencoords[1]/6
        BarreVie1 = pygame.Rect(x, y, 108, 105)
        BarreVie2 = pygame.Rect(x, y, 108, 105*(self.carte._hero.max_hp-self.carte._hero.hp)/self.carte._hero.max_hp)
        pygame.draw.rect(self.screen, (255, 0, 0), BarreVie1)
        pygame.draw.rect(self.screen, (0, 0, 0), BarreVie2)
        
        self.screen.blit(pygame.transform.scale(self.pictures["orb1"], (115, 54)), (x, y+55))
        self.screen.blit(pygame.transform.scale(self.pictures["orb3"], (110, 110)), (x, y))
        self.screen.blit(pygame.transform.scale(self.pictures["orb5"], (110, 110)), (x, y))
        self.screen.blit(pygame.transform.scale(self.pictures["orb6"], (110, 110)), (x, y))
        
    def mana_bar(self):
        """displays the mana bar"""
        #im = self.pictures["manaplaceholder"]
        x,y = self.screencoords[0]-328,self.screencoords[1]/6
        im = self.pictures["manabg"]
        self.screen.blit(im,(x,y))
        if self.carte._hero.mana == 0:
            return None
        im = Image.open('Assets/Blue_bar.png')
        im = im.crop((0,0,128 - 128*((self.carte._hero.max_mana-self.carte._hero.mana)/self.carte._hero.max_mana),128))
        im.save("currentmana.png")
        im = pygame.image.load("currentmana.png")
        self.screen.blit(im,(x,y))
        
    def exp_bar(self):
        """displays the experience bar"""
        from utiles import theGame
        a = self.carte._hero.level
        b = 0
        for i in theGame().level_bonus:
            if b==a:
                currentrequiredxp = i
            b+=1
        x,y = self.screencoords[0]-328,self.screencoords[1]/8
        im = self.pictures["manabg"]
        self.screen.blit(im,(x,y))
        
        im = Image.open('Assets/Green_bar.png')
        if (self.carte._hero.xp/currentrequiredxp)*128<1:
            g = 1
        else:
            g = (self.carte._hero.xp/currentrequiredxp)*128
        im = im.crop((0,0,g,128))
        im.save("currentxp.png")
        img = pygame.image.load("currentxp.png")
        self.screen.blit(img,(x,y))
    

    def action(self, pressed):
        """looking for the events happening on the keyboard and the mouse"""
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
            
        if 121 in pressed and pressed[121]:
            theGame()._actions["y"](self.carte._hero)
            # self.carte.moveAllMonsters()
            pressed[121] = False


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


        sacado = self.carte._hero._inventory
        todelist = []
        for i in range(len(sacado)):
            if 49+i in pressed and pressed[49+i]:
                if mainloop.inv:
                    self.carte._hero.use(sacado[i])
                else:
                    todelist.append(self.carte._hero._inventory[i])
                pressed[49+i] = False
        for i in todelist:
            if i in self.carte._hero._inventory:
                self.carte._hero._inventory.pop(self.carte._hero._inventory.index(i))
def intervert():
        mainloop.inv = not mainloop.inv