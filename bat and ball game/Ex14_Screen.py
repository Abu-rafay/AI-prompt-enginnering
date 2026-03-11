import sys
import pygame
import random
import os
import math
from collections import deque

# --- CONFIGURATION ---
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

# --- UI COMPONENTS ---
class Button:
    def __init__(self, x, y, width, height, text, color=(0, 255, 255)):
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        self.hovered = False

    def draw(self, screen):
        draw_color = [min(255, c + 60) for c in self.color] if self.hovered else self.color
        pygame.draw.rect(screen, (20, 20, 30), self.rect, border_radius=8)
        pygame.draw.rect(screen, draw_color, self.rect, width=2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, draw_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

# --- GAME OBJECTS ---
class Block(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, health, sounds, is_silver=False):
        super().__init__()
        self.width, self.height = 49, 15
        self.health = health
        self.is_silver = is_silver
        self.sounds = sounds 
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.update_appearance()

    def update_appearance(self):
        self.image.fill((0, 0, 0, 0))
        if self.is_silver:
            color, border = (200, 200, 205), (255, 255, 255)
        else:
            border = (0, 0, 0, 0)
            colors = {5: (200, 200, 205), 4: (148, 0, 211), 3: (255, 140, 0), 2: (50, 205, 50), 1: (0, 191, 255)}
            color = colors.get(self.health, (0, 191, 255))
        
        pygame.draw.rect(self.image, color, (0, 0, self.width, self.height), border_radius=4)
        if self.is_silver:
            pygame.draw.rect(self.image, border, (0, 0, self.width, self.height), 2, border_radius=4)

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            if self.sounds.get('brick_break'): self.sounds['brick_break'].play()
            return True
        if self.sounds.get('brick_hit'): self.sounds['brick_hit'].play()
        self.update_appearance()
        return False

class Ball(pygame.sprite.Sprite):
    def __init__(self, bb_game, x_vel, y_vel, max_speed):
        super().__init__()
        self.game = bb_game
        self.radius = 10
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(400, 400))
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.x_vel, self.y_vel = x_vel, y_vel
        self.history = deque(maxlen=8)
        self.max_speed = max_speed

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
            if self.game.sounds.get('bounce'): self.game.sounds['bounce'].play()

        hits = pygame.sprite.spritecollide(self, blocks, False)
        blocks_destroyed = 0
        if hits:
            self.y_vel *= -1
            for block in hits:
                if block.hit(): 
                    block.kill()
                    blocks_destroyed += 1
                    if (self.x_vel**2 + self.y_vel**2)**0.5 < self.max_speed:
                        self.x_vel *= 1.02
                        self.y_vel *= 1.02
        return blocks_destroyed

class Bat:
    def __init__(self, bb_game):
        self.screen = bb_game.screen
        self.settings = bb_game.settings
        self.rect = pygame.Rect(335, 580, 130, 15)
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

