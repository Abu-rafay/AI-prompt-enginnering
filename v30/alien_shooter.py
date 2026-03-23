import pygame
from pygame.sprite import Group
from setting import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_function as gf

class AlienShooter:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen_width = self.settings.screen_width
        self.screen = pygame.display.set_mode((self.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Shooter")
        self.clock = pygame.time.Clock()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets, self.aliens = Group(), Group()
        self.play_button = Button(self, "PLAY")

    def run_game(self):
        while True:
            gf.check_events(self)
            if self.stats.game_active:
                self.ship.update()
                gf.update_bullets(self) 
                gf.update_aliens(self)
            gf.update_screen(self)
            self.clock.tick(self.settings.fps)

if __name__ == "__main__":
    ai = AlienShooter()
    ai.run_game()