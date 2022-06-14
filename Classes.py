import pygame
from time import *
    
        
class anim_total:
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
        
        self.state_anim_time = time()
        
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
            img = pygame.image.load("Hero.sprites/"+str(state)+str(walkingpos)+"/"+str(imgact)+".png")
            if walkingpos == "W":
                img = pygame.transform.flip(img, 1, 0)
        else:
            img = pygame.image.load("Hero.sprites/"+str(state)+"/"+str(imgact)+".png")
            
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
        return pygame.image.load("Bat.sprites/"+str(state)+"/"+str(imgact)+".png"),self.bat_action
    
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
        return pygame.image.load("Goblin.sprites/"+str(state)+"/"+str(imgact)+".png"),self.goblin_action
    
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
            
        return pygame.image.load("Orc.sprites/"+str(state)+"/"+str(imgact)+".png"),self.orc_action

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
        return pygame.image.load("snake.sprites/"+str(state)+"/"+str(imgact)+".png"),self.snake_action
    
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
        return pygame.image.load("Blob.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Blob_action
    
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
        return pygame.image.load("Stone_Minotaur.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Stone_Minotaur_action
    
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
        return pygame.image.load("Rat.sprites/"+str(state)+"/"+str(imgact)+".png"),self.Rat_action
    
    def anim_state(self):
        imgact = int((time()-self.state_anim_time)*100)
        print(imgact)
        if imgact > 63:
            self.state_anim_time = time()
            imgact = 0
        return pygame.image.load("Particles/Purple/"+str(imgact)+".png")
        
        