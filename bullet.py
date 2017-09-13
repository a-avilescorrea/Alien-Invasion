import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A Class to model a bullet for Alien Invasion"""

    def __init__(self, settings, game_board, ship):
        """Create a bullet object"""
        super().__init__()
        self.game_board = game_board

        # Create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_length)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet's pos as a float
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed

    def update(self):
        """A method to update the bullet"""
        # Move the bullet up on the screen
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """A method to draw the bullet"""
        pygame.draw.rect(self.game_board, self.color, self.rect)

