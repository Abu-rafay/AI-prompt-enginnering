import sys
import pygame
import random
from collections import deque

class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color_top = (30, 30, 45) 
        self.bg_color_bottom = (10, 10, 15) 
        self.border_color = (0, 255, 255) 
        self.fps = 60
        self.bat_speed = 10.0

class Block(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, health):
        super().__init__()
        self.width = 49 # Adjusted to fit within borders
        self.height = 15
        self.health = health
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.update_appearance()

    def update_appearance(self):
        self.image.fill((0, 0, 0, 0))
        if self.health == 3: color = (255, 140, 0) 
        elif self.health == 2: color = (50, 205, 50) 
        elif self.health == 1: color = (0, 191, 255) 
        else: color = (0, 0, 0, 0)
        
        pygame.draw.rect(self.image, color, (0, 0, self.width, self.height), border_radius=4)
        pygame.draw.line(self.image, (255, 255, 255, 100), (2, 2), (self.width-2, 2), 1)

    def hit(self):
        self.health -= 1
        if self.health <= 0: return True
        self.update_appearance()
        return False

class Bat:
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.width = 130
        self.height = 15
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (400, 595)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right: self.rect.x += self.settings.bat_speed
        if self.moving_left: self.rect.x -= self.settings.bat_speed
        
        # Mouse support
        mouse_x, _ = pygame.mouse.get_pos()
        if pygame.mouse.get_rel()[0] != 0:
            self.rect.centerx = mouse_x
        
        # Clamp to border
        if self.rect.left < 5: self.rect.left = 5
        if self.rect.right > 795: self.rect.right = 795

    def draw(self):
        # Shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4; shadow_rect.y += 4
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=8)
        # Main Bat
        pygame.draw.rect(self.screen, (100, 100, 110), self.rect, border_radius=8)
        shine_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height // 2)
        pygame.draw.rect(self.screen, (150, 150, 160), shine_rect, border_top_left_radius=8, border_top_right_radius=8)

class Ball(pygame.sprite.Sprite):
    def __init__(self, bb_game, x_vel, y_vel):
        super().__init__()
        self.screen = bb_game.screen
        self.radius = 10
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(400, 400))
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.x_vel, self.y_vel = x_vel, y_vel
        self.history = deque(maxlen=8) 

    def update(self, bat, blocks):
        self.history.append(self.rect.center)
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x, self.rect.y = self.x, self.y

        # Border bounces (5px offset for visible border)
        if self.rect.right >= 795 or self.rect.left <= 5: self.x_vel *= -1
        if self.rect.top <= 5: self.y_vel *= -1
        if self.rect.top >= 600: self.kill()

        if self.rect.colliderect(bat.rect):
            self.y_vel *= -1
            self.rect.bottom = bat.rect.top
            self.y = float(self.rect.y)

        hits = pygame.sprite.spritecollide(self, blocks, False)
        blocks_destroyed = 0
        if hits:
            self.y_vel *= -1
            for block in hits:
                if block.hit(): 
                    block.kill()
                    blocks_destroyed += 1
        return blocks_destroyed

    def draw_fancy(self):
        for i, pos in enumerate(self.history):
            alpha = int(180 * (i / len(self.history))) 
            temp_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (0, 255, 255, alpha), (self.radius, self.radius), self.radius)
            self.screen.blit(temp_surf, (pos[0]-self.radius, pos[1]-self.radius))
        self.screen.blit(self.image, self.rect)

class BatAndBallGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Neon Breakout - Multi-Ball Respawn")
        self.clock = pygame.time.Clock()
        self.bat = Bat(self)
        self.blocks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.destroyed_count = 0
        self._create_block_grid()
        # Start with ONE ball
        self._spawn_ball()
        pygame.mouse.get_rel()

    def _spawn_ball(self):
        """Creates a new ball with randomized speeds."""
        x_speed = random.uniform(4.0, 7.0) * random.choice([-1, 1])
        y_speed = random.uniform(-6.0, -4.0)
        self.balls.add(Ball(self, x_speed, y_speed))

    def _create_block_grid(self):
        # Starts blocks at x=6 to avoid overlapping the 5px border
        for r in range(8):
            for c in range(16):
                self.blocks.add(Block(c*49.5 + 6, r*19 + 25, random.choice([1, 2, 3])))

    def _draw_background(self):
        for y in range(600):
            ratio = y / 600
            r = int(self.settings.bg_color_top[0] * (1-ratio) + self.settings.bg_color_bottom[0] * ratio)
            g = int(self.settings.bg_color_top[1] * (1-ratio) + self.settings.bg_color_bottom[1] * ratio)
            b = int(self.settings.bg_color_top[2] * (1-ratio) + self.settings.bg_color_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (800, y))
        pygame.draw.rect(self.screen, self.settings.border_color, (0, 0, 800, 600), 5)

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: self.bat.moving_right = True
                    if event.key == pygame.K_LEFT: self.bat.moving_left = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT: self.bat.moving_right = False
                    if event.key == pygame.K_LEFT: self.bat.moving_left = False

            self.bat.update()
            
            # Update balls and track total kills
            frame_kills = 0
            for ball in self.balls:
                frame_kills += ball.update(self.bat, self.blocks)
            
            self.destroyed_count += frame_kills

            # Respawn Logic: Every 10 bricks, add a new ball
            if self.destroyed_count >= 10:
                self._spawn_ball()
                self.destroyed_count -= 10 # Subtract 10 so leftovers count toward the next spawn

            self._draw_background()
            self.blocks.draw(self.screen)
            self.bat.draw()
            for ball in self.balls: ball.draw_fancy()
            
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

if __name__ == '__main__':
    BatAndBallGame().run_game()