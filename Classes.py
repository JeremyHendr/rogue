import pygame
from time import *
    
        
class anim_total:
    def __init__(self):
        self.hero_anim_nb = 10
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
        
    def anim_hero(self,state):
        imgact = int((time()-self.hero_anim_time)*10)
        if self.hero_anim_val != state:
            imgact = 0
            self.hero_anim_time = time()
            self.hero_anim_val = state
        if imgact>=self.hero_anim_nb-1:
            self.hero_anim_time = time()
            imgact = 0
            if state != "Idle":
                state = "Idle"
        return pygame.image.load("Hero.sprites/"+str(state)+"/"+str(imgact)+".png"),state
  
    def anim_bat(self,state):
        imgact = int((time()-self.bat_anim_time)*10)
        if state != self.bat_last_state:
            self.bat_last_state = state
            self.bat_action = "Live"
            self.bat_anim_time = time()
            imgact = 0
            
        elif (state != "Idle" and state!="Walking") and (imgact >= (self.bat_anim_nb2_3-1)):
            self.bat_anim_time = time()
            self.bat_action = "Kill"
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
        
        
        
        