import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report scoring, high scores, levels, and ammo."""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        self.font = pygame.font.SysFont("Impact", 35)
        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_bullets()
        self.prep_ships()

    def prep_score(self):
        score_str = f"Score: {self.stats.score}"
        self.score_image = self.font.render(score_str, True, (50, 50, 50))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left, self.score_rect.top = 20, 20

    def prep_high_score(self):
        high_score_str = f"High Score: {self.stats.high_score} ⭐"
        self.high_score_image = self.font.render(high_score_str, True, (218, 165, 32)) # Gold
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 70

    def prep_level(self):
        level_str = f"Level: {self.settings.game_level} / {self.settings.max_level}"
        self.level_image = self.font.render(level_str, True, (0, 139, 139)) # Cyan
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx
        self.level_rect.top = 20

    def prep_bullets(self):
        bullet_str = f"Bullets: {self.stats.bullets_left}"
        self.bullet_image = self.font.render(bullet_str, True, (255, 69, 0)) # Orange-Red
        self.bullet_rect = self.bullet_image.get_rect()
        self.bullet_rect.right = self.screen_rect.right - 20
        self.bullet_rect.top = 20

    def prep_ships(self):
        self.ships = Group()
        for i in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = pygame.transform.smoothscale(ship.image, (25, 25))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 20 + i * 35
            ship.rect.y = 70
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.bullet_image, self.bullet_rect)
        self.ships.draw(self.screen)