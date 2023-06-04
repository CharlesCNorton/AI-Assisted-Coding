import sys
import pygame

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 8
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
ROWS, COLUMNS = 5, 10
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Create the display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load font for text rendering
font = pygame.font.Font(None, 36)

# Create the paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [2, -2]

# Create the bricks
bricks = [pygame.Rect(x * (BRICK_WIDTH + 5), y * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
          for x in range(COLUMNS) for y in range(ROWS)]

def render_text(text, position):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

def game_loop():
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            paddle.move_ip(5, 0)

        # Update ball
        ball.move_ip(*ball_speed)

        # Collisions
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        for brick in bricks:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)
                break

        if ball.left < 0 or ball.right > WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top < 0:
            ball_speed[1] = -ball_speed[1]
        if ball.bottom > HEIGHT:
            render_text("Game Over!", (WIDTH // 2 - 80, HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        if not bricks:
            render_text("You Win!", (WIDTH // 2 - 70, HEIGHT // 2 - 20))
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        # Render game objects
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)
        for brick in bricks:
            pygame.draw.rect(screen, WHITE, brick)

        # Update display
        pygame.display.flip()

        # Cap frame rate
        pygame.time.Clock().tick(60)

# Run the game
game_loop()
