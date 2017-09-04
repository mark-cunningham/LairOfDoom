# Lair of Doom
# Code Angel

# Classes: Player

import pygame

import level
import screen
import lair_of_doom

GRAVITY = 0.6
MOVEMENT_SPACE = 5
JUMP_VELOCITY = 10


# Player class
class Player:

    def __init__(self):
        self.image = lair_of_doom.load_media('image', 'player')

        self.diamond_sound = lair_of_doom.load_media('audio', 'diamond')
        self.completed_sound = lair_of_doom.load_media('audio', 'level_completed')
        self.game_over_sound = lair_of_doom.load_media('audio', 'game_over')

        self.velocity = 0
        self.diamonds_collected = 0

        self.jumping = False
        self.jumping_left = False
        self.jumping_right = False

        self.game_over = False
        self.game_completed = False

        self.rect = pygame.Rect(0, 0, level.BLOCK_SIZE, level.BLOCK_SIZE)

    # set the player location at the start of the game
    def set_location(self, location):
        x_coord = location[0] * level.BLOCK_SIZE
        y_coord = location[1] * level.BLOCK_SIZE
        self.rect = pygame.Rect(x_coord, y_coord, level.BLOCK_SIZE, level.BLOCK_SIZE)

    # Move the player
    def move(self, dx, dy):

        # Move the player dx pixels horizontally, dy pixels vertically
        self.rect.x += dx
        self.rect.y += dy

        # Keep the player from going off left and right edges of the screen
        if self.rect.x >= screen.SCREEN_WIDTH - level.BLOCK_SIZE:
            self.rect.x = screen.SCREEN_WIDTH - level.BLOCK_SIZE
        if self.rect.x <= 0:
            self.rect.x = 0

        # Check if the moving player has hit a ledge
        for ledge in level.ledges:
            if self.rect.colliderect(ledge.rect):

                # player moving right hits the left edge of a ledge, so don't move any further
                if dx > 0:
                    self.rect.right = ledge.rect.left

                # player moving left  hits the right edge of a ledge, so don't move any further
                if dx < 0:
                    self.rect.left = ledge.rect.right

                # player jumping hits the bottom of a ledge so stop going up and start falling
                if dy < 0:
                    self.rect.top = ledge.rect.bottom
                    self.velocity = 0

                # player falling lands on a ledge, so stop falling down
                if dy > 0:
                    self.rect.bottom = ledge.rect.top
                    self.jumping = False
                    self.jumping_left = False
                    self.jumping_right = False
                    self.velocity = 0

        # Check there is a ledge directly below the player. If so, ledge_below should be True
        self.rect.y += MOVEMENT_SPACE
        ledge_below = False
        for ledge in level.ledges:
            if self.rect.colliderect(ledge.rect):
                ledge_below = True

        self.rect.y -= MOVEMENT_SPACE

        # If there is no ledge below start falling
        if ledge_below is False and self.jumping is False:
            self.jumping = True
            self.velocity = 0

    # The player starts a jump
    def start_jump(self):
        self.jumping = True
        self.velocity = JUMP_VELOCITY

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
        for monster in level.doom_monsters:
            if self.rect.colliderect(monster.rect):
                if self.game_over is False:
                    self.game_over = True
                    self.game_over_sound.play()

    # Has the player hit water?
    def check_water(self):
        for wave in level.water:
            if self.rect.colliderect(wave.rect):
                if self.game_over is False:
                    self.game_over = True
                    self.game_over_sound.play()

    # Has the player collected a diamond?
    def check_diamonds(self):
        for diamond in level.diamonds:
            if self.rect.colliderect(diamond.rect):
                level.diamonds.remove(diamond)
                self.diamonds_collected += 1
                self.diamond_sound.play()

    # Has the player found an exit?
    def check_exit(self, game_level):
        for door in level.exit_doors:
            if self.rect.colliderect(door.rect):

                # If an exit has been found, level up
                game_level.level_up()
                self.completed_sound.play()
                if game_level.level_number < 4:
                    game_level.set_up()
                    self.set_location(game_level.player_start_loc)
                else:
                    self.game_completed = True