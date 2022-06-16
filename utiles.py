
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
    """
    teleports the creature to a random empty coordinate
    :param creature: Creature instance
    """
    print("-> In teleport")
    loc = random.choices(theGame()._floor._rooms)[
        0].randEmptyCoord(theGame()._floor)
    theGame().addMessage("The hero is now at "+str(loc))
    theGame()._floor.rm(theGame()._floor.pos(creature))
    theGame()._floor.put(loc, creature)


def cheat_hp(hero):
    """gives the hero a lot of hp to make testing easier"""
    print("CHEATING hp")
    hero.max_hp = 100000
    hero.hp = 100000


def cheat_str(hero):
    """gives the hero a lot of strength to make testing easier"""
    print("CHEATING strength")
    hero._strength = 1000

def cheat_mana(hero):
    """not sure if it is used somewhere"""
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