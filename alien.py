import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to model a sigle alien ship"""

    def __init__(self, game_settings, game_board):
        """Initialize the single alien"""
        super().__init__()
        self.board = game_board
        self.settings = game_settings

        # Load Alien Image and set its rect atribute
        self.image = pygame.image.load('images/clip-art-ufo-flying-saucer-vmuozjo.png')
        self.rect = self.image.get_rect()

        # Start each new alien at the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store pos as a float
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at the current location"""
        self.board.blit(self.image, self.rect)

    def update(self):
        """A method to move the Alien right"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edge(self):
        """Returns true if Alien is at the edge of the game board"""
        board_rect = self.board.get_rect()
        if self.rect.right >= board_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



