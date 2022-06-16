import pygame
from time import *

class anim_total:
    used to animate the game
    def __init__(self):
        self.hero_anim_nb = 10
        self.hero_anim_wk = 8
        self.hero_anim_time,self.hero_anim_val = time() , "Idle"


        
        self.bat_last_state = "Idle"
        self.bat_action = "Live"
        self.bat_anim_nb1 = 30
        self.bat_anim_nb2_3 = 10
        self.bat_anim_time = time()
        
        self.goblin_last_state = "Idle"
        self.goblin_action = "Live"
        self.goblin_anim_nb1 = 20
        self.goblin_anim_nb2_3 = 10
        self.goblin_anim_time = time()
        
        self.orc_last_state = "Idle"
        self.orc_action = "Live"
        self.orc_anim_nb1 = 20
        self.orc_anim_nb2_3_4 = 10
        self.orc_anim_time = time()
        
        self.snake_last_state = "Idle"
        self.snake_action = "Live"
        self.snake_anim_nb1 = 20
        self.snake_anim_nb2_3 = 10
        self.snake_anim_time = time()
        
        self.Blob_last_state = "Idle"
        self.Blob_action = "Live"
        self.Blob_anim_nb1 = 20
        self.Blob_anim_nb2_3 = 10
        self.Blob_anim_time = time()
        
        self.Stone_Minotaur_last_state = "Idle"
        self.Stone_Minotaur_action = "Live"
        self.Stone_Minotaur_anim_nb1 = 20
        self.Stone_Minotaur_anim_nb2_3 = 10
        self.Stone_Minotaur_anim_time = time()
        
        self.Rat_last_state = "Idle"
        self.Rat_action = "Live"
        self.Rat_anim_nb1 = 20
        self.Rat_anim_nb2_3 = 10
        self.Rat_anim_time = time()
        
        self.Statue_last_state = "Idle"
        self.Statue_action = "Live"
        self.Statue_anim_nb1 = 4
        self.Statue_anim_nb2 = 6
        self.Statue_anim_nb3 = 5
        self.Statue_anim_nb4 = 6
        self.Statue_anim_time = time()
        
        self.TA_last_state = "Idle"
        self.TA_action = "Live"
        self.TA_anim_nb1 = 2
        self.TA_anim_nb2 = 9
        self.TA_anim_nb3 = 6
        self.TA_anim_nb4 = 6
        self.TA_anim_time = time()
        
        
        self.healing_anim_time = time()
        self.poisoned_anim_time = time()
        self.burning_anim_time = time()
        self.decaying_anim_time = time()
        self.decay = 0
        self.healing= 0
        
        
    def anim_hero(self,state,walkingpos):
        imgact = int((time()-self.hero_anim_time)*10)
        
        if self.hero_anim_val != state:
            imgact = 0
            self.hero_anim_time = time()
            self.hero_anim_val = state
            
        if imgact>=self.hero_anim_nb and state!="Walking":
            self.hero_anim_time = time()
            imgact = 0
            if state != "Idle":
                state = "Idle"
        elif imgact>=self.hero_anim_wk-1 and state == "Walking":
            self.hero_anim_time = time()
            imgact = 0
            if state != "Idle":
                state = "Idle"
        
        if state == "Walking":
            img = pygame.image.load("Assets/Hero.sprites/"+str(state)+str(walkingpos)+"/"+str(imgact)+".png")
            if walkingpos == "W":
                img = pygame.transform.flip(img, 1, 0)
        elif state!="Walking":
            img = pygame.image.load("Assets/Hero.sprites/"+str(state)+"/"+str(imgact)+".png")
            
        if state == "Attack":
            if walkingpos == "S" or walkingpos =="N":
                img = pygame.image.load("Assets/Hero.sprites/Attack/"+str(state)+walkingpos+".png")
        return img,state


    
  
    def anim_bat(self,state):
        imgact = int((time()-self.bat_anim_time)*10)
        if state != self.bat_last_state:
            self.bat_last_state = state
            self.bat_action = "Live"
            self.bat_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.bat_anim_nb2_3-1)):
            self.bat_anim_time = time()
            self.bat_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.bat_anim_nb2_3-1)):
            self.bat_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.bat_anim_nb1-1:
            self.bat_anim_time = time()
            self.bat_action = "Live"
            imgact = 0
        return pygame.image.load("Assets/Bat.sprites/"+str(state)+"/"+str(imgact)+".png"),self.bat_action
    
    def anim_goblin(self,state):
        imgact = int((time()-self.goblin_anim_time)*10)
        if state != self.goblin_last_state:
            self.goblin_last_state = state
            self.goblin_action = "Live"
            self.goblin_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.goblin_anim_nb2_3-1)):
            self.goblin_anim_time = time()
            self.goblin_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.goblin_anim_nb2_3-1)):
            self.goblin_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.goblin_anim_nb1-1:
            self.goblin_anim_time = time()
            self.goblin_action = "Live"
            imgact = 0
        return pygame.image.load("Assets/Goblin.sprites/"+str(state)+"/"+str(imgact)+".png"),self.goblin_action
    
    def anim_orc(self,state):
        imgact = int((time()-self.orc_anim_time)*10)
        if state != self.orc_last_state:
            self.orc_last_state = state
            self.orc_action = "Live"
            self.orc_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.orc_anim_nb2_3_4-1)):
            self.orc_anim_time = time()
            self.orc_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.orc_anim_nb2_3_4-1)):
            self.orc_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.orc_anim_nb1-1:
            self.orc_anim_time = time()
            self.orc_action = "Live"
            imgact = 0
            
        return pygame.image.load("Assets/Orc.sprites/"+str(state)+"/"+str(imgact)+".png"),self.orc_action

    def anim_snake(self,state):
        imgact = int((time()-self.snake_anim_time)*10)
        if state != self.snake_last_state:
            self.snake_last_state = state
            self.snake_action = "Live"
            self.snake_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.snake_anim_nb2_3-1)):
            self.snake_anim_time = time()
            self.snake_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.snake_anim_nb2_3-1)):
            self.snake_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.snake_anim_nb1-1:
            self.snake_anim_time = time()
            self.snake_action = "Live"
            imgact = 0
        return pygame.image.load("Assets/snake.sprites/"+str(state)+"/"+str(imgact)+".png"),self.snake_action
    
    def anim_Blob(self,state):
        imgact = int((time()-self.Blob_anim_time)*10)
        if state != self.Blob_last_state:
            self.Blob_last_state = state
            self.Blob_action = "Live"
            self.Blob_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.Blob_anim_nb2_3-1)):
            self.Blob_anim_time = time()
            self.Blob_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.Blob_anim_nb2_3-1)):
            self.Blob_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.Blob_anim_nb1-1:
            self.Blob_anim_time = time()
            self.Blob_action = "Live"
            imgact = 0
        return pygame.image.load("Assets/Blob.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Blob_action
    
    def anim_Stone_Minotaur(self,state):
        imgact = int((time()-self.Stone_Minotaur_anim_time)*10)
        if state != self.Stone_Minotaur_last_state:
            self.Stone_Minotaur_last_state = state
            self.Stone_Minotaur_action = "Live"
            self.Stone_Minotaur_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.Stone_Minotaur_anim_nb2_3-1)):
            self.Stone_Minotaur_anim_time = time()
            self.Stone_Minotaur_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.Stone_Minotaur_anim_nb2_3-1)):
            self.Stone_Minotaur_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.Stone_Minotaur_anim_nb1-1:
            self.Stone_Minotaur_anim_time = time()
            self.Stone_Minotaur_action = "Live"
            imgact = 0
        return pygame.image.load("Assets/Stone_Minotaur.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Stone_Minotaur_action
    
    def anim_Rat(self,state):
        imgact = int((time()-self.Rat_anim_time)*10)
        if state != self.Rat_last_state:
            self.Rat_last_state = state
            self.Rat_action = "Live"
            self.Rat_anim_time = time()
            imgact = 0
            
        elif state == "Death"  and (imgact >= (self.Rat_anim_nb2_3-1)):
            self.Rat_anim_time = time()
            self.Rat_action = "Kill"
            imgact = 0
        elif state !="Death" and state !="Idle" and (imgact >= (self.Rat_anim_nb2_3-1)):
            self.Rat_anim_time = time()
            imgact = 0
            
        elif (state == "Idle" or state=="Walking")  and imgact>=self.Rat_anim_nb1-1:
            self.Rat_anim_time = time()
            self.Rat_action = "Live"
            imgact = 0
        return pygame.image.load("Assets/Rat.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Rat_action
    
    def anim_Statue(self,state):
        imgact = int((time()-self.Statue_anim_time)*10)
        if state != self.Statue_last_state:
            self.Statue_last_state = state
            self.Statue_action = "Live"
            self.Statue_anim_time = time()
            imgact = 0
        elif state == "Death"  and (imgact >= (self.Statue_anim_nb4-1)):
            self.Statue_anim_time = time()
            self.Statue_action = "Kill"
            imgact = 0
        elif (state =="Idle" and (imgact >= (self.Statue_anim_nb1-1))) or  (state =="Walking" and (imgact >= (self.Statue_anim_nb2-1))):
            self.Statue_anim_time = time()
            imgact = 0
            
        elif state=="Attack"  and imgact>=self.Statue_anim_nb3-1:
            self.Statue_anim_time = time()
            imgact = 0
        return pygame.image.load("Assets/Statue.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Statue_action
    
    def anim_TA(self,state):
        imgact = int((time()-self.TA_anim_time)*10)
        if state != self.TA_last_state:
            self.TA_last_state = state
            self.TA_action = "Live"
            self.TA_anim_time = time()
            imgact = 0
        elif state == "Death"  and (imgact >= (self.TA_anim_nb4-1)):
            self.TA_anim_time = time()
            self.TA_action = "Kill"
            imgact = 0
        elif state =="Idle" and (imgact >= (self.TA_anim_nb1-1)):
            self.TA_anim_time = time()
            imgact = 0
        elif state=="Walking"  and imgact>=self.TA_anim_nb2-1:
            self.TA_anim_time = time()
            imgact = 0
        elif state=="Attack"  and imgact>=self.TA_anim_nb3-1:
            self.TA_anim_time = time()
            imgact = 0
        return pygame.image.load("Assets/The_Abomination.sprites/"+str(state)+"/"+str(imgact)+".png"),self.TA_action
    
    
    
    
    def anim_state(self,order):
        if order == "poisoned":
            imgact = int((time()-self.poisoned_anim_time)*100)
            if imgact > 63:
                self.poisoned_anim_time = time()
                imgact = 0
            return pygame.image.load("Assets/Particles/Purple/"+str(imgact)+".png"),None
        
        elif order =="burning":
            imgact = int((time()-self.burning_anim_time)*125)
            if imgact > 73:
                self.burning_anim_time = time()
                imgact = 0
            return pygame.image.load("Assets/Particles/Fire/"+str(imgact)+".png"),None
        
        elif order =="decaying":
            if self.decay == 0:
                self.decaying_anim_time = time()
                self.decay = 1
            imgact = int((time()-self.decaying_anim_time)*20)
            stop = False
            if imgact > 23:
                self.decaying_anim_time = time()
                imgact = 0
                stop = True
                self.decay = 0
            return pygame.image.load("Assets/Particles/Doom/"+str(imgact)+".png"),stop
        
        elif order =="healing":
            if self.healing == 0:
                self.healing_anim_time = time()
                self.healing = 1
            imgact = int((time()-self.healing_anim_time)*5)
            stop = False
            if imgact > 5:
                self.healing_anim_time = time()
                imgact = 0
                stop = True
                self.healing = 0
            return [pygame.image.load("Assets/Particles/Heal/"+str(imgact)+".png"),stop]
        
        