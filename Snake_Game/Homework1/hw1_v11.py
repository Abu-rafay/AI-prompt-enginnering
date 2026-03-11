import pygame
import sys
import random
import os

# --- Constants & Globals ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Colors
BLACK       = (20, 20, 20)
GRAY        = (40, 40, 40)
SNAKE_HEAD  = (50, 255, 50)
SNAKE_BODY  = (34, 139, 34)
SNAKE_SHINE = (100, 255, 100)
WHITE       = (255, 255, 255)
RED         = (255, 50, 50)
GOLD        = (255, 215, 0)
BUTTON_BG   = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)

# Difficulty Settings
START_SPEED = 7   
SPEED_INC   = 0.5 
MAX_SPEED   = 25  

HS_FILE = "snake_highscore.txt"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro: Instant End Page")
clock = pygame.time.Clock()

# --- Fonts ---
font_score = pygame.font.SysFont("Consolas", 20)
font_title = pygame.font.SysFont("Arial", 60, bold=True)
font_btn   = pygame.font.SysFont("Arial", 25, bold=True)

# --- Helper Functions ---

def load_high_score():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            try: return int(f.read())
            except: return 0
    return 0

def save_high_score(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))

def spawn_food():
    return (random.randrange(0, WIDTH, BLOCK_SIZE), 
            random.randrange(0, HEIGHT, BLOCK_SIZE))

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_fancy_snake(snake_list):
    for i, segment in enumerate(snake_list):
        rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
        base_color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(screen, base_color, rect, border_radius=5)
        # Shine
        pygame.draw.rect(screen, SNAKE_SHINE, (segment[0]+3, segment[1]+3, 6, 6), border_radius=2)
        if i == 0: # Eyes
            pygame.draw.circle(screen, WHITE, (rect.centerx - 4, rect.centery - 4), 3)
            pygame.draw.circle(screen, WHITE, (rect.centerx + 4, rect.centery - 4), 3)

def draw_button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON_BG
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    label = font_btn.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect.collidepoint(mouse) and click[0] == 1

def show_stats(score, high_score, current_speed):
    s_txt = font_score.render(f"Score: {score}", True, WHITE)
    h_txt = font_score.render(f"Best: {high_score}", True, GOLD)
    sp_txt = font_score.render(f"Speed: {round(current_speed, 1)}", True, (100, 200, 255))
    screen.blit(s_txt, (10, 10))
    screen.blit(h_txt, (10, 35))
    screen.blit(sp_txt, (WIDTH - 130, 10))

# --- Main Logic ---

def main():
    state = "START"
    high_score = load_high_score()
    
    # Game data
    snake = [(100, 100), (80, 100), (60, 100)]
    x_change, y_change = BLOCK_SIZE, 0
    food_pos = spawn_food()
    game_speed = START_SPEED

    while True:
        screen.fill(BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if state == "START":
            title = font_title.render("SNAKE PRO", True, SNAKE_HEAD)
            screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))
            if draw_button("START GAME", WIDTH//2 - 100, 220, 200, 50):
                snake = [(100, 100), (80, 100), (60, 100)]
                x_change, y_change = BLOCK_SIZE, 0
                game_speed = START_SPEED
                state = "PLAYING"

        elif state == "PLAYING":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and y_change == 0:
                        x_change, y_change = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        x_change, y_change = 0, BLOCK_SIZE
                    elif event.key == pygame.K_LEFT and x_change == 0:
                        x_change, y_change = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change, y_change = BLOCK_SIZE, 0

            new_head = (snake[0][0] + x_change, snake[0][1] + y_change)
            
            # Collision Detection
            if (new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 0 or new_head[1] >= HEIGHT or 
                new_head in snake):
                state = "GAMEOVER"
                current_score = len(snake) - 3
                if current_score > high_score:
                    high_score = current_score
                    save_high_score(high_score)
            else:
                snake.insert(0, new_head)
                if snake[0] == food_pos:
                    food_pos = spawn_food()
                    if game_speed < MAX_SPEED:
                        game_speed += SPEED_INC
                else:
                    snake.pop()

            draw_grid()
            pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE), border_radius=5)
            draw_fancy_snake(snake)
            show_stats(len(snake)-3, high_score, game_speed)

        elif state == "GAMEOVER":
            draw_grid()
            draw_fancy_snake(snake)
            show_stats(len(snake)-3, high_score, game_speed)
            
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0,0))
            
            msg = font_title.render("GAME OVER!", True, RED)
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, 100)))

            # Buttons appear instantly now
            if draw_button("RESTART", WIDTH//2 - 100, 200, 200, 50):
                snake = [(100, 100), (80, 100), (60, 100)]
                x_change, y_change = BLOCK_SIZE, 0
                food_pos = spawn_food()
                game_speed = START_SPEED
                state = "PLAYING"
            
            if draw_button("QUIT", WIDTH//2 - 100, 270, 200, 50):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(game_speed)

if __name__ == "__main__":
    main()