
from Game import Game
import random
from Hero import Hero
from mainloop import mainloop
def heal(creature, hp):
    print("-> In heal")
    creature.hp += hp
    if isinstance(creature, Hero) and creature.hp > creature.max_hp:
        creature.hp = creature.max_hp
    return True


def teleport(creature):
    print("-> In teleport")
    loc = random.choices(theGame()._floor._rooms)[
        0].randEmptyCoord(theGame()._floor)
    theGame().addMessage("The hero is now at "+str(loc))
    theGame()._floor.rm(theGame()._floor.pos(creature))
    theGame()._floor.put(loc, creature)


def cheat_hp(hero):
    print("CHEATING hp")
    hero.max_hp = 100000
    hero.hp = 100000


def cheat_str(hero):
    print("CHEATING strength")
    hero._strength = 1000

def cheat_mana(hero):
    print("removing mana and adding exp")
    hero.mana -=3
    hero.xp+=1000

def tempfunct():
    if mainloop.inv:
        mainloop.inv = False
    else:
        mainloop.inv = True
def theGame(game = Game()):
    return game