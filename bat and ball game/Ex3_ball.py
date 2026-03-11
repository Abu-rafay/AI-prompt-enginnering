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
        self.bat_speed = 7.0
        self.bottom_margin = 5  # Exactly 5px from bottom

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
        
        # Position: Bottom center with exactly 5px space from the edge
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom -= self.settings.bottom_margin

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update position while maintaining a 5px gap from side borders."""
        if self.moving_right and self.rect.right < (self.screen_rect.right - 5):
            self.rect.x += self.settings.bat_speed
        if self.moving_left and self.rect.left > 5:
            self.rect.x -= self.settings.bat_speed

    def draw(self):
        """Draw the bat with rounded corners."""
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=5)

class Ball:
    """A class to manage the ball."""
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        
        # Ball properties
        self.radius = 10
        self.color = (255, 255, 255) # White
        
        # Starting position: Centered horizontally, 50px above the bat
        self.x = float(bb_game.bat.rect.centerx)
        self.y = float(bb_game.bat.rect.top - 50)

    def draw(self):
        """Draw the ball to the screen."""
        # Note: draw.circle requires integer coordinates
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

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

        # Initialize game objects
        self.bat = Bat(self)
        self.ball = Ball(self)

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
        self.ball.draw()
        pygame.display.flip()

if __name__ == '__main__':
    bb_game = BatAndBallGame()
    bb_game.run_game()