import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# Grid Position (Unchanged)
X_OFFSET = 200
Y_OFFSET = 70

# Side Panel Calculations with 20px margins
MARGIN = 20
GAP = 20
SIDE_PANEL_X = MARGIN # Starts 20px from the left border
# Width = 200 (grid start) - 20 (gap) - 20 (left margin) = 160
SIDE_PANEL_WIDTH = X_OFFSET - GAP - MARGIN 

# Colors
BLACK = (0, 0, 0)
LIGHT_CYAN = (100, 255, 255)
WHITE = (255, 255, 255)
PANEL_COLOR = (30, 30, 30) # Dark gray

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris - Centered Layout")

# Font setup
font = pygame.font.SysFont(None, 60)

def draw_grid(surface):
    """Draws light-colored grid lines over the play area."""
    for i in range(0, PLAY_HEIGHT + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN, 
                         (X_OFFSET, Y_OFFSET + i), 
                         (X_OFFSET + PLAY_WIDTH, Y_OFFSET + i))
    for j in range(0, PLAY_WIDTH + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN, 
                         (X_OFFSET + j, Y_OFFSET), 
                         (X_OFFSET + j, Y_OFFSET + PLAY_HEIGHT))

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background (Window border area)
        screen.fill(BLACK)
        
        # 1. Draw the "Tetris" Heading
        title_surface = font.render('TETRIS', True, WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, Y_OFFSET // 2))
        screen.blit(title_surface, title_rect)
        
        # 2. Draw the Side Panel (160px wide, with 20px padding on both sides)
        pygame.draw.rect(screen, PANEL_COLOR, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(screen, LIGHT_CYAN, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
        
        # 3. Draw the main play area background
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        
        # 4. Draw the light grid lines
        draw_grid(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()