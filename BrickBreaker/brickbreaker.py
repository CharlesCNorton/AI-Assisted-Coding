import sys
import pygame
import numpy as np
import scipy.io.wavfile as wavfile

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Define constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BALL_RADIUS = 8
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
ROWS, COLUMNS = 5, 10
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PADDLE_SPEED = 5
BALL_SPEED = [2, -2]

def generate_bonk_sound():
    # Sample rate and time
    sample_rate = 44100
    duration = 0.05

    # Frequency for 'bonk' sound
    freq = 440.0

    # Create an array for the sound
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate a 'bonk' sound
    bonk_sound = np.sin(freq * t * 2 * np.pi)

    # Fade in/out
    fade_in = np.linspace(0., 1., int(sample_rate * duration // 10))
    fade_out = np.linspace(1., 0., int(sample_rate * duration // 5))

    bonk_sound[:fade_in.size] = np.multiply(bonk_sound[:fade_in.size], fade_in)
    bonk_sound[-fade_out.size:] = np.multiply(bonk_sound[-fade_out.size:], fade_out)

    # Convert to 16-bit PCM sound
    bonk_sound = (bonk_sound * 32767 / np.max(np.abs(bonk_sound))).astype(np.int16)

    # Convert to stereo sound by duplicating the mono sound
    bonk_sound_stereo = np.vstack([bonk_sound, bonk_sound]).T

    # Make the numpy array C-contiguous
    bonk_sound_stereo = np.ascontiguousarray(bonk_sound_stereo)

    # Write to BytesIO object
    bonk_sound_io = pygame.sndarray.make_sound(bonk_sound_stereo)

    return bonk_sound_io

# Create bonk sound
bonk_sound = generate_bonk_sound()

class Paddle(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_x = self.x  # Track the last position

    def move_paddle(self, speed):
        self.last_x = self.x  # Save the current position before moving
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_ip(-speed, 0)
        if keys[pygame.K_RIGHT]:
            self.move_ip(speed, 0)

        if self.right > WIDTH:
            self.right = WIDTH
        if self.left < 0:
            self.left = 0

    @property
    def velocity(self):
        return self.x - self.last_x  # Calculate the velocity

class Ball(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move_ball(self, speed):
        self.move_ip(*speed)

        # Collisions with screen edges
        if self.left < 0 or self.right > WIDTH:
            speed[0] = -speed[0]
            bonk_sound.play()
        if self.top < 0:
            speed[1] = -speed[1]
            bonk_sound.play()

class Brick(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = WHITE  # default color

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.paddle = Paddle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = Ball(WIDTH // 2 - BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)

        # Initialize bricks
        self.bricks = []
        for x in range(COLUMNS):
            for y in range(ROWS):
                brick = Brick(x * (BRICK_WIDTH + 5), y * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT)
                if y < ROWS // 2:  # set color based on position or any other logic
                    brick.color = RED
                else:
                    brick.color = GREEN
                self.bricks.append(brick)

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
            # Calculate where the ball hit the paddle and change direction accordingly
            hit_location = (self.ball.centerx - self.paddle.left) / self.paddle.width
            BALL_SPEED[0] = (hit_location - 0.5) * 4  # Adjust this to change bounce "sharpness"
            BALL_SPEED[0] += self.paddle.velocity / 10  # Add paddle velocity
            BALL_SPEED[1] = -abs(BALL_SPEED[1])  # Always bounce upwards
            bonk_sound.play()

        for brick in self.bricks:
            if self.ball.colliderect(brick):
                BALL_SPEED[1] = -BALL_SPEED[1]
                self.bricks.remove(brick)
                self.score += 1
                bonk_sound.play()
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
        pygame.draw.circle(self.screen, WHITE, (self.ball.x + BALL_RADIUS, self.ball.y + BALL_RADIUS), BALL_RADIUS)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick.color, brick)

        self.render_text(f"Score: {self.score}", (10, 10))

    def render_text(self, text, position):
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, position)

    def show_menu(self):
        while True:
            self.screen.fill(BLACK)
            self.render_text("Brick Breaker", (WIDTH // 2 - 80, HEIGHT // 3))
            self.render_text("Press SPACE to start", (WIDTH // 2 - 120, HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return  # start the game

if __name__ == "__main__":
    game = Game()
    game.show_menu()
    game.run()
