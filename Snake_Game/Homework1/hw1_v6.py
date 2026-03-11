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

# Direction variables (Moving Right by default)
x_change = BLOCK_SIZE
y_change = 0

snake_body = [(100, 100), (80, 100), (60, 100)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Moving Snake")
clock = pygame.time.Clock()

def spawn_food():
    """Returns a random (x, y) coordinate aligned to the grid."""
    x = random.randrange(0, WIDTH, BLOCK_SIZE)
    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
    return (x, y)

def draw_food(food_pos):
    """Draws a red rectangle representing food."""
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

def main():
    global x_change, y_change
    
    # Initialize the first piece of food
    food_pos = spawn_food()
    
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and y_change == 0:
                    x_change, y_change = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change, y_change = 0, BLOCK_SIZE
                elif event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = BLOCK_SIZE, 0

        # 2. Update Snake Position
        new_head = (snake_body[0][0] + x_change, snake_body[0][1] + y_change)
        snake_body.insert(0, new_head)

        # 3. Collision Logic (The logic you requested)
        if snake_body[0] == food_pos:
            print("Yummy!")
            food_pos = spawn_food()
            # Note: We do NOT pop the tail here, so the snake grows
        else:
            # Remove the tail segment to maintain length during normal movement
            snake_body.pop()

        # --- DRAWING SECTION ---
        screen.fill(BLACK)
        draw_grid()
        draw_food(food_pos)
        draw_fancy_snake()

        pygame.display.flip()
        clock.tick(10) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()