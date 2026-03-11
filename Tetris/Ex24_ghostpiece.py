import pygame
import sys
import random
import os
import math

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

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

# --- FILE HANDLING ---
save_dir = os.path.expanduser("~/Library/Application Support/PygameTetris")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
HS_FILE = os.path.join(save_dir, "highscore.txt")

# --- AUDIO SYSTEM ---
SOUND_DIR = "assets/sounds"
MOVE_CHANNEL = pygame.mixer.Channel(0)
ROTATE_CHANNEL = pygame.mixer.Channel(1)

def load_sound(file, volume=0.5):
    path = os.path.join(SOUND_DIR, file)
    if os.path.exists(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    return None

sounds = {
    'clear': load_sound('clear.wav', 0.5),
    'landing': load_sound('landing.wav', 0.3),
    'gameover': load_sound('gameover.wav', 0.7),
    'click': load_sound('click.wav', 0.4),
    'move': load_sound('move.wav', 0.6),
    'rotate': load_sound('rotatepiece.wav', 0.7)
}

vol_levels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
current_vol_idx = 2 

def update_music_volume():
    pygame.mixer.music.set_volume(vol_levels[current_vol_idx])

def play_bg_music():
    if not pygame.mixer.music.get_busy():
        music_path = os.path.join(SOUND_DIR, "music.mp3")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            update_music_volume()
            pygame.mixer.music.play(-1)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
GRAY = (50, 50, 50) 
LIGHT_CYAN_GRID = (100, 255, 255)
PANEL_BG = (30, 30, 30)

SHAPES = {
    'I': [[1, 1, 1, 1]], 'O': [[1, 1], [1, 1]], 'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]], 'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]], 'L': [[0, 0, 1], [1, 1, 1]]
}
SHAPE_COLORS = {
    'I': (0, 255, 255), 'O': (255, 255, 0), 'T': (128, 0, 128),
    'S': (0, 255, 0), 'Z': (255, 0, 0), 'J': (0, 0, 255), 'L': (255, 165, 0)
}

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris - Refined Audio")

font = pygame.font.SysFont(None, 80, bold=True)
small_font = pygame.font.SysFont(None, 35)
tiny_font = pygame.font.SysFont(None, 25)
micro_font = pygame.font.SysFont(None, 20)

# --- LOGIC FUNCTIONS ---
def load_high_score():
    if not os.path.exists(HS_FILE): return 0
    try:
        with open(HS_FILE, "r") as f: return int(f.read())
    except: return 0

def save_high_score(new_hs):
    try:
        with open(HS_FILE, "w") as f: f.write(str(new_hs))
    except: pass

def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

def valid_space(shape, grid_x, grid_y, board):
    for r, row in enumerate(shape):
        for c, cell in enumerate(row):
            if cell:
                new_x, new_y = grid_x + c, grid_y + r
                if new_x < 0 or new_x >= 10 or new_y >= 20: return False
                if new_y >= 0 and board[new_y][new_x] != (0,0,0): return False
    return True

def clear_lines(board):
    lines_cleared = 0
    for r in range(len(board) - 1, -1, -1):
        if (0, 0, 0) not in board[r]:
            lines_cleared += 1
            del board[r]
            board.insert(0, [(0, 0, 0) for _ in range(10)])
    if lines_cleared > 0 and sounds['clear']:
        sounds['clear'].play()
    return lines_cleared

# --- RENDERING ---
def draw_fancy_background(surface):
    for i in range(WINDOW_HEIGHT):
        color_val = max(0, 40 - (i // 15))
        pygame.draw.line(surface, (20, 20, color_val + 15), (0, i), (WINDOW_WIDTH, i))

def draw_animated_title(surface, timer):
    bob_y = math.sin(timer * 2) * 10
    title_text = font.render("TETRIS", True, WHITE)
    surface.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 10 + bob_y))

