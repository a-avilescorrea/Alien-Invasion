class GameStats():
    """A class to store the stats of Alien Invasion"""

    def __init__(self, game_settings):
        """Instantiate a Game Stats obj"""
        self.game_settings = game_settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        # save the high score
        self.high_score = 0


    def reset_stats(self):
        """Initialize game stats"""
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1

