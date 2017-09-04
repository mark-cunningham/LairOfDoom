# Lair of Doom
# Code Angel

# Classes: Level, Block, LedgeBlock, WaterBlock, DiamondBlock, ExitDoor, DoomMonster

import pygame
import lair_of_doom

BLOCK_SIZE = 16
DOOM_MONSTER_MOVE = 2
DOOM_RIGHT = 1

# Initialise lists
ledges = []
water = []
diamonds = []
exit_doors = []
doom_monsters = []


# The Level class
class Level:

    def __init__(self):
        self.level_number = 1
        self.player_start_loc = None

    # delete the ledge, water, diamonds and doom_monster lists
    def set_up(self):
        del ledges[:]
        del water[:]
        del diamonds[:]
        del exit_doors[:]
        del doom_monsters[:]

        if self.level_number == 1:
            LedgeBlock([0, 29], 35)
            LedgeBlock([6, 26], 4)
            LedgeBlock([12, 22], 6)
            LedgeBlock([7, 18], 4)
            LedgeBlock([14, 15], 13)
            LedgeBlock([29, 21], 8)
            LedgeBlock([36, 16], 4)
            LedgeBlock([38, 12], 2)
            LedgeBlock([32, 8], 4)
            LedgeBlock([20, 8], 8)
            LedgeBlock([6, 8], 10)
            LedgeBlock([0, 5], 4)

            WaterBlock([35, 29], 5)

            DoomMonster(20, 28, 34)

            Diamond([16, 21])
            Diamond([29, 20])
            Diamond([39, 15])
            Diamond([24, 7])

            ExitDoor([0, 4])

            self.player_start_loc = [1, 28]

        elif self.level_number == 2:
            LedgeBlock([0, 26], 22)
            LedgeBlock([25, 29], 8)
            LedgeBlock([36, 29], 4)
            LedgeBlock([39, 24], 1)
            LedgeBlock([37, 19], 1)
            LedgeBlock([32, 14], 3)
            LedgeBlock([6, 17], 22)
            LedgeBlock([3, 13], 4)
            LedgeBlock([0, 9], 3)
            LedgeBlock([10, 10], 8)
            LedgeBlock([22, 9], 6)
            LedgeBlock([32, 7], 4)
            LedgeBlock([37, 5], 3)

            WaterBlock([0, 29], 25)
            WaterBlock([33, 29], 3)

            Diamond([27, 28])
            Diamond([19, 16])
            Diamond([4, 12])
            Diamond([19, 16])
            Diamond([24, 8])
            Diamond([35, 6])

            DoomMonster(8, 25, 19)
            DoomMonster(6, 16, 14)
            DoomMonster(22, 16, 27)
            DoomMonster(10, 9, 17)

            ExitDoor([39, 4])
            ExitDoor([0, 8])

            self.player_start_loc = [1, 25]

        elif self.level_number == 3:
            LedgeBlock([0, 26], 5)
            LedgeBlock([8, 26], 5)
            LedgeBlock([16, 26], 10)
            LedgeBlock([29, 26], 10)
            LedgeBlock([32, 22], 5)
            LedgeBlock([32, 21], 4)
            LedgeBlock([32, 20], 3)
            LedgeBlock([32, 19], 2)
            LedgeBlock([32, 18], 1)
            LedgeBlock([21, 18], 8)
            LedgeBlock([2, 18], 16)
            LedgeBlock([4, 13], 3)
            LedgeBlock([10, 11], 26)
            LedgeBlock([14, 10], 2)
            LedgeBlock([20, 10], 2)
            LedgeBlock([27, 10], 2)
            LedgeBlock([33, 10], 2)
            LedgeBlock([36, 6], 4)
            LedgeBlock([14, 3], 18)
            LedgeBlock([12, 4], 2)
            LedgeBlock([10, 5], 2)
            LedgeBlock([7, 6], 3)
            LedgeBlock([0, 7], 8)
            LedgeBlock([1, 6], 2)

            WaterBlock([0, 29], 40)
            WaterBlock([16, 10], 4)
            WaterBlock([29, 10], 4)
            WaterBlock([3, 6], 4)

            DoomMonster(17, 25, 24)
            DoomMonster(3, 17, 8)
            DoomMonster(12, 17, 16)
            DoomMonster(20, 2, 28)

            Diamond([10, 25])
            Diamond([16, 25])
            Diamond([25, 25])
            Diamond([36, 21])
            Diamond([35, 20])
            Diamond([34, 19])
            Diamond([33, 18])
            Diamond([32, 17])
            Diamond([10, 17])
            Diamond([24, 10])
            Diamond([16, 2])
            Diamond([11, 4])
            Diamond([39, 5])

            ExitDoor([0, 6])

            self.player_start_loc = [1, 25]

    def level_up(self):
        self.level_number += 1


# The block class - any solid line of blocks
class Block:
    def __init__(self, start_location, block_length):
        # The number of individual blocks in the full block
        self.block_length = block_length

        # Start x block
        x_coord = start_location[0] * BLOCK_SIZE

        # Start y block
        y_coord = start_location[1] * BLOCK_SIZE

        # The full block
        self.rect = pygame.Rect(x_coord, y_coord, block_length * BLOCK_SIZE, BLOCK_SIZE)


# Ledge class inherits from the Block class
class LedgeBlock(Block):
    def __init__(self, start_location, block_length):
        self.image = lair_of_doom.load_media('image', 'ledge')
        Block.__init__(self, start_location, block_length)
        ledges.append(self)


# Water class inherits from the Block class
class WaterBlock(Block):
    def __init__(self, start_location, block_length):
        self.image = lair_of_doom.load_media('image', 'water')
        Block.__init__(self, start_location, block_length)
        water.append(self)


# Diamond class inherits from the Block class (only 1 block long)
class Diamond(Block):
    def __init__(self, start_location):
        self.image = lair_of_doom.load_media('image', 'diamond')
        Block.__init__(self, start_location, 1)
        diamonds.append(self)


# Exit Door class inherits from the Block class (only 1 block long)
class ExitDoor(Block):
    def __init__(self, start_location):
        self.image = lair_of_doom.load_media('image', 'exit')
        Block.__init__(self, start_location, 1)
        exit_doors.append(self)


# Doom monster class
class DoomMonster:

    # Initialise each doom monster with a starting location, and also the point where it will change direction
    def __init__(self, start_x, start_y, end_x):
        self.image = lair_of_doom.load_media('image', 'doom_monster')
        self.start_x_coord = start_x * BLOCK_SIZE
        self.start_y_coord = start_y * BLOCK_SIZE
        self.end_x_coord = end_x * BLOCK_SIZE
        self.monster_move = DOOM_MONSTER_MOVE

        self.direction = DOOM_RIGHT
        self.x = self.start_x_coord
        self.y = self.start_y_coord

        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

        doom_monsters.append(self)

    # Move the doom monster horizontally by dx pixels
    def move(self):
        self.x += self.monster_move * self.direction

        # If the monster goes beyond its start or end location, change direction
        if self.x < self.start_x_coord or self.x > self.end_x_coord:
            # Direction is either 1 or -1
            # By multiplying direction by -1, it will be the negative of itself
            self.direction *= -1

        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)


