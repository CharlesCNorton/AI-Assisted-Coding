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
PADDLE_SPEED = 5
BALL_SPEED = [2, -2]

class Paddle(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move_paddle(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT]:
            self.move_ip(speed, 0)

        if self.right > WIDTH:
            self.right = WIDTH
        if self.left < 0:
            self.left = 0

class Ball(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move_ball(self, speed):
        self.move_ip(*speed)

        # Collisions with screen edges
        if self.left < 0 or self.right > WIDTH:
            speed[0] = -speed[0]
        if self.top < 0:
            speed[1] = -speed[1]

class Brick(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = Ball(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.bricks = [Brick(x * (BRICK_WIDTH + 5), y * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT) for x in range(COLUMNS) for y in range(ROWS)]

    def run(self):
        while True:
            self.handle_events()
            self.update_game()
            self.render_objects()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_game(self):
        self.paddle.move_paddle(PADDLE_SPEED)
        self.ball.move_ball(BALL_SPEED)

        if self.ball.colliderect(self.paddle):
            BALL_SPEED[1] = -BALL_SPEED[1]

        for brick in self.bricks:
            if self.ball.colliderect(brick):
                BALL_SPEED[1] = -BALL_SPEED[1]
                self.bricks.remove(brick)
                self.score += 1
                break

        if self.ball.bottom > HEIGHT:
            self.end_game("Game Over!")

        if not self.bricks:
            self.end_game("You Win!")

    def end_game(self, text):
        self.render_text(text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(3000)
        sys.exit()

    def render_objects(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, self.paddle)
        pygame.draw.circle(self.screen, WHITE, self.ball.center, BALL_RADIUS)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, WHITE, brick)
        self.render_text(f"Score: {self.score}", (10, 10))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, position)

if __name__ == "__main__":
    Game().run()