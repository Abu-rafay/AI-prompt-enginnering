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

# Tetromino Definitions
# Each shape is a 2D list. '0' is empty, '1' is a filled block.
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], 
          [1, 1]],
    'T': [[0, 1, 0], 
          [1, 1, 1]],
    'S': [[0, 1, 1], 
          [1, 1, 0]],
    'Z': [[1, 1, 0], 
          [0, 1, 1]],
    'J': [[1, 0, 0], 
          [1, 1, 1]],
    'L': [[0, 0, 1], 
          [1, 1, 1]]
}

# Distinct Colors for each shape
SHAPE_COLORS = {
    'I': (0, 255, 255),   # Cyan
    'O': (255, 255, 0),   # Yellow
    'T': (128, 0, 128),   # Purple
    'S': (0, 255, 0),     # Green
    'Z': (255, 0, 0),     # Red
    'J': (0, 0, 255),     # Blue
    'L': (255, 165, 0)    # Orange
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris - Tetromino Testing")
font = pygame.font.SysFont(None, 60)

def draw_tetromino(surface, shape_type, grid_x, grid_y, start_offset_x, start_offset_y):
    """
    surface: Screen to draw on
    shape_type: Key from SHAPES dictionary (e.g., 'T')
    grid_x/y: The column/row in the 10x20 grid to start drawing
    start_offset_x/y: The pixel X/Y of the grid container (X_OFFSET, Y_OFFSET)
    """
    shape = SHAPES[shape_type]
    color = SHAPE_COLORS[shape_type]
    
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                # Calculate pixel position
                px = start_offset_x + (grid_x + col_index) * BLOCK_SIZE
                py = start_offset_y + (grid_y + row_index) * BLOCK_SIZE
                
                # Draw block
                pygame.draw.rect(surface, color, (px, py, BLOCK_SIZE, BLOCK_SIZE))
                # Draw border for block definition
                pygame.draw.rect(surface, BLACK, (px, py, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_grid_lines(surface):
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
        
        # 1. Heading
        title_surface = font.render('TETRIS', True, WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, Y_OFFSET // 2))
        screen.blit(title_surface, title_rect)
        
        # 2. Side Panel
        pygame.draw.rect(screen, PANEL_BG, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(screen, LIGHT_CYAN_GRID, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
        
        # TEST: Draw 'O' and 'I' in the side panel
        draw_tetromino(screen, 'O', 1, 1, SIDE_PANEL_X, Y_OFFSET)
        draw_tetromino(screen, 'I', 0, 4, SIDE_PANEL_X, Y_OFFSET)
        
        # 3. Main Play Area
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        
        # TEST: Draw 'T' at the top middle of the grid (Column 4, Row 0)
        draw_tetromino(screen, 'T', 4, 0, X_OFFSET, Y_OFFSET)
        
        # Draw grid lines on top
        draw_grid_lines(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()