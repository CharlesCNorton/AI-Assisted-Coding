import sys
import pygame
from pygame.locals import *

pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Paddle dimensions and speed
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball dimensions and speed
BALL_SIZE = 10
BALL_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddles and ball
paddle_a = pygame.Rect(10, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 20, HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)

ball_dx = BALL_SPEED
ball_dy = BALL_SPEED


def move_paddle(paddle, dy):
    if paddle.top + dy > 0 and paddle.bottom + dy < HEIGHT:
        paddle.y += dy


def move_ball():
    global ball_dx, ball_dy

    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_dx = -ball_dx

    if ball.top + ball_dy < 0 or ball.bottom + ball_dy > HEIGHT:
        ball_dy = -ball_dy

    ball.x += ball_dx
    ball.y += ball_dy


def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.rect(screen, WHITE, ball)
    pygame.display.flip()


def main():
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
        if keys[K_UP]:
            move_paddle(paddle_b, -PADDLE_SPEED)
        if keys[K_DOWN]:
            move_paddle(paddle_b, PADDLE_SPEED)

        move_ball()

        if ball.left < 0 or ball.right > WIDTH:
            ball.x = WIDTH / 2 - BALL_SIZE / 2
            ball.y = HEIGHT / 2 - BALL_SIZE / 2
            ball_dx = -ball_dx

        draw()
        clock.tick(60)


if __name__ == "__main__":
    main()
