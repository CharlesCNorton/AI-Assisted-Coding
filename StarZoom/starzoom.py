import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Get screen size and set up the display
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h

# Star colors (white shades)
STAR_COLORS = [(255, 255, 255), (200, 200, 200), (150, 150, 150)]

# Number of stars
NUM_STARS = 400

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Clock for controlling FPS
clock = pygame.time.Clock()

# Star class
class Star:
    def __init__(self):
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(-1, 1)
        self.z = random.uniform(0, 1)
        self.color = random.choice(STAR_COLORS)
        self.speed = random.uniform(0.002, 0.015)
        self.twinkle_speed = random.uniform(0.005, 0.02)
        self.twinkle_direction = random.choice([1, -1])

    def update(self):
        self.z -= self.speed
        if self.z <= 0:
            self.z = random.uniform(0.8, 1)
            self.x = random.uniform(-1, 1)
            self.y = random.uniform(-1, 1)

        self.twinkle()

    def draw(self, surface):
        sx = int((self.x / self.z) * (WIDTH / 2) + (WIDTH / 2))
        sy = int((self.y / self.z) * (HEIGHT / 2) + (HEIGHT / 2))

        if 0 < sx < WIDTH and 0 < sy < HEIGHT:
            r = 3 / self.z
            pygame.draw.circle(surface, self.color, (int(sx), int(sy)), int(r))

    def twinkle(self):
        new_color = [max(0, min(255, channel + self.twinkle_direction * self.twinkle_speed * 255)) for channel in self.color]
        self.color = tuple(map(int, new_color))

        if self.twinkle_direction == 1 and self.color == STAR_COLORS[0]:
            self.twinkle_direction = -1
        elif self.twinkle_direction == -1 and self.color == STAR_COLORS[2]:
            self.twinkle_direction = 1

# Create star instances
stars = [Star() for _ in range(NUM_STARS)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Update stars
    for star in stars:
        star.update()

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw stars
    for star in stars:
        star.draw(screen)

    # Update display
    pygame.display.flip()

    # Control FPS
    clock.tick(60)

# Fade out before exit
surface = pygame.display.set_mode((int(width), int(height)))
fade_surface.fill((0, 0, 0))
alpha = 0
while alpha < 255:
    fade_surface.set_alpha(alpha)
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()
    alpha += 3
    clock.tick(60)

pygame.quit()
sys.exit()

