import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 60
        self.button_color = (0, 102, 204)
        self.hover_color = (0, 204, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Impact", 48)
        self.border_radius = 15

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)
        self.is_hovered = False

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw_button(self):
        color = self.hover_color if self.is_hovered else self.button_color
        pygame.draw.rect(self.screen, (50, 50, 50), self.rect.move(4, 4), border_radius=self.border_radius)
        pygame.draw.rect(self.screen, color, self.rect, border_radius=self.border_radius)
        self.screen.blit(self.msg_image, self.msg_image_rect)