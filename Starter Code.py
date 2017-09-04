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

