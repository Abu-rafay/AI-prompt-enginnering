import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Window")

# Define colors (R, G, B)
GRAY = (128, 128, 128)

# Set up the clock for frame rate control
clock = pygame.time.Clock()
FPS = 60

def main():
    running = True
    
    # Main Game Loop
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Update Game State
        # (Game logic goes here)

        # 3. Drawing
        screen.fill(GRAY)  # Fill background with gray

        # Update the display
        pygame.display.flip()

        # Lock the frame rate to 60 FPS
        clock.tick(FPS)

    # Clean exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()