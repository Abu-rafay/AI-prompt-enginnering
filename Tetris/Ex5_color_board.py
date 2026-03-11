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
X_OFFSET = 200
Y_OFFSET = 70
MARGIN = 20
GAP = 20
SIDE_PANEL_X = MARGIN
SIDE_PANEL_WIDTH = X_OFFSET - GAP - MARGIN 

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_CYAN_GRID = (100, 255, 255)
PANEL_BG = (30, 30, 30)

# Block Colors Map
# 0: Empty, 1: Cyan, 2: Red, 3: Yellow
COLORS = {
    1: (0, 255, 255),   # Cyan
    2: (255, 0, 0),     # Red
    3: (255, 255, 0)    # Yellow
}

# 1. Create a 2D Array for the Grid (20 rows x 10 columns)
# Initializing with 0s
grid = [[0 for _ in range(10)] for _ in range(20)]

# 2. Manually insert test blocks
# Format: grid[row][column] = color_index
grid[19][0] = 1  # Bottom-left Cyan
grid[19][1] = 1
grid[18][5] = 2  # Middle-ish Red
grid[17][5] = 2
grid[5][3] = 3   # High-up Yellow

# For the side panel, we'll create a smaller 2D array (e.g., 4x4)
side_grid = [
    [0, 2, 0, 0],
    [1, 1, 1, 0],
    [0, 0, 3, 3],
    [0, 0, 3, 3]
]

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris - Manual Block Test")
font = pygame.font.SysFont(None, 60)

def draw_blocks(surface, data, start_x, start_y):
    """Generic function to draw blocks from a 2D array."""
    for row_index, row in enumerate(data):
        for col_index, val in enumerate(row):
            if val != 0:
                color = COLORS[val]
                # Calculate pixel position
                block_x = start_x + (col_index * BLOCK_SIZE)
                block_y = start_y + (row_index * BLOCK_SIZE)
                
                # Draw the colored block
                pygame.draw.rect(surface, color, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))
                # Draw a small border around each block for definition
                pygame.draw.rect(surface, BLACK, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_grid_lines(surface):
    """Draws the cyan grid lines."""
    for i in range(0, PLAY_HEIGHT + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN_GRID, (X_OFFSET, Y_OFFSET + i), (X_OFFSET + PLAY_WIDTH, Y_OFFSET + i))
    for j in range(0, PLAY_WIDTH + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN_GRID, (X_OFFSET + j, Y_OFFSET), (X_OFFSET + j, Y_OFFSET + PLAY_HEIGHT))

def main():
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        
        # Heading
        title_surface = font.render('TETRIS', True, WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, Y_OFFSET // 2))
        screen.blit(title_surface, title_rect)
        
        # Side Panel
        pygame.draw.rect(screen, PANEL_BG, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(screen, LIGHT_CYAN_GRID, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
        # Draw test blocks in side panel (using same colors)
        draw_blocks(screen, side_grid, SIDE_PANEL_X + 20, Y_OFFSET + 50)
        
        # Main Grid Area
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        
        # Draw the manual blocks from our 2D array
        draw_blocks(screen, grid, X_OFFSET, Y_OFFSET)
        
        # Draw grid lines on top
        draw_grid_lines(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()