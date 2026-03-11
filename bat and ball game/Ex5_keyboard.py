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
        
        # Position: Center of display, 5px from bottom
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom -= self.settings.bottom_margin

        # Movement flags for keyboard
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the bat's position based on keyboard flags OR mouse movement."""
        
        # 1. Handle Keyboard Movement
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.bat_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.bat_speed

        # 2. Handle Mouse Movement
        # Get the relative movement of the mouse to see if it has moved
        mouse_rel = pygame.mouse.get_rel()
        if mouse_rel[0] != 0:  # If the mouse moved horizontally
            mouse_x, _ = pygame.mouse.get_pos()
            self.rect.centerx = mouse_x

        # 3. Final Boundary Check (Ensures bat stays on screen for both inputs)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right

    def draw(self):
        """Draw the bat with rounded corners."""
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=5)

class Ball:
    """A class to manage the ball."""
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.screen_rect = bb_game.screen.get_rect()
        
        # Ball properties
        self.radius = 10
        self.color = (255, 255, 255) # White
        
        # Starting position: Center of the display
        self.x = float(self.screen_rect.centerx)
        self.y = float(self.screen_rect.centery)

    def draw(self):
        """Draw the ball to the screen."""
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
        
        # Initialize mouse relative movement to prevent a jump at start
        pygame.mouse.get_rel()

    def run_game(self):
        """Main game loop."""
        while True:
            self._check_events()
            self.bat.update()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Keyboard Start (KEYDOWN)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.bat.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.bat.moving_left = True
            
            # Keyboard Stop (KEYUP)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.bat.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.bat.moving_left = False

    def _update_screen(self):
        """Redraw the screen."""
        self.screen.fill(self.settings.bg_color)
        self.bat.draw()
        self.ball.draw()
        pygame.display.flip()

if __name__ == '__main__':
    bb_game = BatAndBallGame()
    bb_game.run_game()