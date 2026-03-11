import sys
import pygame

class Settings:
    """A class to store all settings for the game."""
    def __init__(self):
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (50, 50, 50)  # Dark Gray
        
        # Timing settings
        self.fps = 60

class BatAndBallGame:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        
        # Initialize the window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Bat and Ball Game")
        
        # Create a clock to manage frame rate
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # 1. Watch for keyboard and mouse events
            self._check_events()
            
            # 2. Update screen elements (Redraw)
            self._update_screen()
            
            # 3. Maintain the frame rate
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        
        # (Game objects like the bat and ball would be drawn here)
        
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    bb_game = BatAndBallGame()
    bb_game.run_game()