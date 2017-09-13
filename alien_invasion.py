import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """"Run the main logic of the game"""
    # Setting up the board
    pygame.init()
    game_settings = Settings()
    game_board = pygame.display.set_mode(
        (game_settings.board_width, game_settings.board_length)
        )
    pygame.display.set_caption('Alien Invasion')

    # Display Button
    play_button = Button(game_settings, game_board, "Play")

    # Create an instance to store games stats, show scoreboard
    stats = GameStats(game_settings)
    sb = Scoreboard(game_settings, game_board, stats)

    # Create a ship
    ship = Ship(game_settings, game_board)

    # Make a group for Bullets and Aliens
    bullets = Group()
    aliens = Group()
    gf.create_fleet(game_settings, game_board, ship, aliens)

    # Main driver for the game
    while True:
        gf.check_events(game_settings, game_board, stats, play_button, ship, aliens,
                        bullets, sb)

        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, game_board, ship, aliens, bullets, stats, sb)
            gf.update_aliens(game_settings, stats, game_board, ship, aliens, bullets, sb)

        gf.update_game_board(game_settings, game_board, stats, ship, aliens,
                             bullets, play_button, sb)

run_game()
