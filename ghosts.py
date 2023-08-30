import pygame
import random
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
    def checkIsCutoff1(ghost):
        for key, value in ghost.pacman.isCutoff1.items():
            if value == True:
                if key == ghost.name:
                    return False
                return True
        return False
    
    def checkIsCutoff2(ghost):
        for key, value in ghost.pacman.isCutoff2.items():
            if value == True:
                if key == ghost.name:
                    return False
                return True
        return False
    
    def checkIsCutoff3(ghost):
        for key, value in ghost.pacman.isCutoff3.items():
            if value == True:
                if key == ghost.name:
                    return False
                return True
        return False
    
    def checkIfLastPowerUp(ghost):
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
        
    def checkIfFruitSpawned(ghost):
        if fruitNinja != None:
            for key, value in ghost.pacman.fruitSpawned.items():
                if value == True:
                    if key == ghost.name:
                        return True
                    else:
                        return False
            return True
        else:
            return False

    def checkIfGuardingPowerUp(ghost):
        for key, value in ghost.pacman.guardPowerUp.items():
            if value == True:
                if key == ghost.name:
                    return False
                return True
        return False

    def resetGhostChase(ghost):
        pacman = ghost.pacman
        pacman.isChasing[ghost.name] = False
        pacman.isCutoff1[ghost.name] = False
        pacman.isCutoff2[ghost.name] = False
        pacman.isCutoff3[ghost.name] = False
        pacman.lastPowerUp[ghost.name] = False
        pacman.guardPowerUp[ghost.name] = False
        pacman.fruitSpawned[ghost.name] = False
        pacman.guardFruit[ghost.name] = False
    
    def Medium_Attack(ghost):
        # Various attack behaviors
        if not Behaviors.checkIsChasing(ghost): # Chase
            Behaviors.resetGhostChase(ghost)            
            ghost.pacman.isChasing[ghost.name] = True
            return Behaviors.defaultChase(ghost)
        
        elif not Behaviors.checkIsCutoff1(ghost): # Cutoff Close Distance
            Behaviors.resetGhostChase(ghost)            
            ghost.pacman.isCutoff1[ghost.name] = True
            return Behaviors.cutoff1(ghost)
        
        elif not Behaviors.checkIsCutoff2(ghost): # Cutoff Medium Distance
            Behaviors.resetGhostChase(ghost)           
            ghost.pacman.isCutoff2[ghost.name] = True
            return Behaviors.cutoff2(ghost)
        
        elif not Behaviors.checkIsCutoff3(ghost): # Cutoff Large Distance
            Behaviors.resetGhostChase(ghost)            
            ghost.pacman.isCutoff3[ghost.name] = True
            return Behaviors.cutoff3(ghost)
        
        else:
            Behaviors.resetGhostChase(ghost) # Default Chase
            ghost.pacman.isChasing[ghost.name] = True
            return Behaviors.defaultChase(ghost)
        

    def selector(ghost):
        # Arbitrary range for distance calculation
        numTiles = 24

        # Behaviors for easy difficulty
        if difficulty == "easy":

            # Blinky Behavior
            if ghost.name == BLINKY:
                d = ghost.pacman.position - Vector2(0, 0) # Calculating distance of pacman to Blinky's path
                ds = d.magnitudeSquared()
                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Blinky's path, chase
                    return Behaviors.defaultChase(ghost) 
                else: # If not, continue following path
                    return Vector2(0, 0)
            
            # Pinky Behavior
            if ghost.name == PINKY:
                d = ghost.pacman.position - Vector2(TILEWIDTH*NCOLS, 0) # Calculating distance of pacman to Pinky's path
                ds = d.magnitudeSquared()
                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Pinky's path, chase
                    return Behaviors.defaultChase(ghost)
                else: # If not, continue following path
                    return Vector2(TILEWIDTH*NCOLS, 0)
            
            # Inky Behavior
            if ghost.name == INKY:
                d = ghost.pacman.position - Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS) # Calculating distance of pacman to Inky's path
                ds = d.magnitudeSquared()
                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Inky's path, chase
                    return Behaviors.defaultChase(ghost)
                else: # If not, continue following path
                    return Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)
            
            # Clyde Behavior
            if ghost.name == CLYDE:
                d = ghost.pacman.position - Vector2(0, TILEHEIGHT*NROWS) # Calculating distance of pacman to Clyde's path
                ds = d.magnitudeSquared()
                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Clyde's path, chase
                    return Behaviors.defaultChase(ghost)
                else: # If not, continue following path
                    return Vector2(0, TILEHEIGHT*NROWS)
        
        
        # Behaviors for medium difficulty
        if difficulty == "medium":
            numTiles = 30 # Increase range of attack

            # Blinky Behavior
            if ghost.name == BLINKY:
                d = ghost.pacman.position - Vector2(0, 0) # Calculating distance of pacman to Blinky's path
                ds = d.magnitudeSquared()

                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Blinky's path, attack
                    return Behaviors.Medium_Attack(ghost)
                else:
                    Behaviors.resetGhostChase(ghost)
                    return Vector2(0, 0)
 
            # Pinky Behavior           
            if ghost.name == PINKY:
                d = ghost.pacman.position - Vector2(TILEWIDTH*NCOLS, 0) # Calculating distance of pacman to Pinky's path
                ds = d.magnitudeSquared()

                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Pinky's path, attack
                    return Behaviors.Medium_Attack(ghost)
                else:
                    Behaviors.resetGhostChase(ghost)
                    return Vector2(TILEWIDTH*NCOLS, 0)
            
            # Inky Behavior  
            if ghost.name == INKY: 
                d = ghost.pacman.position - Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS) # Calculating distance of pacman to Inky's path
                ds = d.magnitudeSquared()

                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Inky's path, attack
                    return Behaviors.Medium_Attack(ghost)
                else:
                    Behaviors.resetGhostChase(ghost)
                    return Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)
            
            # Clyde Behavior  
            if ghost.name == CLYDE:
                d = ghost.pacman.position - Vector2(0, TILEHEIGHT*NROWS) # Calculating distance of pacman to Clyde's path
                ds = d.magnitudeSquared()
                if ds <= (TILEWIDTH * numTiles)**2: # If pacman is within range of Clyde's path, attack
                    return Behaviors.Medium_Attack(ghost)
                else:
                    Behaviors.resetGhostChase(ghost)
                    return Vector2(0, TILEHEIGHT*NROWS)
                
        if difficulty == "hard":
            # If pacman gets too close to fruit or powerUp, cut pacman off
            if ghost.pacman.fruitSpawned[ghost.name] or ghost.pacman.guardPowerUp[ghost.name]:
                pos = Vector2(ppp[0][1]*TILEWIDTH, ppp[0][0]*TILEHEIGHT)
                d = ghost.pacman.position - pos
                ds = d.magnitudeSquared()
                if ds <= (TILEWIDTH * 8)**2:
                    return Behaviors.cutoff1(ghost)
                           
            # Checks if any ghost is chasing pacman
            if not Behaviors.checkIsChasing(ghost): # If no ghost is chasing then chase
                Behaviors.resetGhostChase(ghost)            # Resets ghost in all chasing dicts
                ghost.pacman.isChasing[ghost.name] = True
                print("chase", ghost.pacman.position) 
                return Behaviors.defaultChase(ghost)
            
            # Checks if any ghost is cutting off pacman
            elif not Behaviors.checkIsCutoff1(ghost):    # If no ghost is cutting off pacman then cutoff
                Behaviors.resetGhostChase(ghost)
                ghost.pacman.isCutoff1[ghost.name] = True
                print("cuttoff1", ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 4) 
                return Behaviors.cutoff1(ghost)
            
            # Checks if any ghost is cutting off pacman
            elif not Behaviors.checkIsCutoff2(ghost):    # If no ghost is cutting off pacman then cutoff
                Behaviors.resetGhostChase(ghost)
                ghost.pacman.isCutoff2[ghost.name] = True
                print("cuttoff2", ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 8) 
                return Behaviors.cutoff2(ghost)
            
            # Checks if there is one power up left, and if there is someone already targeting it
            elif Behaviors.checkIfLastPowerUp(ghost):
                Behaviors.resetGhostChase(ghost)
                ghost.pacman.lastPowerUp[ghost.name] = True
                ghost.pacman.guardPowerUp[ghost.name] = True
                return Behaviors.guardPower(ghost)
            
            # Checks if fruit has spawned and if someone is chasing it
            elif Behaviors.checkIfFruitSpawned(ghost):
                Behaviors.resetGhostChase(ghost)
                ghost.pacman.fruitSpawned[ghost.name] = True
                return Behaviors.guardFruit(ghost)
            
            elif not Behaviors.checkIsCutoff3(ghost):    # If no ghost is cutting off pacman then cutoff
                Behaviors.resetGhostChase(ghost)
                ghost.pacman.isCutoff3[ghost.name] = True
                print("cuttoff3", ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 12) 
                return Behaviors.cutoff3(ghost)

            # Defaults to chasing pacman
            else:
                Behaviors.resetGhostChase(ghost)
                ghost.pacman.isChasing[ghost.name] = True
                return Behaviors.defaultChase(ghost)
    

    def defaultChase(ghost):
        return ghost.pacman.position

    # Cutoff close distance
    def cutoff1(ghost):
        return ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 2
    
    # Cutoff medium distance
    def cutoff2(ghost):
        return ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 4

    # Cutoff large distance
    def cutoff3(ghost):
        return ghost.pacman.position + ghost.pacman.directions[ghost.pacman.direction] * TILEWIDTH * 6
    
    # Scatters to the fruit
    def guardFruit(ghost):
        return fruitNinja.position

    # Scatters to the last powerup
    def guardPower(ghost):
        pos = Vector2(ppp[0][1]*TILEWIDTH, ppp[0][0]*TILEHEIGHT)  
        return pos
        





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
        # d = self.pacman.position - self.position
        # ds = d.magnitudeSquared()
        # if ds <= (TILEWIDTH * 8)**2:
        #     self.scatter()
        # else:
        #     self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
    


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

def fruitNode(fruitVar):
    global fruitNinja
    fruitNinja = fruitVar

def powerPelletRemove(pelletPos):
    ppp.remove(pelletPos)