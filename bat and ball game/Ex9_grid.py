import sys
import pygame

class Settings:
    """A class to store all settings for the game."""
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (50, 50, 50) 
        self.fps = 60
        
        self.bat_speed = 8.0
        self.bottom_margin = 5 
        self.ball_speed = 4.0

class Block(pygame.sprite.Sprite):
    """A class representing a single breakable block."""
    def __init__(self, x_pos, y_pos):
        super().__init__()
        # New smaller dimensions
        self.width = 60
        self.height = 15
        self.color = (0, 200, 0) # Green

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        
        # Set position based on passed arguments
        self.rect.x = x_pos
        self.rect.y = y_pos

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

        # Wall Collisions
        if self.x + self.radius >= self.screen_rect.right or self.x - self.radius <= 0:
            self.x_velocity *= -1
        if self.y - self.radius <= 0:
            self.y_velocity *= -1

        # Bat Collision
        if self.rect.colliderect(bat.rect):
            self.y_velocity *= -1
            self.rect.bottom = bat.rect.top
            self.y = float(self.rect.centery)

        # Block Collisions
        # sprite.spritecollide returns a list of all blocks hit
        blocks_hit = pygame.sprite.spritecollide(self, blocks, True)
        if blocks_hit:
            self.y_velocity *= -1 # Reverse direction on hit

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.radius)

class BatAndBallGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Bat and Ball Game")
        self.clock = pygame.time.Clock()

        self.bat = Bat(self)
        self.ball = Ball(self)
        
        # Create a group to hold all blocks
        self.blocks = pygame.sprite.Group()
        self._create_block_grid()
        
        pygame.mouse.get_rel()

    def _create_block_grid(self):
        """Create a grid of blocks."""
        block_width = 60
        block_height = 15
        gap = 10
        top_offset = 40
        
        # Calculate how many columns fit (approx 11 for 800px width)
        columns = self.settings.screen_width // (block_width + gap)
        rows = 5

        for row_index in range(rows):
            for col_index in range(columns):
                x = col_index * (block_width + gap) + gap
                y = row_index * (block_height + gap) + top_offset
                new_block = Block(x, y)
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
        self.bat.draw()
        self.ball.draw()
        # Draw all blocks in the group
        self.blocks.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    bb_game = BatAndBallGame()
    bb_game.run_game()