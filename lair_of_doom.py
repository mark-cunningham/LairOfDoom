#!/usr/bin/python
# Lair of Doom
# Code Angel

import sys
import os
import pygame
from pygame.locals import *

import level
import player
import screen

# Setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.init()
game_screen = pygame.display.set_mode((screen.SCREEN_WIDTH, screen.SCREEN_HEIGHT))
pygame.display.set_caption('The Lair of Doom')
pygame.key.set_repeat(10, 20)
clock = pygame.time.Clock()
medium_font = pygame.font.SysFont('Helvetica Bold', 24)
large_font = pygame.font.SysFont('Helvetica Bold', 36)


def main():

    # Load background image
    background_image = load_media('image', 'background')

    # Initialise objects
    # Create a Player object. Let's call him Alfie
    alfie = player.Player()

    # Create a Level object and set up the level
    game_level = level.Level()
    game_level.set_up()

    # Set alfie's start location
    alfie.set_location(game_level.player_start_loc)

    # Main game loop
    while True:
        for event in pygame.event.get():
            key_pressed = pygame.key.get_pressed()

            # Space pressed and player is not already jumping
            if key_pressed[pygame.K_SPACE] and alfie.jumping is False:
                alfie.start_jump()

            # Left key pressed
            elif key_pressed[pygame.K_LEFT]:
                if alfie.jumping is False:
                    alfie.move(-player.MOVEMENT_SPACE, 0)
                else:
                    alfie.jumping_left = True

            # Right key pressed
            elif key_pressed[pygame.K_RIGHT]:
                if alfie.jumping is False:
                    alfie.move(player.MOVEMENT_SPACE, 0)
                else:
                    alfie.jumping_right = True

            # Game has ended and player has pressed return
            elif key_pressed[pygame.K_RETURN]:
                if alfie.game_over is True or alfie.game_completed is True:
                    game_level = level.Level()
                    game_level.set_up()
                    alfie = player.Player()
                    alfie.set_location(game_level.player_start_loc)
                    alfie.diamonds_collected = 0

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Update player location if jumping / falling
        if alfie.jumping is True:
            alfie.jump_move()

        # Move doom monsters
        for monster in level.doom_monsters:
            monster.move()

        # Check if player has collided with anything
        alfie.check_doom_monsters()
        alfie.check_water()
        alfie.check_diamonds()
        alfie.check_exit(game_level)

        # Draw background
        game_screen.blit(background_image, [0, 0])

        # Draw ledges
        for ledge in level.ledges:
            for block_count in range(ledge.block_length):
                game_screen.blit(ledge.image, [ledge.rect.x + block_count * level.BLOCK_SIZE, ledge.rect.y])

        # Draw water
        for wave in level.water:
            for block_count in range(wave.block_length):
                game_screen.blit(wave.image, [wave.rect.x + block_count * level.BLOCK_SIZE, wave.rect.y])

        # Draw diamonds
        for diamond in level.diamonds:
            game_screen.blit(diamond.image, [diamond.rect.x, diamond.rect.y])

        # Draw doom monsters
        for monster in level.doom_monsters:
            game_screen.blit(monster.image, [monster.rect.x, monster.rect.y])

        # Draw exits
        for door in level.exit_doors:
            game_screen.blit(door.image, [door.rect.x, door.rect.y])

        # Draw player
        if alfie.game_over is False:
            game_screen.blit(alfie.image, [alfie.rect.x, alfie.rect.y])

        screen.display_scoreboard(game_screen, medium_font, alfie.diamonds_collected)

        # Display Game Over
        if alfie.game_over is True:
            screen.display_game_over(game_screen, medium_font, large_font, 'Game Over')
        elif alfie.game_completed is True:
            screen.display_game_over(game_screen, medium_font, large_font, 'Game Completed')

        pygame.display.update()
        clock.tick(60)


# Get an image or audio from folder
def load_media(media_type, filename):
    media = None
    full_path = os.path.dirname(os.path.realpath(__file__))

    if media_type == 'image':
        images_path = os.path.join(full_path, 'images')
        full_filename = os.path.join(images_path, filename + '.png')
        media = pygame.image.load(full_filename).convert_alpha()
    elif media_type == 'audio':
        audio_path = os.path.join(full_path, 'audio')
        full_filename = os.path.join(audio_path, filename + '.ogg')
        media = pygame.mixer.Sound(full_filename)

    return media


if __name__ == '__main__':
    main()