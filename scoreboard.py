import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """A class to keep score"""

    def __init__(self, game_settings, game_board, stats):
        """Initialize method"""
        self.game_board = game_board
        self.board_rect = game_board.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        # Font Settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prep the score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.game_settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.board_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """Draw the score to the screen"""
        self.game_board.blit(self.score_image, self.score_rect)
        self.game_board.blit(self.high_score_image, self.high_score_rect)
        self.game_board.blit(self.level_image, self.level_rect)
        self.ships.draw(self.game_board)

    def prep_high_score(self):
        """Draw the high score"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.game_settings.bg_color)

        # center the high schore
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.board_rect.centerx
        self.high_score_rect.top = self.board_rect.top

    def prep_level(self):
        """Draw the level"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
                                            self.game_settings.bg_color)
        # Position the level text
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Draws the ships in the upper left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game_settings, self.game_board)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)