#!/usr/bin/python
# Lair of Doom
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

# Define the colours
WHITE = (255, 255, 255)
DARK_RED = (70, 24, 0)
YELLOW = (255, 206, 0)

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

V_SCOREBOARD_MARGIN = 2
H_SCOREBOARD_MARGIN = 4
SCOREBOARD_HEIGHT = 24

MESSAGEBOX_HEIGHT = SCREEN_HEIGHT / 4
MESSAGEBOX_TOP = (SCREEN_HEIGHT - MESSAGEBOX_HEIGHT) / 2
MESSAGEBOX_MARGIN = SCREEN_WIDTH / 8
MESSAGEBOX_TEXT_MARGIN = 16

GRAVITY = 0.6
BLOCK_SIZE = 16
MOVEMENT_SPACE = 5
JUMP_VELOCITY = 10

DOOM_MONSTER_MOVE = 2
DOOM_RIGHT = 1


# Player class
class Player:

    def __init__(self):
        self.velocity = 0
        self.jumping = False
        self.jumping_left = False
        self.jumping_right = False
        self.diamonds_collected = 0
        self.game_over = False
        self.game_completed = False
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)

    # set the player location at the start of the game
    def set_location(self, location):
        x_coord = location[0] * BLOCK_SIZE
        y_coord = location[1] * BLOCK_SIZE
        self.rect = pygame.Rect(x_coord, y_coord, BLOCK_SIZE, BLOCK_SIZE)

    # Move the player
    def move(self, dx, dy):

        # Move the player dx pixels horizontally, dy pixels vertically
        self.rect.x += dx
        self.rect.y += dy

        # Keep the player from going off left and right edges of the screen
        if self.rect.x >= SCREEN_WIDTH - BLOCK_SIZE:
            self.rect.x = SCREEN_WIDTH - BLOCK_SIZE
        if self.rect.x <= 0:
            self.rect.x = 0

        # Check if the moving player has hit a ledge
        for ledge in ledges:
            if self.rect.colliderect(ledge.rect):

                # player moving right hits the left edge of a ledge, so don't move any further
                if dx > 0:
                    self.rect.right = ledge.rect.left

                # player moving left  hits the right edge of a ledge, so don't move any further
                if dx < 0:
                    self.rect.left = ledge.rect.right

                # player falling lands on a ledge, so stop falling down
                if dy > 0:
                    self.rect.bottom = ledge.rect.top
                    self.jumping = False
                    self.jumping_left = False
                    self.jumping_right = False
                    self.velocity = 0

                # player jumping hits the bottom of a ledge so stop going up and start falling
                if dy < 0:
                    self.rect.top = ledge.rect.bottom
                    self.velocity = 0

        # Check there is a ledge directly below the player. If so, ledge_below should be True
        self.rect.y += MOVEMENT_SPACE
        ledge_below = False
        for ledge in ledges:
            if self.rect.colliderect(ledge.rect):
                ledge_below = True

        self.rect.y -= MOVEMENT_SPACE

        # If there is no ledge below start falling
        if ledge_below is False:
            self.jumping = True

    # The player starts a jump
    def start_jump(self, direction):
        self.jumping = True
        self.velocity = JUMP_VELOCITY
        if direction == 'left':
            self.jumping_left = True
        elif direction == 'right':
            self.jumping_right = True

    # The player is still jumping and will continue to jump until they land on a ledge
    def jump_move(self):

        # Update velocity by gravity, then move the player up/down by the value of the velocity
        self.velocity -= GRAVITY
        self.move(0, -self.velocity)

        # When jumping left/right the player moves at half the normal speed horizontally
        if self.jumping_right is True:
            self.move(MOVEMENT_SPACE / 2, 0)
        elif self.jumping_left is True:
            self.move(-MOVEMENT_SPACE / 2, 0)

    # Has the player collided with a doom monster?
    def check_doom_monsters(self):
        for monster in doom_monsters:
            if self.rect.colliderect(monster.rect):
                self.game_over = True

    # Has the player hit water?
    def check_water(self):
        for wave in water:
            if self.rect.colliderect(wave.rect):
                self.game_over = True

    # Has the player collected a diamond?
    def check_diamonds(self):
        for diamond in diamonds:
            if self.rect.colliderect(diamond.rect):
                diamonds.remove(diamond)
                self.diamonds_collected += 1

    # Has the player found an exit?
    def check_exit(self, game_level):
        if self.rect.colliderect(game_level.exit_door.rect):

            # If an exit has been found, level up
            game_level.level_up()
            if game_level.level_number < 3:
                game_level.set_up()
                self.set_location(game_level.player_start_loc)
            else:
                self.game_completed = True


