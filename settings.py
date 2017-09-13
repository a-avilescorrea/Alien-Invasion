class Settings():
    """A class for all of the Alien Invasion settings"""
    def __init__(self):
        """Initialize Alien Invasion settings"""
        # Game Board settings
        self.board_width = 1100
        self.board_length = 700
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_length = 10
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 4

        # Alien settings
        self.alien_drop_speed = 10

        # Difficulty Settings
        self.speedup_scale = 1.2
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change"""
        self.ship_speed_factor = 2.5
        self.bullet_speed = 3
        self.alien_speed = 1

        # fleet direction means right if 1, left if -1
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings and point settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
