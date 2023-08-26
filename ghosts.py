import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites


class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        # self.goal = self.pacman.position
        self.goal = Behaviors.selector(self)

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection         

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)

    # def setup_behavior_tree(self):
    #     root = Selector(name='High Level Ordering of Strategies')
    #     chase_behavior = Action(Ghost.chase)
    #     scatter_behavior = Action(Ghost.scatter)
    #     root.child_nodes = [scatter_behavior, chase_behavior]
    #     logging.info('\n' + root.tree_to_string())
    #     return root


class Behaviors(Ghost):
    # Helper function to check if any ghost is chasing
    def checkIsChasing(ghost):
        for key, value in ghost.pacman.isChasing.items():
            if value == True:
                if key == ghost.name:
                    return False
                return True
        return False
    
    # Helper function to check if any ghost is cutting off
    def checkIsCutoff(ghost):
        for key, value in ghost.pacman.isCutoff.items():
            if value == True:
                if key == ghost.name:
                    return False
                return True
        return False
    
    def checkIfLastPowerUp(ghost):
        print("ppp: ", ppp)
        if len(ppp) == 1:
            for key, value in ghost.pacman.lastPowerUp.items():
                if value == True:
                    if key == ghost.name:
                        return True
                    else:
                        return False
            return True
        else:
            return False

    def resetGhostChase(ghost):
        pacman = ghost.pacman
        pacman.isChasing[ghost.name] = False
        pacman.isCutoff[ghost.name] = False
        pacman.lastPowerUp[ghost.name] = False
        pacman.guardPowerUp[ghost.name] = False
        pacman.fruitSpawned[ghost.name] = False
        pacman.guardFruit[ghost.name] = False

    def selector(ghost):
        
        #used to calculate distance if needed in behaviors
        d = ghost.pacman.position - ghost.position
        ds = d.magnitudeSquared()
        numTiles = 8
        # if ds <= (TILEWIDTH * numTiles)**2:
        #this is saying if the ghost is less than or equal to numtiles away from pacman
        
        
        
        # groupOne = False
        # parterOne = None
        # parterTwo = None
        #
        # if not groupTwo:
        #   if partnerOne == None:
        #       partnerOne = self.GHOST
        #       continue
        #   else if partnerTwo == None:
        #       partnerTwo = self.GHOST
        #       continue
        #   else if partnerThree == None:
        #       partnerTwo = self.GHOST
        #   else if partnerFour == None:
        #       partnerTwo = self.GHOST
        #

        # if ds <= (TILEWIDTH * numTiles)**2:

        # Checks if any ghost is chasing pacman
        if not Behaviors.checkIsChasing(ghost): # If no ghost is chasing then chase
            Behaviors.resetGhostChase(ghost)            # Resets ghost in all chasing dicts
            ghost.pacman.isChasing[ghost.name] = True
            return Behaviors.defaultChase(ghost)
        
        # if ds <= (TILEWIDTH * numTiles*1.5)**2:
        
        # Checks if any ghost is cutting off pacman
        elif not Behaviors.checkIsCutoff(ghost):    # If no ghost is cutting off pacman then cutoff
            Behaviors.resetGhostChase(ghost)
            ghost.pacman.isCutoff[ghost.name] = True
            return Behaviors.cutoff(ghost)
        
        # Checks if there is one power up left, and if there is someone already targeting it
        elif Behaviors.checkIfLastPowerUp(ghost):   # If no ghost is going to last powerup then go there
            Behaviors.resetGhostChase(ghost)
            ghost.pacman.lastPowerUp[ghost.name] = True
            return Behaviors.guardPower(ghost)

        
        # Defaults to chasing pacman
        else:
            Behaviors.resetGhostChase(ghost)
            ghost.pacman.isChasing[ghost.name] = True
            return Behaviors.defaultChase(ghost)
    
        # else if fruitSpawned:
        #   distance = fruit.pos - ghost.pos
        #   if distance <= 5:
        #       if not guardFruit:
        #           self.guardFruit()
        #           guardFruit = True
        #       else:
        #           continue
        #
        # else if lastPowerUp:
        #   if not guardPowerUp:
        #       guardPowerUp = True
        #       self.guardPower()
        #   else:
        #       continute
        #
        #
        #
        # else:
        #   self.defaultChase()


    def defaultChase(ghost):
        return ghost.pacman.position

    def cutoff(ghost):

        return ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 4
    
    def reverseCutOff(ghost):
        return ghost.pacman.position - ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 4

    def guardFruit(ghost):
        # return self.fruit.position * 1
        pass

    def guardPower(ghost):
        pos = Vector2(ppp[0][1]*TILEWIDTH, ppp[0][0]*TILEHEIGHT)    # (y, x) i have no clue why but this works\
        print("Guarding pos: ", pos)
        
        return pos
        
        

    def groupUp(ghost):
        pass





class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)

class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    # def chase(self):
    #     self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
    
class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    # def chase(self):
    #     vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
    #     vec2 = (vec1 - self.blinky.position) * 2
    #     self.goal = self.blinky.position + vec2

class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    # def chase(self):
    #     d = self.pacman.position - self.position
    #     ds = d.magnitudeSquared()
    #     if ds <= (TILEWIDTH * 8)**2:
    #         self.scatter()
    #     else:
    #         self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
    


class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):   # dt = delta time, amount of time that has passed since last use 
        flag = True
        for ghost in self:
            if flag:
                ghost.pacman.diagnostics()
                flag = False
            ghost.update(dt)


    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

def difficultySave(diff):
    global difficulty
    difficulty = diff

def powerPelletPositions(list):
    global ppp # Power Pellet Positions = [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
    ppp = list

def powerPelletRemove(pelletPos):
    ppp.remove(pelletPos)