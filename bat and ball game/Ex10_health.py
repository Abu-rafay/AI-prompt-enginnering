import sys
import pygame
import random

class Settings:
    """A class to store all settings for the game."""
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (50, 50, 50) 
        self.fps = 60
        
        self.bat_speed = 8.0
        self.bottom_margin = 0  # Flush against the bottom
        self.ball_speed = 5.0

class Block(pygame.sprite.Sprite):
    """A class representing a breakable block with specific color-health mapping."""
    def __init__(self, x_pos, y_pos, health):
        super().__init__()
        self.width = 50
        self.height = 15
        self.health = health
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        
        self.update_appearance()

    def update_appearance(self):
        """Update color based on your specific requirements: 3=Orange, 2=Green, 1=Blue."""
        self.image.fill((0, 0, 0, 0)) # Clear for rounded corners
        
        if self.health == 3:
            color = (255, 165, 0) # Orange
        elif self.health == 2:
            color = (0, 255, 0)   # Green
        elif self.health == 1:
            color = (0, 191, 255) # Deep Sky Blue
        else:
            color = (0, 0, 0, 0)

        pygame.draw.rect(self.image, color, (0, 0, self.width, self.height), border_radius=6)

    def hit(self):
        """Handle damage and update visual."""
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            self.update_appearance()

class Bat:
    """A class to manage the player's bat with strict boundary limits."""
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.screen_rect = bb_game.screen.get_rect()
        self.width = 130
        self.height = 10
        self.color = (244, 164, 96) 
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False

    def update(self):
        # Keyboard movement
        if self.moving_right:
            self.rect.x += self.settings.bat_speed
        if self.moving_left:
            self.rect.x -= self.settings.bat_speed

        # Mouse movement
        mouse_rel = pygame.mouse.get_rel()
        if mouse_rel[0] != 0:
            mouse_x, _ = pygame.mouse.get_pos()
            self.rect.centerx = mouse_x

        # STRICT BOUNDARY CHECK: Bat cannot leave the display
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
        self.radius = 10
        self.color = (255, 255, 255) 
        self.x = float(self.screen_rect.centerx)
        self.y = float(self.screen_rect.centery)
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.x_velocity = self.settings.ball_speed
        self.y_velocity = self.settings.ball_speed

    def update(self, bat, blocks):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.centerx = self.x
        self.rect.centery = self.y

        # Bounce off walls
        if self.x + self.radius >= self.screen_rect.right or self.x - self.radius <= 0:
            self.x_velocity *= -1
        if self.y - self.radius <= 0:
            self.y_velocity *= -1

        # Bounce off bat
        if self.rect.colliderect(bat.rect):
            self.y_velocity *= -1
            self.rect.bottom = bat.rect.top
            self.y = float(self.rect.centery)

        # Hit blocks
        hits = pygame.sprite.spritecollide(self, blocks, False)
        if hits:
            self.y_velocity *= -1
            for block in hits:
                block.hit()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

class BatAndBallGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bat and Ball Game")
        self.clock = pygame.time.Clock()
        self.bat = Bat(self)
        self.ball = Ball(self)
        self.blocks = pygame.sprite.Group()
        self._create_block_grid()
        pygame.mouse.get_rel()

    def _create_block_grid(self):
        """Creates a grid at the top with randomized block health/colors."""
        block_width = 50
        block_height = 15
        v_gap = 4
        top_offset = 20
        columns = 800 // block_width
        rows = 8

        for row in range(rows):
            for col in range(columns):
                x = col * block_width
                y = row * (block_height + v_gap) + top_offset
                # Assign random health: 3(Orange), 2(Green), or 1(Blue)
                random_health = random.choice([1, 2, 3])
                new_block = Block(x, y, random_health)
                self.blocks.add(new_block)

    def run_game(self):
        while True:
            self._check_events()
            self.bat.update()
            self.ball.update(self.bat, self.blocks) 
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: self.bat.moving_right = True
                elif event.key == pygame.K_LEFT: self.bat.moving_left = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT: self.bat.moving_right = False
                elif event.key == pygame.K_LEFT: self.bat.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.blocks.draw(self.screen)
        self.bat.draw()
        self.ball.draw()
        pygame.display.flip()

if __name__ == '__main__':
    bb_game = BatAndBallGame()
    bb_game.run_game()