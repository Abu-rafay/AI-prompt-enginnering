import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        image_path = 'images/alien.jpg' if self.settings.game_level == 1 else 'images/alien2.jpg'
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (80, 80))
        except:
            self.image = pygame.Surface((70, 70))
            self.image.fill((0, 255, 0)) 
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)
        self.target_y = 0.0

    def check_edges(self):
        return self.rect.right >= self.screen.get_rect().right or self.rect.left <= 0

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x