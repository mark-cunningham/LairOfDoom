# The Lair of Doom

import pygame, sys
from pygame.locals import *


# Define the colours
WHITE = (255, 255, 255)
GREEN = (165, 201, 153)
BLUE = (0,71,119)

# Define constants
SCREENWIDTH = 640
SCREENHEIGHT = 480
VSCOREBOARDMARGIN = 2
HSCOREBOARDMARGIN = 4
SCOREBOARDHEIGHT = 24
MESSAGEBOXHEIGHT = SCREENHEIGHT / 4
MESSAGEBOXTOP = (SCREENHEIGHT - MESSAGEBOXHEIGHT) / 2
MESSAGEBOXMARGIN = SCREENWIDTH / 8
MESSAGEBOXTEXTMARGIN = 16

GRAVITY = 0.6
BLOCKSIZE = 16
MOVEMENTSPACE = 5
JUMPVELOCITY = 10

DOOMMONSTERMOVE = 2

# Define globals

# Player class
class Player(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.velocity = 0
        self.jumping = False
        self.jumping_left = False
        self.jumping_right = False
        self.score = 0

    def set_location(self, location):
        x_coord = location[0] * BLOCKSIZE
        y_coord = location[1] * BLOCKSIZE
        self.rect = pygame.Rect(x_coord, y_coord, BLOCKSIZE, BLOCKSIZE)

    def move(self, dx, dy):
        
        # Move the rectangle
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.x >= SCREENWIDTH - BLOCKSIZE:
            self.rect.x = SCREENWIDTH - BLOCKSIZE
        if self.rect.x <= 0:
            self.rect.x = 0


        # Check for any ledge collisions
        for ledge in ledges:
            if self.rect.colliderect(ledge.rect):
                if dx > 0:
                    self.rect.right = ledge.rect.left
                if dx < 0:
                    self.rect.left = ledge.rect.right
                if dy > 0:
                    self.rect.bottom = ledge.rect.top
                    self.jumping = False
                    self.jumping_left = False
                    self.jumping_right = False
                    velocity = 0
                if dy < 0:
                    self.rect.top = ledge.rect.bottom


        # Check there is ground below - otherwise start falling
        self.rect.y += MOVEMENTSPACE
        ledge_below = False
        for ledge in ledges:
            if self.rect.colliderect(ledge.rect):
                ledge_below = True

        self.rect.y -= MOVEMENTSPACE
        if ledge_below is False:
            self.jumping = True



        # Check for any water collisions
        for wave in water:
            if self.rect.colliderect(wave.rect):
                game_level.game_over = True

        # Check for any diamond collisions
        for diamond in diamonds:
            if self.rect.colliderect(diamond.rect):
                diamonds.remove(diamond)
                self.score = self.score + 10

        # Check for any doom monster collisions
        for monster in doom_monsters:
            if self.rect.colliderect(monster.rect):
                game_level.game_over = True

        # Check for exit door collision       
        if self.rect.colliderect(game_level.exit_door.rect):
            game_level.level_up()
            

    def start_jump(self, direction):
        self.jumping = True
        self.velocity = JUMPVELOCITY
        if direction == "Left":
            self.jumping_left = True
        elif direction == "Right":
            self.jumping_right = True

    def jump_move(self):
        self.velocity = self.velocity - GRAVITY
        self.move(0, -self.velocity)
        if self.jumping_right is True:
            self.move(MOVEMENTSPACE / 4, 0)
        elif self.jumping_left is True:
            self.move(-MOVEMENTSPACE / 4, 0)        

    
# Ledge class
class LedgeBlock(object):
    
    def __init__(self, start_location, blocks):
        ledges.append(self)
        self.blocks = blocks
        x_coord = start_location[0] * BLOCKSIZE
        y_coord = start_location[1] * BLOCKSIZE
        self.rect = pygame.Rect(x_coord, y_coord, blocks * BLOCKSIZE, BLOCKSIZE)


# Water class
class WaterBlock(object):

    def __init__(self, start_location, blocks):
        water.append(self)
        self.blocks = blocks
        x_coord = start_location[0] * BLOCKSIZE
        y_coord = start_location[1] * BLOCKSIZE
        self.rect = pygame.Rect(x_coord, y_coord, blocks * BLOCKSIZE, BLOCKSIZE)


# Diamond class
class Diamond(object):
    
    def __init__(self, location):
        diamonds.append(self)
        x_coord = location[0] * BLOCKSIZE
        y_coord = location[1] * BLOCKSIZE
        self.rect = pygame.Rect(x_coord, y_coord, BLOCKSIZE, BLOCKSIZE)


# Doom monster class
class DoomMonster(object):
    
    def __init__(self, start_x, start_y, end_x):
        doom_monsters.append(self)
        self.start_x_coord = start_x * BLOCKSIZE
        self.start_y_coord = start_y * BLOCKSIZE
        self.end_x_coord = end_x * BLOCKSIZE

        self.direction = 1
        self.x = self.start_x_coord
        self.y = self.start_y_coord

        self.rect = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)

    def move(self, dx):
        self.x = self.x + dx * self.direction
        if self.x < self.start_x_coord or self.x > self.end_x_coord:
            self.direction = self.direction * -1
            
        self.rect = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)

        # Check for player collision       
        if self.rect.colliderect(player.rect):
            game_level.game_over = True






