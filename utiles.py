
from Game import Game
import random
def heal(creature,hp):
    from Hero import Hero
    print("-> In heal")
    creature.hp += hp
    if isinstance(creature,Hero) and creature.hp > creature.max_hp:
        creature.hp = creature.max_hp
    return True

def teleport(creature):
    print("-> In teleport")
    loc = random.choices(theGame()._floor._rooms)[0].randEmptyCoord(theGame()._floor)
    theGame().addMessage("The hero is now at "+str(loc))
    theGame()._floor.rm(theGame()._floor.pos(creature))
    theGame()._floor.put(loc,creature)

def cheat_hp(hero):
    print("CHEATING hp")
    hero.max_hp = 100000
    hero.hp = 100000

def cheat_str(hero):
    print("CHEATING strength")
    hero._strength = 1000

def levelUp():
    theGame()._level
    theGame().buildFloor()

def getch():
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')

def theGame(game = Game()):
    return game