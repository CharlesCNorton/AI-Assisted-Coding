import sys
import pygame
from pygame.locals import *
from pygame import mixer
import math

pygame.init()
mixer.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Paddle dimensions and speed
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 2

# Ball dimensions and speed
BALL_SIZE = 10
BALL_SPEED = 2

class Paddle:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = speed

    def move(self, dy):
        if self.rect.top + dy > 0 and self.rect.bottom + dy < HEIGHT:
            self.rect.y += dy

class Ball:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self, x, y, dx, dy):
        self.rect.x = x
        self.rect.y = y
        self.dx = dx
        self.dy = dy

try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
except pygame.error as e:
    print(f"Error: {e}")
    sys.exit(1)

pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Paddles and ball
paddle_a = Paddle(10, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED)
paddle_b = Paddle(WIDTH - 20, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED)
ball = Ball(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, BALL_SPEED, BALL_SPEED)

# Scores
score_a = 0
score_b = 0

def create_beep(frequency, duration):
    # create a beep sound with the pygame mixer
    sample_rate = 44100  # Hz
    try:
        beep = mixer.Sound(bytes([min(255, int(128 + 127 * math.sin(x * frequency * math.pi * 2 / sample_rate)))
                                  for x in range(int(sample_rate * duration))]))
    except pygame.error as e:
        print(f"Error: {e}")
        beep = None
    return beep

beep_sound = create_beep(440, 0.1)

def auto_play(paddle):
    if paddle.rect.centery < ball.rect.centery:
        paddle.move(PADDLE_SPEED)
    if paddle.rect.centery > ball.rect.centery:
        paddle.move(-PADDLE_SPEED)

def move_ball():
    global ball_dx, ball_dy, score_a, score_b

    if ball.rect.colliderect(paddle_a.rect) or ball.rect.colliderect(paddle_b.rect):
        ball.dx = -ball.dx
        if beep_sound:
            beep_sound.play()

    if ball.rect.top + ball.dy < 0 or ball.rect.bottom + ball.dy > HEIGHT:
        ball.dy = -ball.dy

    ball.move()

    if ball.rect.left < 0:
        score_b += 1
        ball.reset(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, BALL_SPEED, BALL_SPEED)
    elif ball.rect.right > WIDTH:
        score_a += 1
        ball.reset(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, -BALL_SPEED, -BALL_SPEED)

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, paddle_a.rect)
    pygame.draw.rect(screen, BLUE, paddle_b.rect)
    pygame.draw.rect(screen, WHITE, ball.rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Player A: {score_a}   Player B: {score_b}", True, WHITE)
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 10))

    pygame.display.flip()

def main(auto_play_enabled=False):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_w]:
            paddle_a.move(-PADDLE_SPEED)
        if keys[K_s]:
            paddle_a.move(PADDLE_SPEED)

        if auto_play_enabled:
            auto_play(paddle_b)
        else:
            if keys[K_UP]:
                paddle_b.move(-PADDLE_SPEED)
            if keys[K_DOWN]:
                paddle_b.move(PADDLE_SPEED)

        move_ball()
        draw()
        clock.tick(60)

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Press 1 for Manual or 2 for Auto play", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[K_1]:
            main(auto_play_enabled=False)
        if keys[K_2]:
            main(auto_play_enabled=True)

if __name__ == "__main__":
    menu()
