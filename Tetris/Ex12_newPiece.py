import pygame
import sys
import random

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
pygame.display.set_caption("Tetris - Next Piece & Gravity")
font = pygame.font.SysFont(None, 40) # Slightly smaller font for labels

board = [[(0,0,0) for _ in range(10)] for _ in range(20)]

def valid_space(shape_type, grid_x, grid_y, board):
    shape = SHAPES[shape_type]
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell:
                new_x = grid_x + c
                new_y = grid_y + r
                if new_x < 0 or new_x >= 10 or new_y >= 20:
                    return False
                if new_y >= 0 and board[new_y][new_x] != (0,0,0):
                    return False
    return True

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

def draw_board(surface, board):
    for r in range(20):
        for c in range(10):
            if board[r][c] != (0,0,0):
                px = X_OFFSET + c * BLOCK_SIZE
                py = Y_OFFSET + r * BLOCK_SIZE
                pygame.draw.rect(surface, board[r][c], (px, py, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(surface, BLACK, (px, py, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_grid_lines(surface):
    for i in range(0, PLAY_HEIGHT + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN_GRID, (X_OFFSET, Y_OFFSET + i), (X_OFFSET + PLAY_WIDTH, Y_OFFSET + i))
    for j in range(0, PLAY_WIDTH + 1, BLOCK_SIZE):
        pygame.draw.line(surface, LIGHT_CYAN_GRID, (X_OFFSET + j, Y_OFFSET), (X_OFFSET + j, Y_OFFSET + PLAY_HEIGHT))

def main():
    clock = pygame.time.Clock()
    
    # Random Piece Initialization
    current_piece = random.choice(list(SHAPES.keys()))
    next_piece = random.choice(list(SHAPES.keys()))
    piece_x, piece_y = 4, 0
    
    # Adjusted Gravity
    fall_time = 0
    fall_speed = 600 # Faster base speed: 600ms

    while True:
        dt = clock.get_rawtime()
        fall_time += dt
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece_x -= 1
                    if not valid_space(current_piece, piece_x, piece_y, board):
                        piece_x += 1
                if event.key == pygame.K_RIGHT:
                    piece_x += 1
                    if not valid_space(current_piece, piece_x, piece_y, board):
                        piece_x -= 1

        # Gravity Logic
        if fall_time >= fall_speed:
            piece_y += 1
            if not valid_space(current_piece, piece_x, piece_y, board):
                piece_y -= 1
                # Lock current piece
                shape = SHAPES[current_piece]
                color = SHAPE_COLORS[current_piece]
                for r, row in enumerate(shape):
                    for c, cell in enumerate(row):
                        if cell:
                            board[piece_y + r][piece_x + c] = color
                
                # Handover: Next becomes Current
                current_piece = next_piece
                next_piece = random.choice(list(SHAPES.keys()))
                piece_x, piece_y = 4, 0
                
            fall_time = 0

        screen.fill(BLACK)
        
        # 1. Labels
        label = font.render('NEXT', True, WHITE)
        screen.blit(label, (SIDE_PANEL_X + 45, Y_OFFSET + 20))
        
        # 2. Side Panel Preview
        pygame.draw.rect(screen, PANEL_BG, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(screen, LIGHT_CYAN_GRID, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
        
        # Draw Preview Piece (Centered in side panel)
        draw_tetromino(screen, next_piece, 1, 3, SIDE_PANEL_X, Y_OFFSET)
        
        # 3. Main Play Area
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        draw_board(screen, board)
        draw_tetromino(screen, current_piece, piece_x, piece_y, X_OFFSET, Y_OFFSET)
        
        draw_grid_lines(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()