# Exit class
class ExitDoor(object):

    def __init__(self, location):
        self.location = location
        x_coord = self.location[0] * BLOCKSIZE
        y_coord = self.location[1] * BLOCKSIZE
        self.rect = pygame.Rect(x_coord, y_coord, BLOCKSIZE, BLOCKSIZE)

# Levels
class Level(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.level_number = 1
        self.game_over = False
        self.game_completed = False

    
    def set_up(self):
        del ledges[:]
        del water[:]
        del diamonds[:]
        del doom_monsters[:]
        
        
        if self.level_number == 1:
            LedgeBlock([0,29], 40)
            LedgeBlock([8,26], 4)
            LedgeBlock([14,22], 6)
            LedgeBlock([10,19], 2)
            LedgeBlock([15,15], 12)
            LedgeBlock([29,21], 8)
            LedgeBlock([36,16], 4)
            LedgeBlock([38,12], 2)
            LedgeBlock([32,8], 4)
            LedgeBlock([20,8], 8)
            LedgeBlock([6,8], 10)
            LedgeBlock([0,5], 4)

            Diamond([18,21])
            Diamond([29,20])
            Diamond([39,15])
            Diamond([24,7])

            self.exit_door = ExitDoor([0,4])

            player.set_location([1,28])
            
        elif self.level_number == 2:
            LedgeBlock([0,26], 20)
            LedgeBlock([25,29], 8)
            LedgeBlock([37,29], 3)
            LedgeBlock([39,24], 1)
            LedgeBlock([37,19], 1)
            LedgeBlock([32,14], 3)
            LedgeBlock([6,17], 22)
            LedgeBlock([3,13], 4)
            LedgeBlock([10,10], 8)
            LedgeBlock([22,9], 6)
            LedgeBlock([32,7], 4)
            LedgeBlock([37,5], 3)

            WaterBlock([0,29], 25)
            WaterBlock([33,29], 4)

            Diamond([27,28])
            Diamond([19,16])
            Diamond([4,12])
            Diamond([19,16])
            Diamond([24,8])
            Diamond([35,6])
            

            DoomMonster(8, 25, 19)
            DoomMonster(6, 16, 14)
            DoomMonster(22, 16, 27)
            DoomMonster(10, 9, 17)
            

            self.exit_door = ExitDoor([39,4])
            
            player.set_location([1,25])
            
            

    def level_up(self):
        self.level_number = self.level_number + 1
        if self.level_number < 3:
            self.set_up()
        else:
            self.game_completed = True
        


# Setup
pygame.init()
game_screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("EZ Platformer")
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Helvetica", 16)

# Load images
char_image = pygame.image.load("main_character.png")
ledge_image = pygame.image.load("ledge.png")
exit_image = pygame.image.load("exit.png")
diamond_image = pygame.image.load("diamond.png")
water_image = pygame.image.load("water.png")
doom_monster_image = pygame.image.load("doom_monster.png")

# Initialise variables

#Initialise objects

ledges = []
water = []
diamonds = []
doom_monsters = []


player = Player()
game_level = Level()
game_level.set_up()
        

      
        
while True: # main game loop
    for event in pygame.event.get():
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_SPACE] and player.jumping is False:
            if key_pressed[pygame.K_d]:
                player.start_jump("Right")
            elif key_pressed[pygame.K_a]:
                player.start_jump("Left")
            else:
                player.start_jump("Up")
            
                    
        elif key_pressed[pygame.K_a]:
            player.move(-MOVEMENTSPACE,0)
                       
        elif key_pressed[pygame.K_d]:
            player.move(MOVEMENTSPACE,0)

        elif key_pressed[pygame.K_RETURN] and (game_level.game_over is True or game_level.game_completed is True):
            player.reset()
            game_level.reset()
            game_level.set_up()
            score = 0
         
            
                
                
    if event.type == QUIT:
        pygame.quit()     
        sys.exit()

    # Move doom monsters
    for monster in doom_monsters:
        monster.move(DOOMMONSTERMOVE)
    

    # Draw screen elements
    game_screen.fill(GREEN)

    for ledge in ledges:
        for block_count in range(ledge.blocks):
            game_screen.blit(ledge_image, [ledge.rect.x + block_count * BLOCKSIZE, ledge.rect.y])

    for wave in water:
        for block_count in range(wave.blocks):
            game_screen.blit(water_image, [wave.rect.x + block_count * BLOCKSIZE, wave.rect.y])

    for diamond in diamonds:
        game_screen.blit(diamond_image, [diamond.rect.x, diamond.rect.y])

    for monster in doom_monsters:
        game_screen.blit(doom_monster_image, [monster.rect.x, monster.rect.y])


    
    game_screen.blit(exit_image, [game_level.exit_door.rect.x, game_level.exit_door.rect.y])

    if game_level.game_over is False:
        game_screen.blit(char_image, [player.rect.x, player.rect.y])
            
    if player.jumping is True:
        player.jump_move()
                    
    # Display scores
    scoreboard_background_rect = (0, 0, SCREENWIDTH, SCOREBOARDHEIGHT)
    pygame.draw.rect(game_screen, BLUE, scoreboard_background_rect)
    score_text = "Score: " + str(player.score)
    text = font.render(score_text, True, (WHITE))
    game_screen.blit(text, [HSCOREBOARDMARGIN, VSCOREBOARDMARGIN])


    # Display Game Over
    if game_level.game_over is True:
        message_text = "Game Over"
    elif game_level.game_completed is True:
        message_text = "Game Completed"

    if game_level.game_over is True or game_level.game_completed is True:
        game_message_background_rect = (MESSAGEBOXMARGIN, MESSAGEBOXTOP, SCREENWIDTH - 2 * MESSAGEBOXMARGIN, MESSAGEBOXHEIGHT)
        pygame.draw.rect(game_screen, BLUE, game_message_background_rect)

        text_1 = font.render(message_text, True, (WHITE))
        text_rect_1 = text_1.get_rect()
        game_screen.blit(text_1, [(SCREENWIDTH - text_rect_1.width) / 2 , MESSAGEBOXTOP + MESSAGEBOXTEXTMARGIN])

        text_2 = font.render("Press RETURN to play again", True, (WHITE))
        text_rect_2 = text_2.get_rect()
        game_screen.blit(text_2, [(SCREENWIDTH - text_rect_2.width) / 2 , MESSAGEBOXTOP + MESSAGEBOXHEIGHT - MESSAGEBOXTEXTMARGIN - text_rect_2.height])

        
            
    pygame.display.update()
    clock.tick(60)



