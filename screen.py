# Lair of Doom
# Code Angel

# Screen display functions

import pygame

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


# Display scoreboard
def display_scoreboard(game_screen, medium_font, score):

    score_text = 'Score: ' + str(score)
    text = medium_font.render(score_text, True, WHITE)
    game_screen.blit(text, [H_SCOREBOARD_MARGIN, V_SCOREBOARD_MARGIN])


# Display game over messages
def display_game_over(game_screen, medium_font, large_font, message_text):

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
                      MESSAGEBOX_TOP + MESSAGEBOX_HEIGHT - MESSAGEBOX_TEXT_MARGIN - text_rect_2.height])