import pygame
from time import *
from images import images

from Hero import Hero
def MenuZero():
    """displays the Home/start page"""
    pygame.display.init()
    pictures = images().img
    sx,sy = pygame.display.Info().current_w , pygame.display.Info().current_h
    while True:
        pygame.display.init()
        screen = pygame.display.set_mode((sx,sy))
        
        mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
        img = pictures["TitleScreen"]
        img = pygame.transform.scale(img, (sx, sy))
        screen.blit(img, (0, 0))
        
        imgsizex = 320
        imgsizey = 60
        
        x = sx/2 - imgsizex/2
        yng = sy/2 - imgsizey
        yo = yng + imgsizey
        yc = yo + imgsizey
        ye = yc + imgsizey
        basenb = 1
        clickablenb = 3
        ng,o,c,e = basenb,basenb,basenb,basenb
        if mx>x and mx<x+imgsizex:
            if my>yng and my<yo:
                ng = clickablenb
            elif my> yo and my<yc:
                o = clickablenb
            elif my > yc and my < ye:
                c = clickablenb
            elif my > ye and my < ye + imgsizey:
                e = clickablenb
        l = ["ng","o","c","e"]
        li = [ng,o,c,e]
        for i in range(4):
            im = pygame.image.load("Assets/UI/"+l[i]+"_"+str(li[i])+".png")
            screen.blit(im,(x,yng + imgsizey*i))
            
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx,my = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
                    if mx>x and mx<x+imgsizex:
                        if my>yng and my<yo:
                            from utiles import theGame
                            theGame()._hero = Hero()
                            return None
                        elif my> yo and my<yc:
                            print("Not Yet Implemented")
                        elif my > yc and my < ye:
                            print("Not Yet Implemented")
                        elif my > ye and my < ye + imgsizey:
                            pygame.quit() 
        mouseui(screen)
        pygame.display.update()
        
def mouseui(screen):
    pygame.mouse.set_visible(False)
    cursorsp = pygame.image.load('Assets/Mpointer.png')
    cursor_rect = cursorsp.get_rect()
    a,b = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
    cursor_rect.center = (a,b)
    screen.blit(cursorsp,cursor_rect)

        


            
        