# Doom monster class
class DoomMonster:

    # Initialise each doom monster with a starting location, and also the point where it will change direction
    def __init__(self, start_x, start_y, end_x):
        doom_monsters.append(self)
        self.start_x_coord = start_x * BLOCK_SIZE
        self.start_y_coord = start_y * BLOCK_SIZE
        self.end_x_coord = end_x * BLOCK_SIZE
        self.monster_move = DOOM_MONSTER_MOVE

        self.direction = DOOM_RIGHT
        self.x = self.start_x_coord
        self.y = self.start_y_coord

        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    # Move the doom monster horizontally by dx pixels
    def move(self):
        self.x += self.monster_move * self.direction

        # If the monster goes beyond its start or end location, change direction
        if self.x < self.start_x_coord or self.x > self.end_x_coord:

            # Direction is either 1 or -1
            # By multiplying direction by -1, it will be the negative of itself
            self.direction *= -1
            
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)


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
        Block.__init__(self, start_location, block_length)
        ledges.append(self)


# Water class inherits from the Block class
class WaterBlock(Block):
    def __init__(self, start_location, block_length):
        Block.__init__(self, start_location, block_length)
        water.append(self)


# Diamond class inherits from the Block class (only 1 block long)
class Diamond(Block):
    def __init__(self, start_location):
        Block.__init__(self, start_location, 1)
        diamonds.append(self)


# Exit Door class
class ExitDoor:
    def __init__(self, location):
        self.location = location
        x_coord = self.location[0] * BLOCK_SIZE
        y_coord = self.location[1] * BLOCK_SIZE
        self.rect = pygame.Rect(x_coord, y_coord, BLOCK_SIZE, BLOCK_SIZE)


# The Level classs
class Level:

    def __init__(self):
        self.level_number = 3
        self.exit_door = None
        self.player_start_loc = None

    # delete the ledge, water, diamonds and doom_monster lists
    def set_up(self):
        del ledges[:]
        del water[:]
        del diamonds[:]
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

            self.exit_door = ExitDoor([0, 4])

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

            self.exit_door = ExitDoor([39, 4])

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

            self.exit_door = ExitDoor([0, 6])

            self.player_start_loc = [1, 25]

    def level_up(self):
        self.level_number += 1


# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
game_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Lair of Doom')
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
medium_font = pygame.font.SysFont('Helvetica Bold', 24)
large_font = pygame.font.SysFont('Helvetica Bold', 36)

# Load images
background_image = pygame.image.load('background.png').convert_alpha()
char_image = pygame.image.load('main_character.png').convert_alpha()
ledge_image = pygame.image.load('ledge.png').convert_alpha()
exit_image = pygame.image.load('exit.png').convert_alpha()
diamond_image = pygame.image.load('diamond.png').convert_alpha()
water_image = pygame.image.load('water.png').convert_alpha()
doom_monster_image = pygame.image.load('doom_monster.png').convert_alpha()

# Initialise lists
ledges = []
water = []
diamonds = []
doom_monsters = []


