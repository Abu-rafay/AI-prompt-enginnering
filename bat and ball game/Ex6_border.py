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
        self.bottom_margin = 5 

        # Ball settings
        self.ball_speed = 4.0

class Bat:
    """A class to manage the player's bat."""
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.screen_rect = bb_game.screen.get_rect()

        self.width = 130
        self.height = 10
        self.color = (244, 164, 96) 

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom -= self.settings.bottom_margin

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.bat_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.bat_speed

        mouse_rel = pygame.mouse.get_rel()
        if mouse_rel[0] != 0:
            mouse_x, _ = pygame.mouse.get_pos()
            self.rect.centerx = mouse_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_rect.right:
            self.rect.right = self.screen_rect.right

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=5)

class Ball:
    """A class to manage the ball."""
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.screen_rect = bb_game.screen.get_rect()
        
        # Ball properties
        self.radius = 10
        self.color = (255, 255, 255) 
        
        # Starting position (Middle)
        self.x = float(self.screen_rect.centerx)
        self.y = float(self.screen_rect.centery)

        # Velocity: Moves at 45 degree angle initially
        self.x_velocity = self.settings.ball_speed
        self.y_velocity = self.settings.ball_speed

    def update(self):
        """Update ball position and check for wall collisions."""
        # Update position
        self.x += self.x_velocity
        self.y += self.y_velocity

        # Collision: Right Wall
        if self.x + self.radius >= self.screen_rect.right:
            self.x_velocity *= -1
        
        # Collision: Left Wall
        if self.x - self.radius <= 0:
            self.x_velocity *= -1

        # Collision: Top Wall
        if self.y - self.radius <= 0:
            self.y_velocity *= -1

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

        self.bat = Bat(self)
        self.ball = Ball(self)
        pygame.mouse.get_rel()

    def run_game(self):
        while True:
            self._check_events()
            self.bat.update()
            self.ball.update() # Added ball update
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