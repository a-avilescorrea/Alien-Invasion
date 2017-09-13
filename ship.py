import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to model the ship in Alien Invasion"""

    def __init__(self, game_settings, board):
        """Initialize the ship and starting position"""
        super(Ship, self).__init__()
        self.game_board = board
        self.game_settings = game_settings

        # Load the ship image and gets it's bounding rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.game_board_rect = board.get_rect()

        # position new ships at the bottom center of screen
        self.rect.centerx = self.game_board_rect.centerx
        self.rect.bottom = self.game_board_rect.bottom

        # Store a float for ships center
        self.center = float(self.rect.centerx)

        # Give the ship Movement Flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its location"""
        self.game_board.blit(self.image, self.rect)

    def update(self):
        """Update the ships position based on Movement Flag"""
        # Updates the variable storing the center not the rect
        if self.moving_right and self.rect.right < self.game_board_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Update center of rect
        self.rect.centerx = self.center

    def center_ship(self):
        """Center ship on the screen"""
        self.center = self.game_board_rect.centerx
