import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_grid(surface, width, height, block_size):
    gray = (50, 50, 50)
    for x in range(0, width, block_size):
        pygame.draw.line(surface, gray, (x, 0), (x, height))
    for y in range(0, height, block_size):
        pygame.draw.line(surface, gray, (0, y), (width, y))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 1. Clear the screen
        screen.fill((0, 0, 0))
        
        # 2. Draw the grid
        draw_grid(screen, WIDTH, HEIGHT, BLOCK_SIZE)
        
        # 3. Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()