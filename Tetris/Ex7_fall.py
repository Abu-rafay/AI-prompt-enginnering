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
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

SHAPE_COLORS = {
    'I': (0, 255, 255), 'O': (255, 255, 0), 'T': (128, 0, 128),
    'S': (0, 255, 0), 'Z': (255, 0, 0), 'J': (0, 0, 255), 'L': (255, 165, 0)
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris - Gravity Implementation")
font = pygame.font.SysFont(None, 60)

def draw_tetromino(surface, shape_type, grid_x, grid_y, start_offset_x, start_offset_y):
    shape = SHAPES[shape_type]
    color = SHAPE_COLORS[shape_type]
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                px = start_offset_x + (grid_x + col_index) * BLOCK_SIZE
                py = start_offset_y + (grid_y + row_index) * BLOCK_SIZE
                pygame.draw.rect(surface, color, (px, py, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, BLACK, (px, py, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_grid_lines(surface):
    for i in range(0, PLAY_HEIGHT + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN_GRID, (X_OFFSET, Y_OFFSET + i), (X_OFFSET + PLAY_WIDTH, Y_OFFSET + i))
    for j in range(0, PLAY_WIDTH + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN_GRID, (X_OFFSET + j, Y_OFFSET), (X_OFFSET + j, Y_OFFSET + PLAY_HEIGHT))

def main():
    clock = pygame.time.Clock()
    
    # Gravity Variables
    current_piece = 'T'
    piece_x, piece_y = 4, 0  # Starting position (Middle-Top)
    
    fall_time = 0
    fall_speed = 1000 # 1000ms = 1 second drop interval

    while True:
        # Get the time passed since the last tick
        dt = clock.get_rawtime()
        fall_time += dt
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gravity Logic: Check if it's time to drop the piece
        if fall_time >= fall_speed:
            piece_y += 1
            fall_time = 0 # Reset timer

            # Reset piece to top if it falls off the board (Looping for testing)
            if piece_y > 18: 
                piece_y = 0

        screen.fill(BLACK)
        
        # Heading
        title_surface = font.render('TETRIS', True, WHITE)
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, Y_OFFSET // 2))
        screen.blit(title_surface, title_rect)
        
        # Side Panel
        pygame.draw.rect(screen, PANEL_BG, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(screen, LIGHT_CYAN_GRID, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
        
        # Main Play Area
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        
        # Draw the falling piece
        draw_tetromino(screen, current_piece, piece_x, piece_y, X_OFFSET, Y_OFFSET)
        
        draw_grid_lines(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
    