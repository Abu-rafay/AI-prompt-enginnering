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
        self.bat_speed = 12.0 
        self.base_ball_speed = 5.0 

class Block(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, health, sounds, is_silver=False):
        super().__init__()
        self.width = 49
        self.height = 15
        self.health = health
        self.is_silver = is_silver
        self.sounds = sounds 
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.update_appearance()

    def update_appearance(self):
        self.image.fill((0, 0, 0, 0))
        if self.is_silver:
            color = (200, 200, 205) 
            border_color = (255, 255, 255)
        else:
            border_color = (0, 0, 0, 0)
            if self.health >= 4: color = (148, 0, 211) 
            elif self.health == 3: color = (255, 140, 0) 
            elif self.health == 2: color = (50, 205, 50) 
            elif self.health == 1: color = (0, 191, 255) 
            else: color = (0, 0, 0, 0)
        
        pygame.draw.rect(self.image, color, (0, 0, self.width, self.height), border_radius=4)
        if self.is_silver:
            pygame.draw.rect(self.image, border_color, (0, 0, self.width, self.height), 2, border_radius=4)

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            if self.sounds.get('brick_break'): self.sounds['brick_break'].play() 
            return True
        else:
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
    def __init__(self, bb_game, x_vel, y_vel, sounds, max_speed):
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
        self.max_speed = max_speed

    def get_speed(self):
        return (self.x_vel**2 + self.y_vel**2)**0.5

    def update(self, bat, blocks):
        self.history.append(self.rect.center)
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x, self.rect.y = self.x, self.y

        if self.rect.right >= 795 or self.rect.left <= 5: self.x_vel *= -1
        if self.rect.top <= 5: self.y_vel *= -1
        if self.rect.top >= 600: self.kill()

        if self.rect.colliderect(bat.rect):
            self.y_vel *= -1
            self.rect.bottom = bat.rect.top
            self.y = float(self.rect.y)
            if self.sounds.get('bounce'): self.sounds['bounce'].play() 

        hits = pygame.sprite.spritecollide(self, blocks, False)
        blocks_destroyed = 0
        if hits:
            self.y_vel *= -1
            for block in hits:
                if block.hit(): 
                    block.kill()
                    blocks_destroyed += 1
                    if self.get_speed() < self.max_speed:
                        self.x_vel *= 1.02
                        self.y_vel *= 1.02
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
        pygame.mixer.init()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_dir = os.path.join(script_dir, 'assets', 'music')
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Neon Breakout - Polish Update")
        self.clock = pygame.time.Clock()
        
        self.current_level = 2 
        self.current_max_speed = 10.5
        self.destroyed_count = 0 
        self.in_transition = False
        self.transition_timer = 0

        self.sounds = {}
        sound_files = {'bounce': 'bounce.mp3', 'brick_hit': 'brick_hit.mp3', 'brick_break': 'brick_break.mp3'}
        for key, filename in sound_files.items():
            path = os.path.join(music_dir, filename)
            try: self.sounds[key] = pygame.mixer.Sound(path)
            except: self.sounds[key] = None

        self.bat = Bat(self)
        self.blocks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.start_level(1)

    def start_level(self, level_num):
        self.current_level = level_num
        self.blocks.empty()
        for ball in self.balls: ball.kill()
        self.destroyed_count = 0 
        self.in_transition = True
        self.transition_timer = pygame.time.get_ticks()
        
        if level_num == 1:
            self.ball_speed_modifier, self.current_max_speed = 0, 9.0
            for r in range(10): 
                for c in range(16):
                    if (r + c) % 2 == 0:
                        rv = random.random()
                        if rv < 0.1: is_s, hp = True, 5
                        elif rv < 0.5: is_s, hp = False, 1
                        else: is_s, hp = False, random.choice([2, 3])
                        self.blocks.add(Block(c*49.5 + 6, r*19 + 50, hp, self.sounds, is_s))
        
        elif level_num == 2:
            self.ball_speed_modifier, self.current_max_speed = 2.5, 10.5
            for r in range(6):
                for c in range(16):
                    rv = random.random()
                    if rv < 0.2: is_s, hp = True, 5
                    elif rv < 0.7: is_s, hp = False, 1
                    else: is_s, hp = False, random.choice([2, 3])
                    self.blocks.add(Block(c*49.5 + 6, r*19 + 50, hp, self.sounds, is_s))

        elif level_num == 3:
            self.ball_speed_modifier, self.current_max_speed = 5.0, 13.0
            for r in range(12):
                for c in range(16):
                    if abs(7.5 - c) + abs(5.5 - r) <= 5.5:
                        is_s = random.random() < 0.6
                        hp = 5 if is_s else 4
                        self.blocks.add(Block(c*49.5 + 6, r*19 + 50, hp, self.sounds, is_s))

    def _draw_ui(self):
        font = pygame.font.SysFont("Arial", 24, bold=True)
        # Level Text
        l_surf = font.render(f"LEVEL {self.current_level}", True, (255, 255, 255))
        self.screen.blit(l_surf, (15, 15))

        # Speedometer Logic
        if self.balls:
            main_ball = self.balls.sprites()[0]
            speed_ratio = min(main_ball.get_speed() / self.current_max_speed, 1.0)
            
            # Draw Meter Background
            meter_rect = pygame.Rect(630, 20, 150, 15)
            pygame.draw.rect(self.screen, (50, 50, 50), meter_rect, border_radius=5)
            
            # Dynamic Color (Cyan -> Red)
            color = (int(255 * speed_ratio), int(255 * (1 - speed_ratio)), 255)
            fill_rect = pygame.Rect(630, 20, 150 * speed_ratio, 15)
            pygame.draw.rect(self.screen, color, fill_rect, border_radius=5)
            
            s_label = font.render("SPEED", True, (200, 200, 200))
            self.screen.blit(s_label, (550, 15))

    def _draw_transition(self):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.SysFont("Arial", 72, bold=True)
        t_surf = font.render(f"LEVEL {self.current_level}", True, (0, 255, 255))
        t_rect = t_surf.get_rect(center=(400, 300))
        self.screen.blit(t_surf, t_rect)

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

            # Background Gradient & Border
            for y in range(600):
                ratio = y / 600
                r = int(self.settings.bg_color_top[0]*(1-ratio) + self.settings.bg_color_bottom[0]*ratio)
                g = int(self.settings.bg_color_top[1]*(1-ratio) + self.settings.bg_color_bottom[1]*ratio)
                b = int(self.settings.bg_color_top[2]*(1-ratio) + self.settings.bg_color_bottom[2]*ratio)
                pygame.draw.line(self.screen, (r, g, b), (0, y), (800, y))
            pygame.draw.rect(self.screen, self.settings.border_color, (0,0,800,600), 5)

            if self.in_transition:
                self._draw_transition()
                if pygame.time.get_ticks() - self.transition_timer > 2000:
                    self.in_transition = False
                    self._spawn_ball()
            else:
                self.bat.update()
                kills = 0
                for ball in self.balls: kills += ball.update(self.bat, self.blocks)
                self.destroyed_count += kills
                if self.destroyed_count >= 10:
                    self._spawn_ball()
                    self.destroyed_count -= 10
                
                if not self.blocks: self.start_level(self.current_level + 1)
                if not self.balls: self.start_level(self.current_level)

                self.blocks.draw(self.screen)
                self.bat.draw()
                for ball in self.balls: ball.draw_fancy()
            
            self._draw_ui()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)

    def _spawn_ball(self):
        speed = self.settings.base_ball_speed + self.ball_speed_modifier
        self.balls.add(Ball(self, speed * random.choice([-1, 1]), -speed, self.sounds, self.current_max_speed))

if __name__ == '__main__':
    BatAndBallGame().run_game()