import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BLOCK_SIZE = 30
PLAY_WIDTH = 300
PLAY_HEIGHT = 600

# NEW WINDOW SIZE
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700

# Offsets for positioning the grid
X_OFFSET = 200
Y_OFFSET = 70

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("600x700 Centered Grid")

# Colors
GRAY = (128, 128, 128)
GRID_COLOR = (100, 100, 100) 
BLACK = (0, 0, 0)

def draw_grid(surface):
    """Draws grid lines starting from the offsets."""
    # Draw horizontal lines
    for i in range(0, PLAY_HEIGHT + 1, BLOCK_SIZE):
        pygame.draw.line(surface, GRID_COLOR, 
                         (X_OFFSET, Y_OFFSET + i), 
                         (X_OFFSET + PLAY_WIDTH, Y_OFFSET + i))
    
    # Draw vertical lines
    for j in range(0, PLAY_WIDTH + 1, BLOCK_SIZE):
        pygame.draw.line(surface, GRID_COLOR, 
                         (X_OFFSET + j, Y_OFFSET), 
                         (X_OFFSET + j, Y_OFFSET + PLAY_HEIGHT))

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill background with gray
        screen.fill(GRAY)
        
        # Draw the play area background at the offset
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        
        # Draw grid lines over the black area
        draw_grid(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()