# --- MAIN GAME ENGINE ---
class BatAndBallGame:
    def __init__(self):
        pygame.init()
        # Audio pre-init for low latency
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        
        # --- ASSET LOADING ---
        script_dir = os.path.dirname(os.path.abspath(__file__))
        music_dir = os.path.join(script_dir, 'assets', 'music')
        
        self.sounds = {}
        sound_files = {'bounce': 'bounce.mp3', 'brick_hit': 'brick_hit.mp3', 'brick_break': 'brick_break.mp3'}
        for key, filename in sound_files.items():
            path = os.path.join(music_dir, filename)
            try:
                self.sounds[key] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Sound Error {filename}: {e}")
                self.sounds[key] = None

        try:
            pygame.mixer.music.load(os.path.join(music_dir, 'background.mp3'))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except:
            print("Background music file not found.")

        self.state = "TRANSITION" 
        self.current_level = 1
        self.destroyed_count = 0
        self.transition_timer = 0
        
        self.bat = Bat(self)
        self.blocks = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        
        cx, cy = 400, 300
        self.btn_next = Button(cx, cy + 80, 200, 50, "NEXT LEVEL", (0, 255, 150))
        self.btn_restart = Button(cx, cy + 80, 200, 50, "RESTART", (0, 200, 255))
        self.btn_quit = Button(cx, cy + 150, 200, 50, "QUIT", (255, 50, 50))

        self.start_level(1)

    def start_level(self, level_num):
        self.current_level = level_num
        self.blocks.empty()
        self.balls.empty()
        self.destroyed_count = 0
        self.state = "TRANSITION"
        self.transition_timer = pygame.time.get_ticks()
        
        if level_num == 1:
            self.ball_speed_modifier, self.current_max_speed = 0, 9.0
            for r in range(10): 
                for c in range(16):
                    if (r + c) % 2 == 0:
                        rv = random.random()
                        is_s, hp = (True, 5) if rv < 0.1 else (False, random.choice([1, 2, 3]))
                        self.blocks.add(Block(c*49.5 + 6, r*19 + 50, hp, self.sounds, is_s))
        elif level_num == 2:
            self.ball_speed_modifier, self.current_max_speed = 2.5, 10.5
            for r in range(6):
                for c in range(16):
                    rv = random.random()
                    is_s, hp = (True, 5) if rv < 0.2 else (False, random.choice([1, 1, 2, 3]))
                    self.blocks.add(Block(c*49.5 + 6, r*19 + 50, hp, self.sounds, is_s))
        else:
            self.ball_speed_modifier, self.current_max_speed = 5.0, 13.0
            for r in range(12):
                for c in range(16):
                    if abs(7.5 - c) + abs(5.5 - r) <= 5.5:
                        is_s = random.random() < 0.6
                        hp = 5 if is_s else 4
                        self.blocks.add(Block(c*49.5 + 6, r*19 + 50, hp, self.sounds, is_s))

    def _spawn_ball(self):
        if len(self.balls) < 5:
            speed = self.settings.base_ball_speed + self.ball_speed_modifier
            self.balls.add(Ball(self, speed * random.choice([-1, 1]), -speed, self.current_max_speed))

    def _draw_background(self):
        for y in range(600):
            ratio = y / 600
            r = int(self.settings.bg_color_top[0]*(1-ratio) + self.settings.bg_color_bottom[0]*ratio)
            g = int(self.settings.bg_color_top[1]*(1-ratio) + self.settings.bg_color_bottom[1]*ratio)
            b = int(self.settings.bg_color_top[2]*(1-ratio) + self.settings.bg_color_bottom[2]*ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (800, y))
        pygame.draw.rect(self.screen, self.settings.border_color, (0, 0, 800, 600), 5)

    def _overlay_static(self, title, subtitle):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((10, 10, 20, 210))
        self.screen.blit(overlay, (0,0))
        font_big = pygame.font.SysFont("Arial", 72, bold=True)
        font_small = pygame.font.SysFont("Arial", 32, bold=True)
        t_surf = font_big.render(title, True, (0, 255, 255))
        s_surf = font_small.render(subtitle, True, (200, 200, 200))
        self.screen.blit(t_surf, t_surf.get_rect(center=(400, 230)))
        self.screen.blit(s_surf, s_surf.get_rect(center=(400, 310)))

    def run_game(self):
        while True:
            m_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: self.bat.moving_right = True
                    if event.key == pygame.K_LEFT: self.bat.moving_left = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT: self.bat.moving_right = False
                    if event.key == pygame.K_LEFT: self.bat.moving_left = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "LEVEL_COMPLETE" and self.btn_next.is_clicked(m_pos):
                        self.start_level(self.current_level + 1)
                    if self.state == "GAME_OVER":
                        if self.btn_restart.is_clicked(m_pos): self.start_level(1)
                        if self.btn_quit.is_clicked(m_pos): pygame.quit(); sys.exit()

            self._draw_background()
            
            if self.state == "PLAYING":
                self.bat.update()
                kills = 0
                for ball in self.balls: kills += ball.update(self.bat, self.blocks)
                self.destroyed_count += kills
                
                if self.destroyed_count >= 10:
                    self._spawn_ball()
                    self.destroyed_count -= 10
                
                if not self.blocks: self.state = "LEVEL_COMPLETE"
                if not self.balls: self.state = "GAME_OVER"
                
                self.blocks.draw(self.screen)
                self.bat.draw()
                for b in self.balls:
                    for i, pos in enumerate(b.history):
                        alpha = int(180 * (i / 8))
                        t_surf = pygame.Surface((b.radius*2, b.radius*2), pygame.SRCALPHA)
                        pygame.draw.circle(t_surf, (0, 255, 255, alpha), (b.radius, b.radius), b.radius)
                        self.screen.blit(t_surf, (pos[0]-b.radius, pos[1]-b.radius))
                    self.screen.blit(b.image, b.rect)

            elif self.state == "TRANSITION":
                self.blocks.draw(self.screen)
                self._overlay_static(f"LEVEL {self.current_level}", "Get Ready...")
                if pygame.time.get_ticks() - self.transition_timer > 2000:
                    self.state = "PLAYING"
                    self._spawn_ball()

            elif self.state == "LEVEL_COMPLETE":
                self.blocks.draw(self.screen)
                self._overlay_static("CLEARED!", f"Advance to Level {self.current_level + 1}")
                self.btn_next.update_hover(m_pos)
                self.btn_next.draw(self.screen)

            elif self.state == "GAME_OVER":
                self.blocks.draw(self.screen)
                self._overlay_static("GAME OVER", f"Level reached: {self.current_level}")
                self.btn_restart.update_hover(m_pos)
                self.btn_quit.update_hover(m_pos)
                self.btn_restart.draw(self.screen)
                self.btn_quit.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    BatAndBallGame().run_game()