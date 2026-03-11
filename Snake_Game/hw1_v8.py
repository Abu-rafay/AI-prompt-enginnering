import pygame
import sys
import random

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

# Direction variables
x_change = BLOCK_SIZE
y_change = 0

snake_body = [(100, 100), (80, 100), (60, 100)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: Post-Mortem Mode")
clock = pygame.time.Clock()

# Font setup for the Game Over message
font = pygame.font.SysFont("Arial", 50, bold=True)

def spawn_food():
    x = random.randrange(0, WIDTH, BLOCK_SIZE)
    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    return (x, y)

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
        
        # Shine effect
        shine_rect = pygame.Rect(segment[0] + 3, segment[1] + 3, 6, 6)
        pygame.draw.rect(screen, SNAKE_SHINE, shine_rect, border_radius=2)

        if i == 0: # Eyes
            pygame.draw.circle(screen, WHITE, (rect.centerx - 4, rect.centery - 4), 3)
            pygame.draw.circle(screen, WHITE, (rect.centerx + 4, rect.centery - 4), 3)

def show_game_over():
    """Renders the Game Over text in the center of the screen."""
    text_surface = font.render("GAME OVER!", True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    # Draw a dark overlay to make text pop
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150)) 
    screen.blit(overlay, (0,0))
    screen.blit(text_surface, text_rect)

def main():
    global x_change, y_change
    
    food_pos = spawn_food()
    is_dead = False  # Track if the player has lost
    running = True

    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Only allow movement if the snake is alive
            if not is_dead and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_change == 0:
                    x_change, y_change = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change, y_change = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = BLOCK_SIZE, 0

        if not is_dead:
            # 2. Update Position Logic
            new_head = (snake_body[0][0] + x_change, snake_body[0][1] + y_change)

            # 3. Collision Checks
            # Boundary or Self-Collision
            if (new_head[0] < 0 or new_head[0] >= WIDTH or 
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake_body):
                print("Game Over triggered!")
                is_dead = True
            else:
                snake_body.insert(0, new_head)
                if snake_body[0] == food_pos:
                    print("Yummy!")
                    food_pos = spawn_food()
                else:
                    snake_body.pop()

        # --- DRAWING SECTION ---
        screen.fill(BLACK)
        draw_grid()
        draw_food(food_pos)
        draw_fancy_snake()

        if is_dead:
            show_game_over()

        pygame.display.flip()
        clock.tick(10) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()