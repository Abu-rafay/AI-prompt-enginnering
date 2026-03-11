import sys
import pygame
import random
import os
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
    def __init__(self, x_pos, y_pos, health, sounds):
        super().__init__()
        self.width = 49
        self.height = 15
        self.health = health
        self.sounds = sounds 
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

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            # Plays ONLY the break sound when destroyed
            if self.sounds.get('brick_break'): self.sounds['brick_break'].play() 
            return True
        else:
            # Plays the hit sound if it still has health left
            if self.sounds.get('brick_hit'): self.sounds['brick_hit'].play() 
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
        mouse_x, _ = pygame.mouse.get_pos()
        if pygame.mouse.get_rel()[0] != 0: self.rect.centerx = mouse_x
        if self.rect.left < 5: self.rect.left = 5
        if self.rect.right > 795: self.rect.right = 795

    def draw(self):
        pygame.draw.rect(self.screen, (100, 100, 110), self.rect, border_radius=8)

class Ball(pygame.sprite.Sprite):
    def __init__(self, bb_game, x_vel, y_vel, sounds):
        super().__init__()
        self.screen = bb_game.screen
        self.sounds = sounds
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

        # Border bounces - SOUNDS REMOVED HERE
        if self.rect.right >= 795 or self.rect.left <= 5: 
            self.x_vel *= -1
        if self.rect.top <= 5: 
            self.y_vel *= -1
        if self.rect.top >= 600: self.kill()

        # Bat collision - KEPT BOUNCE SOUND FOR FEEDBACK
        if self.rect.colliderect(bat.rect):
            self.y_vel *= -1
            self.rect.bottom = bat.rect.top
            self.y = float(self.rect.y)
            if self.sounds.get('bounce'): self.sounds['bounce'].play() 

        # Block collisions
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
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_dir = os.path.join(script_dir, 'assets', 'music')
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Neon Breakout - Audio Refined")
        self.clock = pygame.time.Clock()
        
        self.sounds = {}
        sound_files = {
            'bounce': 'bounce.mp3',
            'brick_hit': 'brick_hit.mp3',
            'brick_break': 'brick_break.mp3'
        }

        for key, filename in sound_files.items():
            path = os.path.join(music_dir, filename)
            try:
                self.sounds[key] = pygame.mixer.Sound(path)
            except:
                try:
                    with open(path, 'rb') as f:
                        self.sounds[key] = pygame.mixer.Sound(f)
                except Exception as e:
                    print(f"Could not load {filename}: {e}")
                    self.sounds[key] = None

        try:
            bg_path = os.path.join(music_dir, 'background.mp3')
            pygame.mixer.music.load(bg_path)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Background music error: {e}")
        
        self.bat = Bat(self)
        self.blocks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.destroyed_count = 0
        self._create_block_grid()
        self._spawn_ball() 
        pygame.mouse.get_rel()

    def _spawn_ball(self):
        x_speed = random.uniform(4.0, 7.0) * random.choice([-1, 1])
        y_speed = random.uniform(-6.0, -4.0)
        self.balls.add(Ball(self, x_speed, y_speed, self.sounds))

    def _create_block_grid(self):
        for r in range(8):
            for c in range(16):
                self.blocks.add(Block(c*49.5 + 6, r*19 + 25, random.choice([1, 2, 3]), self.sounds))

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
            frame_kills = 0
            for ball in self.balls:
                frame_kills += ball.update(self.bat, self.blocks)
            self.destroyed_count += frame_kills

            if self.destroyed_count >= 10:
                self._spawn_ball()
                self.destroyed_count -= 10 

            self._draw_background()
            self.blocks.draw(self.screen)
            self.bat.draw()
            for ball in self.balls: ball.draw_fancy()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

if __name__ == '__main__':
    BatAndBallGame().run_game()