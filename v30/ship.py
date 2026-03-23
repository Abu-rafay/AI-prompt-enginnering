import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.moving_right = False
        self.moving_left = False
        self.update_appearance()

    def update_appearance(self):
        image_path = 'images/ship.jpeg' if self.settings.game_level == 1 else 'images/ship2.jpg'
        try:
            self.image = pygame.image.load(image_path).convert()
            self.image = pygame.transform.smoothscale(self.image, (100, 100))
        except:
            self.image = pygame.Surface((60, 40))
            self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom = self.screen_rect.bottom - 20 
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)