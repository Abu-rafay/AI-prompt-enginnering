import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Setup the display
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Pygame Window")

# 3. Setup the clock (controls the frame rate)
clock = pygame.time.Clock()

def main():
    running = True
    
    # --- MAIN GAME LOOP ---
    while running:
        # A. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # B. Game Logic (Update positions, scores, etc.)
        # ...

        # C. Drawing / Rendering
        screen.fill((0, 0, 0))  # Fill with Black (RGB)
        
        # D. Flip the display (Updates the actual screen)
        pygame.display.flip()

        # E. Maintain 60 FPS
        clock.tick(60)

    # 4. Clean Shutdown
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()