import pygame
import sys

# --- Constants & Globals ---
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20

# Color Palette
BLACK       = (20, 20, 20)      # Slightly lighter black for better contrast
GRAY        = (40, 40, 40)      # Subtle grid lines
SNAKE_HEAD  = (50, 255, 50)     # Bright Neon Green
SNAKE_BODY  = (34, 139, 34)     # Forest Green
SNAKE_SHINE = (100, 255, 100)    # Highlight color
WHITE       = (255, 255, 255)

snake_body = [(100, 100), (80, 100), (60, 100)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Snake Design")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def draw_fancy_snake():
    for i, segment in enumerate(snake_body):
        # Create the main rectangle
        rect = pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)
        
        # 1. Pick color: Head is brighter than the body
        base_color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        
        # 2. Draw the main body with rounded corners (border_radius=5)
        pygame.draw.rect(screen, base_color, rect, border_radius=5)
        
        # 3. Add a "Shine" (a smaller, lighter rect inside for depth)
        shine_rect = pygame.Rect(segment[0] + 3, segment[1] + 3, 6, 6)
        pygame.draw.rect(screen, SNAKE_SHINE, shine_rect, border_radius=2)

        # 4. Add Eyes only to the head (the first segment)
        if i == 0:
            # Left Eye
            pygame.draw.circle(screen, WHITE, (rect.centerx - 4, rect.centery - 4), 3)
            # Right Eye
            pygame.draw.circle(screen, WHITE, (rect.centerx + 4, rect.centery - 4), 3)
            # Pupils
            pygame.draw.circle(screen, (0, 0, 0), (rect.centerx - 4, rect.centery - 4), 1)
            pygame.draw.circle(screen, (0, 0, 0), (rect.centerx + 4, rect.centery - 4), 1)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- DRAWING SECTION ---
        screen.fill(BLACK)
        draw_grid()

        # Call our new fancy drawing function
        draw_fancy_snake()

        pygame.display.flip()
        clock.tick(60) # Smooth 60 FPS for static viewing

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()