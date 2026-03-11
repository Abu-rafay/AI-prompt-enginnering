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

# Movement Setup
x_change = BLOCK_SIZE
y_change = 0
snake_body = [(100, 100), (80, 100), (60, 100)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: High Score Edition")
clock = pygame.time.Clock()

# Font setup
score_font = pygame.font.SysFont("Consolas", 25)
game_over_font = pygame.font.SysFont("Arial", 50, bold=True)

# --- High Score Logic ---
HS_FILE = "high_score.txt"

def load_high_score():
    if os.path.exists(HS_FILE):
        with open(HS_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))

def show_score(current_score, high_score):
    """Displays current score and high score in the top-left."""
    score_surf = score_font.render(f"Score: {current_score}", True, WHITE)
    high_surf = score_font.render(f"High Score: {high_score}", True, GOLD)
    screen.blit(score_surf, (10, 10))
    screen.blit(high_surf, (10, 35))

def spawn_food():
    return (random.randrange(0, WIDTH, BLOCK_SIZE), 
            random.randrange(0, HEIGHT, BLOCK_SIZE))

def draw_food(food_pos):
    rect = pygame.Rect(food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, RED, rect, border_radius=5)

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_fancy_snake():
    for i, segment in enumerate(snake_body):
        rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
        base_color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(screen, base_color, rect, border_radius=5)
        if i == 0: # Eyes
            pygame.draw.circle(screen, WHITE, (rect.centerx - 4, rect.centery - 4), 3)
            pygame.draw.circle(screen, WHITE, (rect.centerx + 4, rect.centery - 4), 3)

def main():
    global x_change, y_change
    
    food_pos = spawn_food()
    high_score = load_high_score()
    is_dead = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not is_dead and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_change == 0:
                    x_change, y_change = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change, y_change = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = BLOCK_SIZE, 0

        current_score = len(snake_body) - 3

        if not is_dead:
            new_head = (snake_body[0][0] + x_change, snake_body[0][1] + y_change)

            # Collision Checks
            if (new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 0 or new_head[1] >= HEIGHT or 
                new_head in snake_body):
                is_dead = True
                # Check if we beat the high score upon death
                if current_score > high_score:
                    high_score = current_score
                    save_high_score(high_score)
            else:
                snake_body.insert(0, new_head)
                if snake_body[0] == food_pos:
                    food_pos = spawn_food()
                else:
                    snake_body.pop()

        # --- DRAWING ---
        screen.fill(BLACK)
        draw_grid()
        show_score(current_score, high_score) # Called after background
        draw_food(food_pos)
        draw_fancy_snake()

        if is_dead:
            msg = game_over_font.render("GAME OVER!", True, WHITE)
            screen.blit(msg, (WIDTH//2 - 100, HEIGHT//2 - 25))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()