class Settings:
    """A class to store all settings for Alien Shooter."""
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.fps = 60
        self.bg_color = (255, 255, 255) 

        # Ship settings
        self.ship_speed = 7.0
        self.ship_limit = 3 

        # Bullet settings
        self.bullet_speed = 12.0
        self.bullet_width = 6
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        # Progression Constants
        self.speedup_scale = 2.0  
        self.max_level = 10
        
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Settings that reset at the start of Level 1."""
        self.game_level = 1
        self.alien_speed = 2.0      
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 
        self.max_bullets = 40 

    def increase_difficulty(self):
        """Scale difficulty, but CAP speed at Level 5 to keep it playable."""
        if self.game_level < self.max_level:
            self.game_level += 1
            
            # Only double the speed if we are BELOW Level 6
            if self.game_level <= 5:
                self.alien_speed *= self.speedup_scale
                self.fleet_drop_speed += 2 
            
            # Ammo continues to decrease every level to add challenge
            self.max_bullets -= 2