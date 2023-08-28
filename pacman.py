import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

        # Dictionaries for behaviors
        self.isChasing = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.isCutoff1 = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.isCutoff2 = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.isCutoff3 = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.lastPowerUp = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.guardPowerUp = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.fruitSpawned = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        self.guardFruit = {BLINKY : False, PINKY : False, INKY : False, CLYDE : False}
        

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        if key_pressed[K_w]:
            return UP
        if key_pressed[K_s]:
            return DOWN
        if key_pressed[K_a]:
            return LEFT
        if key_pressed[K_d]:
            return RIGHT
        return STOP  

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    def diagnostics(self):
            # Define the mapping of numbers to names
        name_mapping = {4: "BLINKY", 5: "PINKY", 6: "INKY", 7: "CLYDE"}

        # List of all dictionaries with their names
        dicts = [("isChasing", self.isChasing), ("isCutoff1", self.isCutoff1), ("isCutoff2", self.isCutoff2), ("isCutoff3", self.isCutoff3), ("lastPowerUp", self.lastPowerUp), 
                ("guardPowerUp", self.guardPowerUp), ("fruitSpawned", self.fruitSpawned), ("guardFruit", self.guardFruit)]

        # Determine the maximum width required for each column
        max_width = max(len(name) for name in name_mapping.values()) + len(": True") + 2  # Account for ": True" or ": False" and some padding

        # Print dictionary names in a single line with added padding to the left
        for dict_name, _ in dicts:
            print(f"{dict_name:<15}", end='')  # Use 15 spaces to ensure proper alignment of dictionary names
        print()  # Move to the next line

        # Print each row of values underneath their respective dictionary names
        for key in name_mapping:
            for _, d in dicts:
                # Calculate the string representation of the key-value pair
                kv_str = f"{name_mapping[key]}: {d[key]}"
                # Calculate the padding needed to reach the desired distance of 15 spaces
                padding = 15 - len(kv_str)
                print(f"{kv_str}", end=' ' * padding)
            print()  # Move to the next line
        print()