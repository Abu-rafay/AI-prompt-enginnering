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
RED = (255, 0, 0)
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
pygame.display.set_caption("Tetris - Game Over State")

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 35)
tiny_font = pygame.font.SysFont(None, 25)

board = [[(0,0,0) for _ in range(10)] for _ in range(20)]

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def valid_space(shape, grid_x, grid_y, board):
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

def clear_lines(board):
    lines_cleared = 0
    for r in range(len(board) - 1, -1, -1):
        if (0, 0, 0) not in board[r]:
            lines_cleared += 1
            del board[r]
            board.insert(0, [(0, 0, 0) for _ in range(10)])
    return lines_cleared

def draw_tetromino(surface, shape_matrix, color, grid_x, grid_y, start_offset_x, start_offset_y):
    for row_index, row in enumerate(shape_matrix):
        for col_index, cell in enumerate(row):
            if cell:
                px = start_offset_x + (col_index + grid_x) * BLOCK_SIZE
                py = start_offset_y + (row_index + grid_y) * BLOCK_SIZE
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
    
    current_type = random.choice(list(SHAPES.keys()))
    current_shape = SHAPES[current_type]
    next_type = random.choice(list(SHAPES.keys()))
    next_shape = SHAPES[next_type]
    
    piece_x, piece_y = 4, 0
    fall_time = 0
    
    score = 0
    level = 1
    total_lines = 0
    game_over = False
    
    base_speed = 600
    soft_drop_speed = 60
    speed_floor = 100

    while True:
        current_normal_speed = max(base_speed - ((level - 1) * 50), speed_floor)
        dt = clock.get_rawtime()
        
        # Only accumulate time if game is not over
        if not game_over:
            fall_time += dt
        
        clock.tick()

        keys = pygame.key.get_pressed()
        fall_speed = soft_drop_speed if keys[pygame.K_DOWN] else current_normal_speed
        
        was_hard_drop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Disable input if game is over
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        piece_x -= 1
                        if not valid_space(current_shape, piece_x, piece_y, board):
                            piece_x += 1
                    if event.key == pygame.K_RIGHT:
                        piece_x += 1
                        if not valid_space(current_shape, piece_x, piece_y, board):
                            piece_x -= 1
                    if event.key == pygame.K_UP:
                        new_shape = rotate_shape(current_shape)
                        if valid_space(new_shape, piece_x, piece_y, board):
                            current_shape = new_shape
                    if event.key == pygame.K_SPACE:
                        while valid_space(current_shape, piece_x, piece_y + 1, board):
                            piece_y += 1
                        was_hard_drop = True
                        fall_time = fall_speed 

        # Gravity & Locking
        if not game_over and fall_time >= fall_speed:
            piece_y += 1
            if not valid_space(current_shape, piece_x, piece_y, board):
                piece_y -= 1
                for r, row in enumerate(current_shape):
                    for c, cell in enumerate(row):
                        if cell:
                            board[piece_y + r][piece_x + c] = SHAPE_COLORS[current_type]
                
                num_cleared = clear_lines(board)
                if num_cleared > 0:
                    turn_points = 2**(num_cleared - 1)
                    if was_hard_drop: turn_points *= 2
                    score += turn_points
                    total_lines += num_cleared
                    level = (total_lines // 10) + 1
                
                # Check for Game Over upon spawning next piece
                current_type = next_type
                current_shape = SHAPES[current_type]
                next_type = random.choice(list(SHAPES.keys()))
                next_shape = SHAPES[next_type]
                piece_x, piece_y = 4, 0
                
                if not valid_space(current_shape, piece_x, piece_y, board):
                    game_over = True
                
                was_hard_drop = False
            fall_time = 0

        # Rendering
        screen.fill(BLACK)
        
        # Side Panel
        pygame.draw.rect(screen, PANEL_BG, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
        pygame.draw.rect(screen, LIGHT_CYAN_GRID, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
        panel_center = SIDE_PANEL_X + (SIDE_PANEL_WIDTH // 2)

        next_label = small_font.render("NEXT", True, WHITE)
        screen.blit(next_label, (panel_center - next_label.get_width() // 2, Y_OFFSET + 20))
        draw_tetromino(screen, next_shape, SHAPE_COLORS[next_type], 1, 2, SIDE_PANEL_X, Y_OFFSET)
        
        # Stats
        for i, (label, val) in enumerate([("SCORE", score), ("LEVEL", level), ("LINES", total_lines)]):
            lbl = tiny_font.render(label, True, WHITE)
            v_lbl = small_font.render(str(val), True, LIGHT_CYAN_GRID)
            screen.blit(lbl, (panel_center - lbl.get_width() // 2, Y_OFFSET + 220 + (i * 100)))
            screen.blit(v_lbl, (panel_center - v_lbl.get_width() // 2, Y_OFFSET + 245 + (i * 100)))

        # Main Board
        pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
        draw_board(screen, board)
        if not game_over:
            draw_tetromino(screen, current_shape, SHAPE_COLORS[current_type], piece_x, piece_y, X_OFFSET, Y_OFFSET)
        
        draw_grid_lines(screen)

        # Game Over Overlay
        if game_over:
            # Semi-transparent darkened effect
            overlay = pygame.Surface((PLAY_WIDTH, PLAY_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (X_OFFSET, Y_OFFSET))
            
            msg = font.render("GAME OVER", True, RED)
            screen.blit(msg, (X_OFFSET + (PLAY_WIDTH // 2 - msg.get_width() // 2), Y_OFFSET + (PLAY_HEIGHT // 2 - msg.get_height() // 2)))

        pygame.display.flip()

if __name__ == "__main__":
    main()