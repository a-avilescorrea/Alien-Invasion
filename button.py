import pygame.font


class Button():
    """A class to model a button"""

    def __init__(self, game_settings, game_board, msg):
        """Initialize button"""
        self.game_board = game_board
        self.board_rect = game_board.get_rect()

        # Set the dimensions
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build Button rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.board_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
            """Turn message into a rendered image and center text on button"""
            self.msg_image = self.font.render(msg, True, self.text_color,
                                              self.button_color)
            self.msg_image_rect = self.msg_image.get_rect()
            self.msg_image_rect.center = self.rect.center

    def draw_button(self):
            """Draws the button and message"""
            self.game_board.fill(self.button_color, self.rect)
            self.game_board.blit(self.msg_image, self.msg_image_rect)