def draw_tetromino(surface, shape_matrix, color, grid_x, grid_y, start_offset_x, start_offset_y, is_ghost=False):
    for row_index, row in enumerate(shape_matrix):
        for col_index, cell in enumerate(row):
            if cell:
                px = start_offset_x + (col_index + grid_x) * BLOCK_SIZE
                py = start_offset_y + (row_index + grid_y) * BLOCK_SIZE
                if is_ghost:
                    # Draw a hollow rectangle for the ghost piece
                    pygame.draw.rect(surface, color, (px, py, BLOCK_SIZE, BLOCK_SIZE), 2)
                else:
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
    global current_vol_idx
    clock = pygame.time.Clock()
    high_score = load_high_score()
    game_state = "START"
    
    start_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, 520, 240, 65)
    pause_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 15, 100, 35)
    music_button_rect = pygame.Rect(WINDOW_WIDTH - 110, 60, 100, 35)
    
    anim_timer = 0
    
    def reset_game():
        board = [[(0,0,0) for _ in range(10)] for _ in range(20)]
        curr_t = random.choice(list(SHAPES.keys()))
        next_t = random.choice(list(SHAPES.keys()))
        play_bg_music()
        return board, curr_t, SHAPES[curr_t], next_t, SHAPES[next_t], 4, 0, 0, 1, 0, "PLAYING", 0

    board, current_type, current_shape, next_type, next_shape, piece_x, piece_y, score, level, total_lines, _, fall_time = reset_game()
    game_state = "START"
    
    base_speed, soft_drop_speed, speed_floor = 600, 60, 100

    while True:
        current_normal_speed = max(base_speed - ((level - 1) * 50), speed_floor)
        dt = clock.get_rawtime()
        anim_timer += dt / 1000
        
        if game_state == "PLAYING": fall_time += dt
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "START" and start_button_rect.collidepoint(event.pos):
                    board, current_type, current_shape, next_type, next_shape, piece_x, piece_y, score, level, total_lines, game_state, fall_time = reset_game()
                elif game_state == "GAME_OVER":
                    board, current_type, current_shape, next_type, next_shape, piece_x, piece_y, score, level, total_lines, game_state, fall_time = reset_game()
                    high_score = load_high_score()

                if music_button_rect.collidepoint(event.pos):
                    if sounds['click']: sounds['click'].play()
                    current_vol_idx = (current_vol_idx + 1) % len(vol_levels)
                    update_music_volume()

                if game_state in ["PLAYING", "PAUSED"] and pause_button_rect.collidepoint(event.pos):
                    game_state = "PAUSED" if game_state == "PLAYING" else "PLAYING"
                    if game_state == "PAUSED": pygame.mixer.music.pause()
                    else: pygame.mixer.music.unpause()

            if game_state == "PLAYING" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_state = "PAUSED"
                    pygame.mixer.music.pause()
                
                if event.key == pygame.K_LEFT:
                    piece_x -= 1
                    if not valid_space(current_shape, piece_x, piece_y, board): piece_x += 1
                    elif sounds['move']: MOVE_CHANNEL.play(sounds['move'])
                if event.key == pygame.K_RIGHT:
                    piece_x += 1
                    if not valid_space(current_shape, piece_x, piece_y, board): piece_x -= 1
                    elif sounds['move']: MOVE_CHANNEL.play(sounds['move'])
                if event.key == pygame.K_UP:
                    new_shape = rotate_shape(current_shape)
                    if valid_space(new_shape, piece_x, piece_y, board): 
                        current_shape = new_shape
                        if sounds['rotate']: ROTATE_CHANNEL.play(sounds['rotate'])
                if event.key == pygame.K_SPACE:
                    while valid_space(current_shape, piece_x, piece_y + 1, board): piece_y += 1
                    fall_time = 1000 

        if game_state == "PLAYING" and fall_time >= (soft_drop_speed if pygame.key.get_pressed()[pygame.K_DOWN] else current_normal_speed):
            piece_y += 1
            if not valid_space(current_shape, piece_x, piece_y, board):
                piece_y -= 1
                if sounds['landing']: sounds['landing'].play()
                for r, row in enumerate(current_shape):
                    for c, cell in enumerate(row):
                        if cell: board[piece_y + r][piece_x + c] = SHAPE_COLORS[current_type]
                
                num_cleared = clear_lines(board)
                if num_cleared > 0:
                    score += {1: 1, 2: 3, 3: 6, 4: 12}.get(num_cleared, num_cleared * 3)
                    total_lines += num_cleared
                    level = (total_lines // 10) + 1
                    if score > high_score:
                        high_score = score; save_high_score(high_score)
                
                current_type, current_shape = next_type, SHAPES[next_type]
                next_type = random.choice(list(SHAPES.keys()))
                next_shape = SHAPES[next_type]
                piece_x, piece_y = 4, 0
                if not valid_space(current_shape, piece_x, piece_y, board):
                    game_state = "GAME_OVER"
                    pygame.mixer.music.fadeout(1000)
                    if sounds['gameover']: sounds['gameover'].play()
            fall_time = 0

        draw_fancy_background(screen)
        draw_animated_title(screen, anim_timer)
        
        if game_state == "START":
            ctrl_box = pygame.Surface((400, 300), pygame.SRCALPHA)
            pygame.draw.rect(ctrl_box, (255, 255, 255, 20), (0, 0, 400, 300), border_radius=15)
            screen.blit(ctrl_box, (WINDOW_WIDTH // 2 - 200, 190))
            controls = [("CONTROLS", LIGHT_CYAN_GRID), ("Left/Right - Move", WHITE), ("Up Arrow - Rotate", WHITE), ("Down Arrow - Soft Drop", WHITE), ("Space Bar - Hard Drop", WHITE), ("P - Pause / Resume", WHITE)]
            for i, (line, color) in enumerate(controls):
                txt = small_font.render(line, True, color) if i == 0 else tiny_font.render(line, True, color)
                screen.blit(txt, (WINDOW_WIDTH // 2 - txt.get_width() // 2, 210 + (i * 40)))
            pulse = math.sin(anim_timer * 4) * 3
            btn_rect = start_button_rect.inflate(pulse, pulse)
            pygame.draw.rect(screen, BRIGHT_GREEN if start_button_rect.collidepoint(pygame.mouse.get_pos()) else GREEN, btn_rect, border_radius=15)
            btn_txt = small_font.render("START GAME", True, BLACK)
            screen.blit(btn_txt, (start_button_rect.centerx - btn_txt.get_width() // 2, start_button_rect.centery - btn_txt.get_height() // 2))

        elif game_state in ["PLAYING", "PAUSED", "GAME_OVER"]:
            pygame.draw.rect(screen, PANEL_BG, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT))
            pygame.draw.rect(screen, LIGHT_CYAN_GRID, (SIDE_PANEL_X, Y_OFFSET, SIDE_PANEL_WIDTH, PLAY_HEIGHT), 1)
            panel_center = SIDE_PANEL_X + (SIDE_PANEL_WIDTH // 2)
            next_label = small_font.render("NEXT", True, WHITE)
            screen.blit(next_label, (panel_center - next_label.get_width() // 2, Y_OFFSET + 10))
            draw_tetromino(screen, next_shape, SHAPE_COLORS[next_type], 1, 1.5, SIDE_PANEL_X, Y_OFFSET)
            
            stats = [("SCORE", score), ("BEST", high_score), ("LEVEL", level), ("LINES", total_lines)]
            for i, (label, val) in enumerate(stats):
                y_pos = Y_OFFSET + 180 + (i * 90)
                screen.blit(tiny_font.render(label, True, WHITE), (panel_center - tiny_font.size(label)[0]//2, y_pos))
                screen.blit(small_font.render(str(val), True, LIGHT_CYAN_GRID), (panel_center - small_font.size(str(val))[0]//2, y_pos + 22))

            pygame.draw.rect(screen, BLACK, (X_OFFSET, Y_OFFSET, PLAY_WIDTH, PLAY_HEIGHT))
            draw_board(screen, board)
            
            if game_state in ["PLAYING", "PAUSED"]:
                # --- GHOST PIECE LOGIC ---
                ghost_y = piece_y
                # Find the lowest valid space for the ghost piece
                while valid_space(current_shape, piece_x, ghost_y + 1, board):
                    ghost_y += 1
                
                # Draw Ghost first (so active piece is on top)
                draw_tetromino(screen, current_shape, SHAPE_COLORS[current_type], piece_x, ghost_y, X_OFFSET, Y_OFFSET, is_ghost=True)
                # Draw Active Piece
                draw_tetromino(screen, current_shape, SHAPE_COLORS[current_type], piece_x, piece_y, X_OFFSET, Y_OFFSET)
            
            draw_grid_lines(screen)

            ui_buttons = [
                (pause_button_rect, "RESUME" if game_state == "PAUSED" else "PAUSE"),
                (music_button_rect, f"MUSIC: {int(vol_levels[current_vol_idx]*100)}%")
            ]
            for rect, text in ui_buttons:
                hover = rect.collidepoint(pygame.mouse.get_pos())
                pygame.draw.rect(screen, GRAY if hover else PANEL_BG, rect, border_radius=8)
                pygame.draw.rect(screen, LIGHT_CYAN_GRID, rect, 1, border_radius=8)
                btn_lbl = micro_font.render(text, True, WHITE)
                screen.blit(btn_lbl, (rect.centerx - btn_lbl.get_width()//2, rect.centery - btn_lbl.get_height()//2))

            if game_state == "PAUSED":
                overlay = pygame.Surface((PLAY_WIDTH, PLAY_HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (X_OFFSET, Y_OFFSET))
                screen.blit(font.render("PAUSED", True, WHITE), (X_OFFSET + 30, Y_OFFSET + 250))

            if game_state == "GAME_OVER":
                overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA); overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                go_txt = font.render("GAME OVER", True, RED)
                restart_txt = small_font.render("Click anywhere to Restart", True, WHITE)
                screen.blit(go_txt, (WINDOW_WIDTH // 2 - go_txt.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
                screen.blit(restart_txt, (WINDOW_WIDTH // 2 - restart_txt.get_width() // 2, WINDOW_HEIGHT // 2 + 30))

        pygame.display.flip()

if __name__ == "__main__":
    main()