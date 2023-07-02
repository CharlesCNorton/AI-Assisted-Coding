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
paddle_a = pygame.Rect(10, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 20, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)

ball_dx = BALL_SPEED
ball_dy = BALL_SPEED

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

def move_paddle(paddle, dy):
    if paddle.top + dy > 0 and paddle.bottom + dy < HEIGHT:
        paddle.y += dy

def auto_play(paddle):
    if paddle.centery < ball.centery:
        move_paddle(paddle, PADDLE_SPEED)
    if paddle.centery > ball.centery:
        move_paddle(paddle, -PADDLE_SPEED)

def move_ball():
    global ball_dx, ball_dy

    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_dx = -ball_dx
        if beep_sound:
            beep_sound.play()

    if ball.top + ball_dy < 0 or ball.bottom + ball_dy > HEIGHT:
        ball_dy = -ball_dy

    ball.x += ball_dx
    ball.y += ball_dy

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, paddle_a)
    pygame.draw.rect(screen, BLUE, paddle_b)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.display.flip()

def main(auto_play_enabled=False):
    global ball_dx

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[K_w]:
            move_paddle(paddle_a, -PADDLE_SPEED)
        if keys[K_s]:
            move_paddle(paddle_a, PADDLE_SPEED)

        if auto_play_enabled:
            auto_play(paddle_b)
        else:
            if keys[K_UP]:
                move_paddle(paddle_b, -PADDLE_SPEED)
            if keys[K_DOWN]:
                move_paddle(paddle_b, PADDLE_SPEED)

        move_ball()

        if ball.left < 0 or ball.right > WIDTH:
            ball.x = WIDTH / 2 - BALL_SIZE / 2
            ball.y = HEIGHT / 2 - BALL_SIZE / 2
            ball_dx = -ball_dx
            ball_dy = BALL_SPEED if paddle_a.centery < ball.centery else -BALL_SPEED

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