def main():
    
    # Initialise objects
    player = Player()
    game_level = Level()
    game_level.set_up()
    player.set_location(game_level.player_start_loc)

    # Main game loop
    while True:
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            # Space pressed and player is not already jumping
            if key_pressed[pygame.K_SPACE] and player.jumping is False:
                if key_pressed[pygame.K_RIGHT]:
                    player.start_jump('right')
                elif key_pressed[pygame.K_LEFT]:
                    player.start_jump('left')
                else:
                    player.start_jump('Up')

            # Left key pressed
            elif key_pressed[pygame.K_LEFT]:
                if player.jumping is False:
                    player.move(-MOVEMENT_SPACE, 0)
                else:
                    player.jumping_left = True

            # Right key pressed
            elif key_pressed[pygame.K_RIGHT]:
                if player.jumping is False:
                    player.move(MOVEMENT_SPACE, 0)
                else:
                    player.jumping_right = True

            # Game has ended and player has pressed return
            elif key_pressed[pygame.K_RETURN]:
                if player.game_over is True or player.game_completed is True:
                    game_level = Level()
                    game_level.set_up()
                    player = Player()
                    player.set_location(game_level.player_start_loc)
                    player.diamonds_collected = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update player location if jumping / falling
        if player.jumping is True:
            player.jump_move()

        # Move doom monsters
        for monster in doom_monsters:
            monster.move()

        # Check if player has collided with anything
        player.check_doom_monsters()
        player.check_water()
        player.check_diamonds()
        player.check_exit(game_level)

        # Draw background
        game_screen.blit(background_image, [0, 0])

        # Draw ledges
        for ledge in ledges:
            for block_count in range(ledge.block_length):
                game_screen.blit(ledge_image, [ledge.rect.x + block_count * BLOCK_SIZE, ledge.rect.y])

        # Draw water
        for wave in water:
            for block_count in range(wave.block_length):
                game_screen.blit(water_image, [wave.rect.x + block_count * BLOCK_SIZE, wave.rect.y])

        # Draw diamonds
        for diamond in diamonds:
            game_screen.blit(diamond_image, [diamond.rect.x, diamond.rect.y])

        # Draw doom monsters
        for monster in doom_monsters:
            game_screen.blit(doom_monster_image, [monster.rect.x, monster.rect.y])

        # Draw exit
        game_screen.blit(exit_image, [game_level.exit_door.rect.x, game_level.exit_door.rect.y])

        # Draw player
        if player.game_over is False:
            game_screen.blit(char_image, [player.rect.x, player.rect.y])

        display_scoreboard(player.diamonds_collected)

        # Display Game Over
        if player.game_over is True:
            display_game_over('Game Over')
        elif player.game_completed is True:
            display_game_over('Game Completed')

        pygame.display.update()
        clock.tick(60)


# Display scoreboard
def display_scoreboard(score):

    score_text = 'Score: ' + str(score)
    text = medium_font.render(score_text, True, WHITE)
    game_screen.blit(text, [H_SCOREBOARD_MARGIN, V_SCOREBOARD_MARGIN])


# Display game over messages
def display_game_over(message_text):

    game_message_background_rect = (
        MESSAGEBOX_MARGIN, MESSAGEBOX_TOP,
        SCREEN_WIDTH - 2 * MESSAGEBOX_MARGIN, MESSAGEBOX_HEIGHT
    )

    pygame.draw.rect(game_screen, DARK_RED, game_message_background_rect)

    text_1 = large_font.render(message_text, True, YELLOW)
    text_rect_1 = text_1.get_rect()
    game_screen.blit(text_1,
                     [(SCREEN_WIDTH - text_rect_1.width) / 2,
                      MESSAGEBOX_TOP + MESSAGEBOX_TEXT_MARGIN]
                     )

    text_2 = medium_font.render('Press RETURN to play again', True, WHITE)
    text_rect_2 = text_2.get_rect()
    game_screen.blit(text_2,
                     [(SCREEN_WIDTH - text_rect_2.width) / 2,
                      MESSAGEBOX_TOP + MESSAGEBOX_HEIGHT - MESSAGEBOX_TEXT_MARGIN - text_rect_2.height]
                     )


if __name__ == '__main__':
    main()