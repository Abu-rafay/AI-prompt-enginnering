import pygame
import sys
import random
import os

# --- Constants ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Colors
BLACK, GRAY = (20, 20, 20), (40, 40, 40)
SNAKE_HEAD, SNAKE_BODY = (50, 255, 50), (34, 139, 34)
SNAKE_SHINE = (100, 255, 100)
WHITE, RED, GOLD = (255, 255, 255), (255, 50, 50), (255, 215, 0)
WALL_COLOR = (120, 120, 120)
BUTTON_BG, BUTTON_HOVER = (50, 50, 50), (80, 80, 80)

HS_FILE = "snake_highscore.txt"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Pro: Modified Challenges")
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

def spawn_food(snake, obstacles):
    while True:
        x = random.randrange(0, WIDTH, BLOCK_SIZE)
        y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        if (x, y) not in snake and (x, y) not in obstacles:
            return (x, y)

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_fancy_snake(snake_list):
    for i, segment in enumerate(snake_list):
        rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(screen, color, rect, border_radius=5)
        pygame.draw.rect(screen, SNAKE_SHINE, (segment[0]+3, segment[1]+3, 6, 6), border_radius=2)
        if i == 0:
            pygame.draw.circle(screen, WHITE, (rect.centerx - 4, rect.centery - 4), 3)
            pygame.draw.circle(screen, WHITE, (rect.centerx + 4, rect.centery - 4), 3)

def draw_button(text, x, y, w, h, active_color=BUTTON_BG):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    color = BUTTON_HOVER if rect.collidepoint(mouse) else active_color
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    label = font_btn.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=rect.center))
    return rect.collidepoint(mouse) and click[0] == 1

def main():
    state = "START"
    high_score = load_high_score()
    
    snake = []
    x_change, y_change = BLOCK_SIZE, 0
    obstacles = []
    current_speed = 7
    speed_inc = 1.0
    food_pos = (0,0)

    while True:
        screen.fill(BLACK)
        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if state == "START":
            title = font_title.render("SNAKE PRO", True, SNAKE_HEAD)
            screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))
            
            # Button Logic
            e_p = draw_button("[E] EASY", WIDTH//2 - 100, 160, 200, 45, (34, 139, 34)) or keys[pygame.K_e]
            m_p = draw_button("[M] MEDIUM", WIDTH//2 - 100, 220, 200, 45, (218, 165, 32)) or keys[pygame.K_m]
            h_p = draw_button("[H] HARD", WIDTH//2 - 100, 280, 200, 45, (178, 34, 34)) or keys[pygame.K_h]

            if e_p or m_p or h_p:
                snake = [(100, 100), (80, 100), (60, 100)]
                x_change, y_change = BLOCK_SIZE, 0
                obstacles = []

                if e_p:
                    current_speed, speed_inc = 7, 0.5 # Updated: 0.5 increment
                elif m_p:
                    current_speed, speed_inc = 8, 1.0
                    for i in range(10, 20):
                        obstacles.extend([(i*BLOCK_SIZE, 60), (i*BLOCK_SIZE, 200), (i*BLOCK_SIZE, 340)])
                elif h_p:
                    current_speed, speed_inc = 9, 1.0
                    # Updated: 15 Random blocks
                    while len(obstacles) < 15:
                        wx = random.randrange(0, WIDTH, BLOCK_SIZE)
                        wy = random.randrange(0, HEIGHT, BLOCK_SIZE)
                        # Ensure walls don't spawn on snake body
                        if (wx, wy) not in snake:
                            obstacles.append((wx, wy))
                
                food_pos = spawn_food(snake, obstacles)
                state = "PLAYING"

        elif state == "PLAYING":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and y_change != BLOCK_SIZE:
                        x_change, y_change = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and y_change != -BLOCK_SIZE:
                        x_change, y_change = 0, BLOCK_SIZE
                    elif event.key == pygame.K_LEFT and x_change != BLOCK_SIZE:
                        x_change, y_change = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and x_change != -BLOCK_SIZE:
                        x_change, y_change = BLOCK_SIZE, 0

            new_head = (snake[0][0] + x_change, snake[0][1] + y_change)
            
            if (new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 0 or new_head[1] >= HEIGHT or 
                new_head in snake or new_head in obstacles):
                state = "GAMEOVER"
                if (len(snake)-3) > high_score:
                    high_score = len(snake)-3
                    save_high_score(high_score)
            else:
                snake.insert(0, new_head)
                if snake[0] == food_pos:
                    food_pos = spawn_food(snake, obstacles)
                    current_speed += speed_inc
                else:
                    snake.pop()

            draw_grid()
            for wall in obstacles:
                pygame.draw.rect(screen, WALL_COLOR, (wall[0], wall[1], BLOCK_SIZE, BLOCK_SIZE), border_radius=3)
            pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE), border_radius=5)
            draw_fancy_snake(snake)
            screen.blit(font_score.render(f"Score: {len(snake)-3}", True, WHITE), (10, 10))
            screen.blit(font_score.render(f"Best: {high_score}", True, GOLD), (10, 35))

        elif state == "GAMEOVER":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)); screen.blit(overlay, (0,0))
            msg = font_title.render("GAME OVER!", True, RED)
            screen.blit(msg, msg.get_rect(center=(WIDTH//2, 100)))

            if draw_button("[R] RESTART", WIDTH//2 - 100, 200, 200, 50) or keys[pygame.K_r]:
                state = "START"
            if draw_button("[Q] QUIT", WIDTH//2 - 100, 270, 200, 50) or keys[pygame.K_q]:
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(current_speed)

if __name__ == "__main__":
    main()