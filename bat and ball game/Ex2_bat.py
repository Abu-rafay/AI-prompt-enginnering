import sys
import pygame

class Settings:
    """A class to store all settings for the game."""
    def __init__(self):
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (50, 50, 50)  # Dark Gray
        
        # Timing settings
        self.fps = 60
        
        # Bat settings
        self.bat_speed = 8.0
        self.edge_spacing = 5  # The 5px gap you requested

class Bat:
    """A class to manage the player's bat."""
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.screen_rect = bb_game.screen.get_rect()

        # Dimensions
        self.width = 130 
        self.height = 10
        self.color = (244, 164, 96) # Sandy Brown

        # Create the bat's rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
        # Position: Bottom center + spacing from the very bottom
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= (30 + self.settings.edge_spacing) 

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update position while maintaining a 5px gap from borders."""
        # Check right boundary minus the spacing
        if self.moving_right and self.rect.right < (self.screen_rect.right - self.settings.edge_spacing):
            self.rect.x += self.settings.bat_speed
            
        # Check left boundary plus the spacing
        if self.moving_left and self.rect.left > self.settings.edge_spacing:
            self.rect.x -= self.settings.bat_speed

    def draw(self):
        """Draw the bat with rounded corners."""
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=5)

class BatAndBallGame:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Bat and Ball Game")
        self.clock = pygame.time.Clock()

        self.bat = Bat(self)

    def run_game(self):
        while True:
            self._check_events()
            self.bat.update()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.bat.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.bat.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.bat.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.bat.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.bat.draw()
        pygame.display.flip()

if __name__ == '__main__':
    bb_game = BatAndBallGame()
    bb_game.run_game()