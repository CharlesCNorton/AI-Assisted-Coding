import sys
import pygame
import math
from pygame.locals import *
from pygame import mixer

# Initializations
pygame.init()
mixer.init()

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 2
BALL_SIZE = 10
BALL_SPEED = 2
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
SAMPLE_RATE = 44100  # Hz

font = pygame.font.Font(None, FONT_SIZE)


class Paddle:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = speed

    def move(self, dy):
        if 0 < self.rect.top + dy < HEIGHT - PADDLE_HEIGHT:
            self.rect.y += dy


class Ball:
    def __init__(self, x, y, dx, dy):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.dx = dx
        self.dy = dy

    def move(self):
        if self.rect.colliderect(paddle_a.rect) or self.rect.colliderect(paddle_b.rect):
            self.dx = -self.dx
            beep_sound.play()

        if self.rect.top + self.dy < 0 or self.rect.bottom + self.dy > HEIGHT:
            self.dy = -self.dy

        self.rect.x += self.dx
        self.rect.y += self.dy

    def reset(self, towards_left=True):
        direction = -1 if towards_left else 1
        self.rect.x = WIDTH / 2 - BALL_SIZE / 2
        self.rect.y = HEIGHT / 2 - BALL_SIZE / 2
        self.dx = direction * BALL_SPEED
        self.dy = BALL_SPEED


def create_beep(frequency, duration):
    try:
        beep = mixer.Sound(bytes([min(255, int(128 + 127 * math.sin(x * frequency * math.pi * 2 / SAMPLE_RATE)))
                                  for x in range(int(SAMPLE_RATE * duration))]))
    except pygame.error as e:
        print(f"Error: {e}")
        beep = None
    return beep


beep_sound = create_beep(440, 0.1)


def auto_play(paddle):
    if paddle.rect.centery < ball.rect.centery:
        paddle.move(PADDLE_SPEED)
    else:
        paddle.move(-PADDLE_SPEED)


def move_ball():
    global score_a, score_b

    ball.move()

    if ball.rect.left < 0:
        score_b += 1
        ball.reset(towards_left=False)
    elif ball.rect.right > WIDTH:
        score_a += 1
        ball.reset()


def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, paddle_a.rect)
    pygame.draw.rect(screen, BLUE, paddle_b.rect)
    pygame.draw.ellipse(screen, WHITE, ball.rect)
    pygame.draw.aaline(screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

    score_text = font.render(f"Player A: {score_a}   Player B: {score_b}", True, WHITE)
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 10))

    pygame.display.flip()


def main(auto_play_enabled=False):
    global score_a, score_b
    score_a, score_b = 0, 0

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
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        clock = pygame.time.Clock()
        paddle_a = Paddle(10, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED)
        paddle_b = Paddle(WIDTH - 20, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED)
        ball = Ball(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, BALL_SPEED, BALL_SPEED)
        menu()
    except pygame.error as e:
        print(f"Error: {e}")
        sys.exit(1)
