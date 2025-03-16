"""
Enhanced Brick Breaker Game
---------------------------
A more robust implementation with improved gameplay mechanics, better code organization,
and additional features like power-ups, lives system, and level progression.
"""

import sys
import os
import random
import json
from typing import List, Dict, Tuple, Optional, Union, Any
import pygame
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# =============== CONFIGURATION ===============

class Config:
    """Game configuration and constants"""
    # Display
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    TITLE = "Advanced Brick Breaker"
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    CYAN = (0, 255, 255)
    GRAY = (128, 128, 128)
    
    # Game elements
    PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
    BALL_RADIUS = 8
    BRICK_WIDTH, BRICK_HEIGHT = 75, 20
    POWERUP_SIZE = 20
    POWERUP_SPEED = 2
    
    # Game settings
    PADDLE_SPEED = 8
    BALL_INITIAL_SPEED_X = 2
    BALL_INITIAL_SPEED_Y = -4
    
    # Difficulty levels
    EASY = 1
    MEDIUM = 2
    HARD = 3
    
    DIFFICULTY_LEVELS = {
        EASY: {"ball_speed_multiplier": 1.0, "score_multiplier": 1.0, "lives": 5},
        MEDIUM: {"ball_speed_multiplier": 1.4, "score_multiplier": 1.5, "lives": 3},
        HARD: {"ball_speed_multiplier": 1.8, "score_multiplier": 2.0, "lives": 2}
    }

    # Level settings
    MAX_LEVEL = 5
    
    # Save file
    SAVE_FILE = "breakout_save.json"
    HIGH_SCORES_FILE = "breakout_scores.json"
    
    @staticmethod
    def get_difficulty_settings(level: int) -> Dict[str, float]:
        """Get settings for a specific difficulty level"""
        if level in Config.DIFFICULTY_LEVELS:
            return Config.DIFFICULTY_LEVELS[level]
        return Config.DIFFICULTY_LEVELS[Config.EASY]  # Default to easy

# =============== ASSET MANAGER ===============

class AssetManager:
    """Handles loading and managing game assets"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists"""
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the asset manager"""
        if self._initialized:
            return
            
        self.sounds = {}
        self.fonts = {}
        self._initialized = True
        
        # Load assets
        self._load_sounds()
        self._load_fonts()
    
    def _load_sounds(self):
        """Generate and load sound effects"""
        self.sounds["paddle_hit"] = self._generate_sound(440, 0.1)  # Higher pitch for paddle
        self.sounds["brick_hit"] = self._generate_sound(330, 0.1)   # Mid pitch for bricks
        self.sounds["wall_hit"] = self._generate_sound(220, 0.1)    # Lower pitch for walls
        self.sounds["power_up"] = self._generate_sound(660, 0.2)    # Power-up collection sound
        self.sounds["level_complete"] = self._generate_sound(550, 0.4, is_success=True)
        self.sounds["game_over"] = self._generate_sound(110, 0.5, is_success=False)
    
    def _generate_sound(self, frequency: float, duration: float, is_success: bool = None) -> pygame.mixer.Sound:
        """Generate a sound effect with the given parameters"""
        sample_rate = 44100
        
        # Create time array
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        if is_success is not None:
            # Generate more complex sound for level complete/game over
            if is_success:
                # Success sound (ascending notes)
                note1 = np.sin(frequency * t * 2 * np.pi)
                note2 = np.sin(frequency * 1.25 * (t - 0.1) * 2 * np.pi) * (t > 0.1)
                note3 = np.sin(frequency * 1.5 * (t - 0.2) * 2 * np.pi) * (t > 0.2)
                sound = note1 + note2 + note3
            else:
                # Game over sound (descending notes)
                note1 = np.sin(frequency * t * 2 * np.pi)
                note2 = np.sin(frequency * 0.75 * (t - 0.1) * 2 * np.pi) * (t > 0.1)
                note3 = np.sin(frequency * 0.5 * (t - 0.2) * 2 * np.pi) * (t > 0.2)
                sound = note1 + note2 + note3
        else:
            # Simple sine wave for basic sounds
            sound = np.sin(frequency * t * 2 * np.pi)
        
        # Apply envelope
        fade_in = np.linspace(0.0, 1.0, int(sample_rate * duration * 0.1))
        fade_out = np.linspace(1.0, 0.0, int(sample_rate * duration * 0.2))
        
        sound[:fade_in.size] = sound[:fade_in.size] * fade_in
        sound[-fade_out.size:] = sound[-fade_out.size:] * fade_out
        
        # Normalize and convert to 16-bit PCM
        sound = (sound / np.max(np.abs(sound)) * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_sound = np.vstack([sound, sound]).T
        stereo_sound = np.ascontiguousarray(stereo_sound)
        
        # Create pygame sound object
        return pygame.sndarray.make_sound(stereo_sound)
    
    def _load_fonts(self):
        """Load game fonts"""
        try:
            self.fonts["small"] = pygame.font.Font(None, 24)
            self.fonts["medium"] = pygame.font.Font(None, 36)
            self.fonts["large"] = pygame.font.Font(None, 48)
            self.fonts["title"] = pygame.font.Font(None, 72)
        except Exception as e:
            print(f"Error loading fonts: {e}")
            # Fallback to default font if error occurs
            default_font = pygame.font.Font(None, 36)
            self.fonts = {
                "small": default_font,
                "medium": default_font,
                "large": default_font,
                "title": default_font
            }
    
    def play_sound(self, sound_name: str) -> None:
        """Play a sound by name"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def get_font(self, size: str) -> pygame.font.Font:
        """Get a font by size"""
        if size in self.fonts:
            return self.fonts[size]
        return self.fonts["medium"]  # Default to medium size

# =============== GAME ENTITIES ===============

class GameObject:
    """Base class for all game objects"""
    
    def __init__(self, x: float, y: float, width: float, height: float, color: Tuple[int, int, int] = Config.WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active = True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the object on the given surface"""
        if self.active:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def update(self) -> None:
        """Update the object state (to be overridden by subclasses)"""
        pass

class Paddle(GameObject):
    """Player-controlled paddle"""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, Config.PADDLE_WIDTH, Config.PADDLE_HEIGHT, Config.CYAN)
        self.speed = Config.PADDLE_SPEED
        self.last_x = x  # Track previous position for velocity calculation
        self.original_width = Config.PADDLE_WIDTH
        self.powerup_timer = 0
    
    def update(self, mouse_control: bool = False) -> None:
        """Update paddle position based on input"""
        self.last_x = self.rect.x
        
        if mouse_control:
            # Mouse control
            mouse_x, _ = pygame.mouse.get_pos()
            self.rect.centerx = mouse_x
        else:
            # Keyboard control
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
        
        # Keep paddle within screen boundaries
        if self.rect.right > Config.WIDTH:
            self.rect.right = Config.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
        # Handle power-up effects
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.rect.width = self.original_width  # Reset width when timer expires
    
    @property
    def velocity(self) -> float:
        """Calculate paddle velocity for ball physics"""
        return (self.rect.x - self.last_x) * 0.2  # Dampen the effect
    
    def apply_powerup(self, powerup_type: str) -> None:
        """Apply a power-up effect to the paddle"""
        if powerup_type == "expand":
            self.rect.width = min(self.original_width * 1.5, Config.WIDTH // 2)
            self.powerup_timer = Config.FPS * 10  # 10 seconds
        elif powerup_type == "shrink":
            self.rect.width = max(self.original_width * 0.5, 40)
            self.powerup_timer = Config.FPS * 5  # 5 seconds
        
        # Ensure paddle stays within screen bounds after resize
        if self.rect.right > Config.WIDTH:
            self.rect.right = Config.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ball(GameObject):
    """Ball that bounces around and breaks bricks"""
    
    def __init__(self, x: float, y: float, difficulty: int = Config.EASY):
        super().__init__(x, y, Config.BALL_RADIUS * 2, Config.BALL_RADIUS * 2, Config.WHITE)
        
        # Apply difficulty multiplier to speed
        speed_multiplier = Config.get_difficulty_settings(difficulty)["ball_speed_multiplier"]
        
        self.speed_x = Config.BALL_INITIAL_SPEED_X * speed_multiplier
        self.speed_y = Config.BALL_INITIAL_SPEED_Y * speed_multiplier
        self.attached = False  # Whether ball is attached to paddle at start
        self.attach_offset = 0  # Offset from paddle center when attached
        self.fire_mode = False  # Power-up: ball destroys bricks without bouncing
        self.fire_timer = 0
    
    def update(self) -> bool:
        """Update ball position and handle basic collisions
        
        Returns:
            bool: True if ball is still in play, False if it fell off the bottom
        """
        if self.attached:
            return True  # Skip movement if attached to paddle
        
        # Move ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Screen boundary collisions
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x = abs(self.speed_x)  # Bounce right
            AssetManager().play_sound("wall_hit")
            
        elif self.rect.right >= Config.WIDTH:
            self.rect.right = Config.WIDTH
            self.speed_x = -abs(self.speed_x)  # Bounce left
            AssetManager().play_sound("wall_hit")
            
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)  # Bounce down
            AssetManager().play_sound("wall_hit")
        
        # Update fire power-up timer
        if self.fire_mode and self.fire_timer > 0:
            self.fire_timer -= 1
            if self.fire_timer == 0:
                self.fire_mode = False
                self.color = Config.WHITE
        
        # Check if ball fell off the bottom
        return self.rect.top < Config.HEIGHT
    
    def attach_to_paddle(self, paddle: Paddle) -> None:
        """Attach ball to paddle for the start of the game or after losing a life"""
        self.attached = True
        self.attach_offset = random.randint(-paddle.rect.width // 3, paddle.rect.width // 3)
        self.rect.centerx = paddle.rect.centerx + self.attach_offset
        self.rect.bottom = paddle.rect.top
    
    def release(self, paddle) -> None:
        """Release ball from paddle"""
        if self.attached:
            self.attached = False
            # Add slight randomness to initial direction
            self.speed_x = Config.BALL_INITIAL_SPEED_X + (self.attach_offset / paddle.rect.width * 2)
            self.speed_y = Config.BALL_INITIAL_SPEED_Y
    
    def handle_paddle_collision(self, paddle: Paddle) -> bool:
        """Handle collision with the paddle
        
        Returns:
            bool: True if collision occurred, False otherwise
        """
        if not self.rect.colliderect(paddle.rect):
            return False
            
        AssetManager().play_sound("paddle_hit")
        
        # Calculate bounce angle based on where ball hit paddle
        hit_pos = (self.rect.centerx - paddle.rect.left) / paddle.rect.width
        
        # Normalize hit position to [-1, 1] range
        hit_pos = 2 * hit_pos - 1
        
        # Steeper angles at the edges, moderate angles near the center
        self.speed_x = hit_pos * abs(self.speed_y) * 0.75
        
        # Add paddle's movement to the ball
        self.speed_x += paddle.velocity
        
        # Ensure ball always goes upward
        self.speed_y = -abs(self.speed_y)
        
        # Ensure ball doesn't get stuck in paddle
        self.rect.bottom = paddle.rect.top - 1
        
        return True
    
    def handle_brick_collision(self, brick: 'Brick') -> bool:
        """Handle collision with a brick
        
        Returns:
            bool: True if collision occurred, False otherwise
        """
        if not self.rect.colliderect(brick.rect) or not brick.active:
            return False
            
        # In fire mode, just destroy the brick without bouncing
        if self.fire_mode:
            return True
            
        AssetManager().play_sound("brick_hit")
        
        # Determine which side of the brick was hit
        # Calculate distances to each side of the brick
        left_dist = abs(self.rect.right - brick.rect.left)
        right_dist = abs(self.rect.left - brick.rect.right)
        top_dist = abs(self.rect.bottom - brick.rect.top)
        bottom_dist = abs(self.rect.top - brick.rect.bottom)
        
        # Find the minimum distance
        min_dist = min(left_dist, right_dist, top_dist, bottom_dist)
        
        # Bounce based on which side was hit
        if min_dist == left_dist or min_dist == right_dist:
            self.speed_x = -self.speed_x
        else:  # top or bottom collision
            self.speed_y = -self.speed_y
        
        return True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the ball on the given surface"""
        if self.active:
            pygame.draw.ellipse(surface, self.color, self.rect)
            
            # Add fire effect when in fire mode
            if self.fire_mode:
                # Draw flame effect (orange/red circles around the ball)
                flame_radius = random.randint(Config.BALL_RADIUS - 2, Config.BALL_RADIUS + 2)
                flame_rect = pygame.Rect(
                    self.rect.centerx - flame_radius,
                    self.rect.centery - flame_radius,
                    flame_radius * 2,
                    flame_radius * 2
                )
                flame_color = random.choice([Config.RED, Config.ORANGE, Config.YELLOW])
                pygame.draw.ellipse(surface, flame_color, flame_rect)
    
    def apply_powerup(self, powerup_type: str) -> None:
        """Apply a power-up effect to the ball"""
        if powerup_type == "speed_up":
            # Increase speed by 30%
            speed_magnitude = (self.speed_x**2 + self.speed_y**2)**0.5
            speed_up_factor = 1.3
            
            # Preserve direction but increase magnitude
            if speed_magnitude > 0:
                self.speed_x = self.speed_x / speed_magnitude * (speed_magnitude * speed_up_factor)
                self.speed_y = self.speed_y / speed_magnitude * (speed_magnitude * speed_up_factor)
        
        elif powerup_type == "slow_down":
            # Decrease speed by 30%
            speed_magnitude = (self.speed_x**2 + self.speed_y**2)**0.5
            slow_down_factor = 0.7
            
            # Preserve direction but decrease magnitude
            if speed_magnitude > 0:
                self.speed_x = self.speed_x / speed_magnitude * (speed_magnitude * slow_down_factor)
                self.speed_y = self.speed_y / speed_magnitude * (speed_magnitude * slow_down_factor)
        
        elif powerup_type == "fire_ball":
            self.fire_mode = True
            self.color = Config.ORANGE
            self.fire_timer = Config.FPS * 8  # 8 seconds of fire mode

class Brick(GameObject):
    """Breakable brick that increases score when hit"""
    
    def __init__(self, x: float, y: float, brick_type: str = "normal"):
        # Set color and properties based on brick type
        color = self._get_color_for_type(brick_type)
        super().__init__(x, y, Config.BRICK_WIDTH, Config.BRICK_HEIGHT, color)
        
        self.brick_type = brick_type
        self.hits_required = self._get_hits_required()
        self.current_hits = 0
        self.points = self._get_points()
        self.has_powerup = random.random() < 0.2  # 20% chance of containing a power-up
        self.powerup_type = self._get_random_powerup() if self.has_powerup else None
    
    def _get_color_for_type(self, brick_type: str) -> Tuple[int, int, int]:
        """Get the color for a specific brick type"""
        colors = {
            "normal": Config.WHITE,
            "hardy": Config.YELLOW,
            "strong": Config.ORANGE,
            "unbreakable": Config.GRAY,
            "bonus": Config.GREEN,
            "explosive": Config.RED,
            "powerup": Config.PURPLE
        }
        return colors.get(brick_type, Config.WHITE)
    
    def _get_hits_required(self) -> int:
        """Get the number of hits required to break this brick"""
        hits = {
            "normal": 1,
            "hardy": 2,
            "strong": 3,
            "unbreakable": -1,  # Unbreakable
            "bonus": 1,
            "explosive": 1,
            "powerup": 1
        }
        return hits.get(self.brick_type, 1)
    
    def _get_points(self) -> int:
        """Get the points awarded for breaking this brick"""
        points = {
            "normal": 10,
            "hardy": 20,
            "strong": 30,
            "unbreakable": 0,
            "bonus": 50,
            "explosive": 15,
            "powerup": 25
        }
        return points.get(self.brick_type, 10)
    
    def _get_random_powerup(self) -> str:
        """Get a random power-up type"""
        powerups = [
            "expand",       # Expand paddle
            "shrink",       # Shrink paddle
            "slow_down",    # Slow down ball
            "speed_up",     # Speed up ball
            "fire_ball",    # Ball breaks bricks without bouncing
            "extra_life"    # Award an extra life
        ]
        return random.choice(powerups)
    
    def hit(self) -> Tuple[bool, Optional[str]]:
        """Register a hit on the brick
        
        Returns:
            Tuple[bool, Optional[str]]: (is_broken, powerup_type if any)
        """
        if self.brick_type == "unbreakable":
            return False, None
            
        self.current_hits += 1
        
        # Update color based on remaining hits (for multi-hit bricks)
        if self.brick_type in ("hardy", "strong"):
            brightness = max(0.3, 1 - (self.current_hits / self.hits_required))
            r, g, b = self.color
            self.color = (
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            )
        
        if self.current_hits >= self.hits_required:
            self.active = False
            return True, self.powerup_type
            
        return False, None
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the brick with additional visual effects"""
        if not self.active:
            return
            
        # Draw basic brick
        super().draw(surface)
        
        # Add visual indicators
        if self.brick_type == "unbreakable":
            # Draw X pattern for unbreakable bricks
            pygame.draw.line(surface, Config.BLACK, 
                             (self.rect.left + 5, self.rect.top + 5),
                             (self.rect.right - 5, self.rect.bottom - 5), 2)
            pygame.draw.line(surface, Config.BLACK, 
                             (self.rect.left + 5, self.rect.bottom - 5),
                             (self.rect.right - 5, self.rect.top + 5), 2)
        
        elif self.brick_type in ("hardy", "strong"):
            # Draw number of hits remaining
            hits_left = self.hits_required - self.current_hits
            font = AssetManager().get_font("small")
            text = font.render(str(hits_left), True, Config.BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        
        elif self.has_powerup:
            # Draw a small indicator that this brick contains a power-up
            indicator_radius = 3
            pygame.draw.circle(
                surface,
                Config.PURPLE,
                (self.rect.centerx, self.rect.centery),
                indicator_radius
            )

class PowerUp(GameObject):
    """Power-up that falls from broken bricks"""
    
    def __init__(self, x: float, y: float, powerup_type: str):
        super().__init__(
            x - Config.POWERUP_SIZE // 2,
            y - Config.POWERUP_SIZE // 2,
            Config.POWERUP_SIZE,
            Config.POWERUP_SIZE,
            self._get_color_for_type(powerup_type)
        )
        self.powerup_type = powerup_type
        self.speed = Config.POWERUP_SPEED
    
    def _get_color_for_type(self, powerup_type: str) -> Tuple[int, int, int]:
        """Get the color for a specific power-up type"""
        colors = {
            "expand": Config.GREEN,
            "shrink": Config.RED,
            "slow_down": Config.CYAN,
            "speed_up": Config.YELLOW,
            "fire_ball": Config.ORANGE,
            "extra_life": Config.PURPLE
        }
        return colors.get(powerup_type, Config.WHITE)
    
    def update(self) -> bool:
        """Update power-up position
        
        Returns:
            bool: True if still on screen, False if it fell off
        """
        self.rect.y += self.speed
        return self.rect.top < Config.HEIGHT
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the power-up with a distinctive shape"""
        if not self.active:
            return
            
        # Draw colored background
        pygame.draw.rect(surface, self.color, self.rect)
        
        # Draw white symbol based on type
        symbol_color = Config.WHITE
        
        if self.powerup_type == "expand":
            # Draw expand symbol (horizontal line)
            pygame.draw.line(
                surface, symbol_color,
                (self.rect.left + 4, self.rect.centery),
                (self.rect.right - 4, self.rect.centery),
                2
            )
        elif self.powerup_type == "shrink":
            # Draw shrink symbol (vertical line)
            pygame.draw.line(
                surface, symbol_color,
                (self.rect.centerx, self.rect.top + 4),
                (self.rect.centerx, self.rect.bottom - 4),
                2
            )
        elif self.powerup_type == "slow_down":
            # Draw slow down symbol (minus sign)
            pygame.draw.line(
                surface, symbol_color,
                (self.rect.left + 4, self.rect.centery),
                (self.rect.right - 4, self.rect.centery),
                2
            )
        elif self.powerup_type == "speed_up":
            # Draw speed up symbol (plus sign)
            pygame.draw.line(
                surface, symbol_color,
                (self.rect.left + 4, self.rect.centery),
                (self.rect.right - 4, self.rect.centery),
                2
            )
            pygame.draw.line(
                surface, symbol_color,
                (self.rect.centerx, self.rect.top + 4),
                (self.rect.centerx, self.rect.bottom - 4),
                2
            )
        elif self.powerup_type == "fire_ball":
            # Draw fire symbol (triangle)
            pygame.draw.polygon(
                surface, symbol_color,
                [
                    (self.rect.centerx, self.rect.top + 4),
                    (self.rect.left + 4, self.rect.bottom - 4),
                    (self.rect.right - 4, self.rect.bottom - 4)
                ]
            )
        elif self.powerup_type == "extra_life":
            # Draw heart symbol
            pygame.draw.circle(
                surface, symbol_color,
                (self.rect.centerx - 4, self.rect.centery - 2),
                3
            )
            pygame.draw.circle(
                surface, symbol_color,
                (self.rect.centerx + 4, self.rect.centery - 2),
                3
            )
            # Draw triangle for bottom of heart
            pygame.draw.polygon(
                surface, symbol_color,
                [
                    (self.rect.centerx - 7, self.rect.centery - 2),
                    (self.rect.centerx + 7, self.rect.centery - 2),
                    (self.rect.centerx, self.rect.centery + 5)
                ]
            )

# =============== LEVEL MANAGEMENT ===============

class LevelManager:
    """Manages game levels and brick layouts"""
    
    def __init__(self):
        self.current_level = 1
    
    def create_level(self, level: int) -> List[Brick]:
        """Create bricks for the specified level"""
        bricks = []
        
        if level == 1:
            # Basic grid layout
            bricks = self._create_grid_layout(rows=4, cols=10)
        elif level == 2:
            # Checkerboard with some hardy bricks
            bricks = self._create_checkerboard_layout(rows=5, cols=10)
        elif level == 3:
            # Wall layout with unbreakable bricks
            bricks = self._create_wall_layout()
        elif level == 4:
            # Pyramid layout
            bricks = self._create_pyramid_layout(rows=6)
        elif level == 5:
            # Final level - complex layout with all brick types
            bricks = self._create_final_layout()
        else:
            # Fallback to random layout for any other level
            bricks = self._create_random_layout(rows=5, cols=10)
            
        return bricks
    
    def _create_grid_layout(self, rows: int, cols: int) -> List[Brick]:
        """Create a simple grid layout of bricks"""
        bricks = []
        brick_types = ["normal"] * 8 + ["hardy"] * 2  # 80% normal, 20% hardy
        
        for row in range(rows):
            for col in range(cols):
                brick_type = brick_types[row % len(brick_types)]
                
                # Determine color by row
                color_options = [Config.RED, Config.ORANGE, Config.YELLOW, Config.GREEN, Config.BLUE]
                color = color_options[row % len(color_options)]
                
                x = col * (Config.BRICK_WIDTH + 5) + 10
                y = row * (Config.BRICK_HEIGHT + 5) + 50
                
                brick = Brick(x, y, brick_type)
                brick.color = color
                bricks.append(brick)
                
        return bricks
    
    def _create_checkerboard_layout(self, rows: int, cols: int) -> List[Brick]:
        """Create a checkerboard layout of bricks"""
        bricks = []
        
        for row in range(rows):
            for col in range(cols):
                # Skip some positions to create checkerboard
                if (row + col) % 2 == 0:
                    continue
                
                # Choose brick type: more hardy bricks in higher rows
                if row < rows // 2:
                    brick_type = "normal"
                else:
                    brick_type = random.choice(["normal", "hardy", "normal"])
                
                x = col * (Config.BRICK_WIDTH + 5) + 10
                y = row * (Config.BRICK_HEIGHT + 5) + 50
                
                bricks.append(Brick(x, y, brick_type))
                
        return bricks
    
    def _create_wall_layout(self) -> List[Brick]:
        """Create a wall layout with some unbreakable bricks"""
        bricks = []
        cols = 10
        
        # Row 1: Alternating normal and unbreakable
        for col in range(cols):
            x = col * (Config.BRICK_WIDTH + 5) + 10
            y = 50
            brick_type = "unbreakable" if col % 2 == 0 else "normal"
            bricks.append(Brick(x, y, brick_type))
        
        # Row 2: All normal
        for col in range(cols):
            x = col * (Config.BRICK_WIDTH + 5) + 10
            y = 50 + (Config.BRICK_HEIGHT + 5)
            bricks.append(Brick(x, y, "normal"))
        
        # Row 3: Strong bricks
        for col in range(cols):
            x = col * (Config.BRICK_WIDTH + 5) + 10
            y = 50 + 2 * (Config.BRICK_HEIGHT + 5)
            bricks.append(Brick(x, y, "strong"))
        
        # Row 4: Hardy bricks
        for col in range(cols):
            x = col * (Config.BRICK_WIDTH + 5) + 10
            y = 50 + 3 * (Config.BRICK_HEIGHT + 5)
            bricks.append(Brick(x, y, "hardy"))
        
        # Row 5: Normal bricks
        for col in range(cols):
            x = col * (Config.BRICK_WIDTH + 5) + 10
            y = 50 + 4 * (Config.BRICK_HEIGHT + 5)
            brick_type = "powerup" if col % 3 == 0 else "normal"
            bricks.append(Brick(x, y, brick_type))
            
        return bricks
    
    def _create_pyramid_layout(self, rows: int) -> List[Brick]:
        """Create a pyramid layout of bricks"""
        bricks = []
        max_cols = 2 * rows - 1
        
        for row in range(rows):
            cols_in_row = 2 * (rows - row) - 1
            start_col = (max_cols - cols_in_row) // 2
            
            for i in range(cols_in_row):
                col = start_col + i
                x = col * (Config.BRICK_WIDTH + 5) + 10
                y = row * (Config.BRICK_HEIGHT + 5) + 50
                
                # Determine brick type based on position
                if row == 0:  # Top row
                    brick_type = "strong"
                elif row < rows // 2:  # Upper half
                    brick_type = "hardy"
                else:  # Lower half
                    brick_type = "normal"
                
                # Add some bonus bricks
                if row > 0 and i % 5 == 0:
                    brick_type = "bonus"
                
                bricks.append(Brick(x, y, brick_type))
                
        return bricks
    
    def _create_final_layout(self) -> List[Brick]:
        """Create a complex layout for the final level"""
        bricks = []
        
        # Create a perimeter of unbreakable bricks
        cols = 10
        rows = 6
        
        for col in range(cols):
            for row in range(rows):
                x = col * (Config.BRICK_WIDTH + 5) + 10
                y = row * (Config.BRICK_HEIGHT + 5) + 50
                
                # Perimeter is unbreakable
                if col == 0 or col == cols - 1 or row == 0 or row == rows - 1:
                    brick_type = "unbreakable"
                # Inside has a mix of different brick types
                else:
                    # Create a pattern with different brick types
                    if (row + col) % 3 == 0:
                        brick_type = "strong"
                    elif (row + col) % 3 == 1:
                        brick_type = "hardy"
                    else:
                        brick_type = "normal"
                    
                    # Add some bonus and powerup bricks
                    if row == 2 and col % 2 == 0:
                        brick_type = "bonus"
                    elif row == 3 and col % 2 == 1:
                        brick_type = "powerup"
                
                bricks.append(Brick(x, y, brick_type))
        
        return bricks
    
    def _create_random_layout(self, rows: int, cols: int) -> List[Brick]:
        """Create a randomized layout of bricks"""
        bricks = []
        brick_types = ["normal", "normal", "normal", "hardy", "strong", "bonus", "powerup"]
        
        for row in range(rows):
            for col in range(cols):
                # Randomly skip some positions (20% chance)
                if random.random() < 0.2:
                    continue
                
                x = col * (Config.BRICK_WIDTH + 5) + 10
                y = row * (Config.BRICK_HEIGHT + 5) + 50
                
                # Select a random brick type
                brick_type = random.choice(brick_types)
                
                # Don't put unbreakable bricks in random layouts
                if brick_type == "unbreakable":
                    brick_type = "normal"
                
                bricks.append(Brick(x, y, brick_type))
                
        return bricks

# =============== GAME STATE MANAGEMENT ===============

class GameState:
    """Base class for game states"""
    
    def __init__(self, game):
        self.game = game
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle pygame events"""
        pass
    
    def update(self) -> None:
        """Update game state"""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw current state to the screen"""
        pass

class MenuState(GameState):
    """Main menu state"""
    
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Start Game", "High Scores", "Settings", "Quit"]
        self.selected_option = 0
        self.selected_difficulty = Config.MEDIUM
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle menu input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self._select_option()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    # Set difficulty
                    if event.unicode == "1":
                        self.selected_difficulty = Config.EASY
                    elif event.unicode == "2":
                        self.selected_difficulty = Config.MEDIUM
                    elif event.unicode == "3":
                        self.selected_difficulty = Config.HARD
    
    def _select_option(self) -> None:
        """Handle menu option selection"""
        if self.options[self.selected_option] == "Start Game":
            self.game.start_game(self.selected_difficulty)
        elif self.options[self.selected_option] == "High Scores":
            self.game.set_state(HighScoreState(self.game))
        elif self.options[self.selected_option] == "Settings":
            self.game.set_state(SettingsState(self.game))
        elif self.options[self.selected_option] == "Quit":
            pygame.quit()
            sys.exit()
    
    def update(self) -> None:
        """Update menu state"""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw menu screen"""
        surface.fill(Config.BLACK)
        
        # Draw title
        title_font = AssetManager().get_font("title")
        title = title_font.render("BRICK BREAKER", True, Config.WHITE)
        title_rect = title.get_rect(centerx=Config.WIDTH // 2, y=50)
        surface.blit(title, title_rect)
        
        # Draw menu options
        menu_font = AssetManager().get_font("large")
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = Config.YELLOW
                text = f"> {option} <"
            else:
                color = Config.WHITE
                text = option
                
            option_text = menu_font.render(text, True, color)
            option_rect = option_text.get_rect(centerx=Config.WIDTH // 2, y=200 + i * 50)
            surface.blit(option_text, option_rect)
        
        # Draw difficulty selection
        diff_font = AssetManager().get_font("medium")
        diff_text = "Difficulty: "
        
        if self.selected_difficulty == Config.EASY:
            diff_text += "EASY"
            diff_color = Config.GREEN
        elif self.selected_difficulty == Config.MEDIUM:
            diff_text += "MEDIUM"
            diff_color = Config.YELLOW
        else:
            diff_text += "HARD"
            diff_color = Config.RED
            
        diff_label = diff_font.render(diff_text, True, diff_color)
        diff_rect = diff_label.get_rect(centerx=Config.WIDTH // 2, y=400)
        surface.blit(diff_label, diff_rect)
        
        # Draw controls help
        help_font = AssetManager().get_font("small")
        help_texts = [
            "Press 1-3 to change difficulty",
            "Press UP/DOWN to navigate",
            "Press ENTER to select",
            "In-game: LEFT/RIGHT to move, SPACE to launch ball",
            "Press P to pause during gameplay",
            "Press M to toggle control mode (keyboard/mouse)"
        ]
        
        for i, text in enumerate(help_texts):
            help_label = help_font.render(text, True, Config.GRAY)
            help_rect = help_label.get_rect(centerx=Config.WIDTH // 2, y=450 + i * 25)
            surface.blit(help_label, help_rect)

class PlayState(GameState):
    """Gameplay state"""
    
    def __init__(self, game, difficulty: int = Config.MEDIUM):
        super().__init__(game)
        self.difficulty = difficulty
        self.paused = False
        self.mouse_control = False
        self.level_manager = LevelManager()
        self.reset_level(1)
    
    def reset_level(self, level: int) -> None:
        """Reset the game state for a new level"""
        # Set up game objects
        self.paddle = Paddle((Config.WIDTH - Config.PADDLE_WIDTH) // 2, Config.HEIGHT - 50)
        self.ball = Ball(Config.WIDTH // 2, Config.HEIGHT // 2, self.difficulty)
        self.ball.attach_to_paddle(self.paddle)
        
        self.difficulty_settings = Config.get_difficulty_settings(self.difficulty)
        self.lives = self.difficulty_settings["lives"]
        self.score = self.game.score  # Keep score between levels
        self.level = level
        
        # Create bricks for this level
        self.bricks = self.level_manager.create_level(level)
        self.powerups = []
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle gameplay input"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Toggle pause
                    self.paused = not self.paused
                elif event.key == pygame.K_m:
                    # Toggle mouse control
                    self.mouse_control = not self.mouse_control
                elif event.key == pygame.K_SPACE:
                    # Launch ball if attached
                    if self.ball.attached:
                        self.ball.release(self.paddle)
                elif event.key == pygame.K_ESCAPE:
                    # Return to menu
                    self.game.set_state(MenuState(self.game))
    
    def update(self) -> None:
        """Update gameplay state"""
        if self.paused:
            return
            
        # Update paddle
        self.paddle.update(self.mouse_control)
        
        # Update ball and handle ball-paddle attachment
        if self.ball.attached:
            self.ball.rect.centerx = self.paddle.rect.centerx + self.ball.attach_offset
            self.ball.rect.bottom = self.paddle.rect.top
        else:
            # Update ball and check if it's still in play
            if not self.ball.update():
                # Ball fell off the bottom
                self.lives -= 1
                if self.lives <= 0:
                    # Game over
                    self.game.score = self.score
                    AssetManager().play_sound("game_over")
                    self.game.set_state(GameOverState(self.game))
                else:
                    # Reset ball
                    self.ball.attach_to_paddle(self.paddle)
        
        # Handle ball-paddle collisions
        self.ball.handle_paddle_collision(self.paddle)
        
        # Handle ball-brick collisions
        for brick in self.bricks[:]:  # Create a copy to safely remove during iteration
            if not brick.active:
                continue
                
            if self.ball.handle_brick_collision(brick):
                # Brick was hit
                broken, powerup_type = brick.hit()
                
                if broken:
                    # Award points
                    self.score += brick.points * self.difficulty_settings["score_multiplier"]
                    AssetManager().play_sound("brick_hit")
                    
                    # Spawn power-up if brick had one
                    if powerup_type:
                        self.powerups.append(
                            PowerUp(brick.rect.centerx, brick.rect.centery, powerup_type)
                        )
        
        # Update power-ups
        for powerup in self.powerups[:]:
            if not powerup.update():
                # Power-up fell off screen
                self.powerups.remove(powerup)
                continue
                
            if powerup.rect.colliderect(self.paddle.rect):
                # Power-up collected
                AssetManager().play_sound("power_up")
                
                if powerup.powerup_type == "extra_life":
                    self.lives += 1
                elif powerup.powerup_type in ("expand", "shrink"):
                    self.paddle.apply_powerup(powerup.powerup_type)
                elif powerup.powerup_type in ("speed_up", "slow_down", "fire_ball"):
                    self.ball.apply_powerup(powerup.powerup_type)
                
                self.powerups.remove(powerup)
        
        # Check if level is complete (all breakable bricks destroyed)
        breakable_bricks_left = any(
            brick.active and brick.brick_type != "unbreakable" 
            for brick in self.bricks
        )
        
        if not breakable_bricks_left:
            # Level complete
            if self.level < Config.MAX_LEVEL:
                # Advance to next level
                AssetManager().play_sound("level_complete")
                self.game.score = self.score
                self.reset_level(self.level + 1)
            else:
                # Game complete
                AssetManager().play_sound("level_complete")
                self.game.score = self.score
                self.game.set_state(GameCompleteState(self.game))
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw gameplay screen"""
        surface.fill(Config.BLACK)
        
        # Draw UI elements
        self._draw_ui(surface)
        
        # Draw game objects
        self.paddle.draw(surface)
        self.ball.draw(surface)
        
        for brick in self.bricks:
            brick.draw(surface)
            
        for powerup in self.powerups:
            powerup.draw(surface)
        
        # Draw pause overlay if paused
        if self.paused:
            self._draw_pause_overlay(surface)
    
    def _draw_ui(self, surface: pygame.Surface) -> None:
        """Draw UI elements (score, lives, level)"""
        ui_font = AssetManager().get_font("medium")
        
        # Draw score
        score_text = f"Score: {self.score}"
        score_label = ui_font.render(score_text, True, Config.WHITE)
        surface.blit(score_label, (20, 10))
        
        # Draw lives
        lives_text = f"Lives: {self.lives}"
        lives_label = ui_font.render(lives_text, True, Config.WHITE)
        lives_rect = lives_label.get_rect(midtop=(Config.WIDTH // 2, 10))
        surface.blit(lives_label, lives_rect)
        
        # Draw level
        level_text = f"Level: {self.level}"
        level_label = ui_font.render(level_text, True, Config.WHITE)
        level_rect = level_label.get_rect(right=Config.WIDTH - 20, top=10)
        surface.blit(level_label, level_rect)
        
        # Draw control mode indicator
        mode_text = "Mouse Control" if self.mouse_control else "Keyboard Control"
        mode_label = AssetManager().get_font("small").render(mode_text, True, Config.GRAY)
        mode_rect = mode_label.get_rect(right=Config.WIDTH - 20, top=40)
        surface.blit(mode_label, mode_rect)
    
    def _draw_pause_overlay(self, surface: pygame.Surface) -> None:
        """Draw pause screen overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        surface.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_font = AssetManager().get_font("large")
        pause_text = pause_font.render("PAUSED", True, Config.WHITE)
        pause_rect = pause_text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
        surface.blit(pause_text, pause_rect)
        
        # Draw help text
        help_font = AssetManager().get_font("small")
        help_texts = [
            "Press P to resume",
            "Press ESC to return to menu",
            "Press M to toggle control mode"
        ]
        
        for i, text in enumerate(help_texts):
            help_label = help_font.render(text, True, Config.WHITE)
            help_rect = help_label.get_rect(
                centerx=Config.WIDTH // 2, 
                y=Config.HEIGHT // 2 + 50 + i * 30
            )
            surface.blit(help_label, help_rect)

class GameOverState(GameState):
    """Game over state"""
    
    def __init__(self, game):
        super().__init__(game)
        self.final_score = game.score
        self.name = ""
        self.name_entered = False
        self.high_scores = self._load_high_scores()
        self.is_high_score = self._check_if_high_score()
    
    def _load_high_scores(self) -> List[Dict[str, Any]]:
        """Load high scores from file"""
        try:
            if os.path.exists(Config.HIGH_SCORES_FILE):
                with open(Config.HIGH_SCORES_FILE, "r") as f:
                    return json.load(f)
            return []
        except Exception:
            return []
    
    def _save_high_scores(self) -> None:
        """Save high scores to file"""
        try:
            with open(Config.HIGH_SCORES_FILE, "w") as f:
                json.dump(self.high_scores, f)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    def _check_if_high_score(self) -> bool:
        """Check if current score is a high score"""
        if len(self.high_scores) < 10:
            return True
        return any(score["score"] < self.final_score for score in self.high_scores)
    
    def _add_high_score(self) -> None:
        """Add current score to high scores"""
        name = self.name if self.name else "Unknown"
        
        self.high_scores.append({
            "name": name,
            "score": self.final_score,
            "date": pygame.time.get_ticks()  # Simple timestamp
        })
        
        # Sort by score (descending) and keep only top 10
        self.high_scores = sorted(
            self.high_scores, 
            key=lambda x: x["score"], 
            reverse=True
        )[:10]
        
        self._save_high_scores()
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle input for game over screen"""
        for event in events:
            if self.is_high_score and not self.name_entered:
                # Input name for high score
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self._add_high_score()
                        self.name_entered = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.unicode.isalnum() and len(self.name) < 10:
                        self.name += event.unicode
            else:
                # After name entry or if not a high score
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.game.set_state(MenuState(self.game))
    
    def update(self) -> None:
        """Update game over state"""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw game over screen"""
        surface.fill(Config.BLACK)
        
        # Draw game over text
        game_over_font = AssetManager().get_font("title")
        game_over_text = game_over_font.render("GAME OVER", True, Config.RED)
        game_over_rect = game_over_text.get_rect(centerx=Config.WIDTH // 2, y=100)
        surface.blit(game_over_text, game_over_rect)
        
        # Draw score
        score_font = AssetManager().get_font("large")
        score_text = score_font.render(f"Final Score: {self.final_score}", True, Config.WHITE)
        score_rect = score_text.get_rect(centerx=Config.WIDTH // 2, y=200)
        surface.blit(score_text, score_rect)
        
        if self.is_high_score:
            # Draw high score message
            high_score_font = AssetManager().get_font("medium")
            high_score_text = high_score_font.render("New High Score!", True, Config.YELLOW)
            high_score_rect = high_score_text.get_rect(centerx=Config.WIDTH // 2, y=250)
            surface.blit(high_score_text, high_score_rect)
            
            if not self.name_entered:
                # Draw name input field
                name_prompt = high_score_font.render("Enter your name:", True, Config.WHITE)
                name_prompt_rect = name_prompt.get_rect(centerx=Config.WIDTH // 2, y=300)
                surface.blit(name_prompt, name_prompt_rect)
                
                name_text = high_score_font.render(self.name + "_", True, Config.WHITE)
                name_rect = name_text.get_rect(centerx=Config.WIDTH // 2, y=340)
                
                # Draw input box
                input_box = pygame.Rect(0, 0, max(200, name_rect.width + 20), name_rect.height + 20)
                input_box.center = (Config.WIDTH // 2, 340)
                pygame.draw.rect(surface, Config.BLUE, input_box, 2)
                
                surface.blit(name_text, name_rect)
                
                # Draw instructions
                instructions = AssetManager().get_font("small").render(
                    "Type your name and press Enter", True, Config.GRAY
                )
                instructions_rect = instructions.get_rect(centerx=Config.WIDTH // 2, y=380)
                surface.blit(instructions, instructions_rect)
            else:
                # Draw continue prompt
                continue_font = AssetManager().get_font("medium")
                continue_text = continue_font.render(
                    "Press Enter to continue", True, Config.WHITE
                )
                continue_rect = continue_text.get_rect(centerx=Config.WIDTH // 2, y=350)
                surface.blit(continue_text, continue_rect)
        else:
            # Draw continue prompt
            continue_font = AssetManager().get_font("medium")
            continue_text = continue_font.render(
                "Press Enter to continue", True, Config.WHITE
            )
            continue_rect = continue_text.get_rect(centerx=Config.WIDTH // 2, y=300)
            surface.blit(continue_text, continue_rect)

class GameCompleteState(GameState):
    """Game complete state"""
    
    def __init__(self, game):
        super().__init__(game)
        self.final_score = game.score
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle input for game complete screen"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.game.set_state(MenuState(self.game))
    
    def update(self) -> None:
        """Update game complete state"""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw game complete screen"""
        surface.fill(Config.BLACK)
        
        # Draw congratulations text
        congrats_font = AssetManager().get_font("title")
        congrats_text = congrats_font.render("CONGRATULATIONS!", True, Config.GREEN)
        congrats_rect = congrats_text.get_rect(centerx=Config.WIDTH // 2, y=100)
        surface.blit(congrats_text, congrats_rect)
        
        # Draw completion message
        complete_font = AssetManager().get_font("large")
        complete_text = complete_font.render("You've completed all levels!", True, Config.WHITE)
        complete_rect = complete_text.get_rect(centerx=Config.WIDTH // 2, y=200)
        surface.blit(complete_text, complete_rect)
        
        # Draw final score
        score_font = AssetManager().get_font("medium")
        score_text = score_font.render(f"Final Score: {self.final_score}", True, Config.YELLOW)
        score_rect = score_text.get_rect(centerx=Config.WIDTH // 2, y=270)
        surface.blit(score_text, score_rect)
        
        # Draw continue prompt
        continue_font = AssetManager().get_font("medium")
        continue_text = continue_font.render("Press Enter to return to menu", True, Config.WHITE)
        continue_rect = continue_text.get_rect(centerx=Config.WIDTH // 2, y=350)
        surface.blit(continue_text, continue_rect)

class HighScoreState(GameState):
    """High scores state"""
    
    def __init__(self, game):
        super().__init__(game)
        self.high_scores = self._load_high_scores()
    
    def _load_high_scores(self) -> List[Dict[str, Any]]:
        """Load high scores from file"""
        try:
            if os.path.exists(Config.HIGH_SCORES_FILE):
                with open(Config.HIGH_SCORES_FILE, "r") as f:
                    return json.load(f)
            return []
        except Exception:
            return []
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle input for high scores screen"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.game.set_state(MenuState(self.game))
    
    def update(self) -> None:
        """Update high scores state"""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw high scores screen"""
        surface.fill(Config.BLACK)
        
        # Draw title
        title_font = AssetManager().get_font("large")
        title_text = title_font.render("HIGH SCORES", True, Config.YELLOW)
        title_rect = title_text.get_rect(centerx=Config.WIDTH // 2, y=50)
        surface.blit(title_text, title_rect)
        
        # Draw high scores
        score_font = AssetManager().get_font("medium")
        
        if not self.high_scores:
            # No high scores yet
            no_scores_text = score_font.render("No high scores yet!", True, Config.WHITE)
            no_scores_rect = no_scores_text.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT // 2))
            surface.blit(no_scores_text, no_scores_rect)
        else:
            # Draw score headers
            header_font = AssetManager().get_font("medium")
            header_rank = header_font.render("Rank", True, Config.CYAN)
            header_name = header_font.render("Name", True, Config.CYAN)
            header_score = header_font.render("Score", True, Config.CYAN)
            
            surface.blit(header_rank, (150, 120))
            surface.blit(header_name, (250, 120))
            surface.blit(header_score, (550, 120))
            
            # Draw horizontal line
            pygame.draw.line(surface, Config.WHITE, (100, 150), (700, 150), 2)
            
            # Draw each score
            for i, score in enumerate(self.high_scores):
                y_pos = 180 + i * 40
                
                # Rank
                rank_text = score_font.render(f"{i + 1}.", True, Config.WHITE)
                surface.blit(rank_text, (150, y_pos))
                
                # Name
                name_text = score_font.render(score["name"], True, Config.WHITE)
                surface.blit(name_text, (250, y_pos))
                
                # Score
                score_text = score_font.render(str(score["score"]), True, Config.WHITE)
                surface.blit(score_text, (550, y_pos))
        
        # Draw back instruction
        back_font = AssetManager().get_font("small")
        back_text = back_font.render("Press ESC or ENTER to return to menu", True, Config.GRAY)
        back_rect = back_text.get_rect(centerx=Config.WIDTH // 2, bottom=Config.HEIGHT - 20)
        surface.blit(back_text, back_rect)

class SettingsState(GameState):
    """Settings state"""
    
    def __init__(self, game):
        super().__init__(game)
        self.options = ["Mouse Control: Off", "Sound: On", "Back to Menu"]
        self.selected_option = 0
        
        # Load current settings
        self.mouse_control = game.mouse_control
        self.sound_enabled = game.sound_enabled
        
        # Update option text based on current settings
        self._update_option_text()
    
    def _update_option_text(self) -> None:
        """Update option text based on current settings"""
        self.options[0] = f"Mouse Control: {'On' if self.mouse_control else 'Off'}"
        self.options[1] = f"Sound: {'On' if self.sound_enabled else 'Off'}"
    
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Handle input for settings screen"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._select_option()
                elif event.key == pygame.K_ESCAPE:
                    self._save_settings()
                    self.game.set_state(MenuState(self.game))
    
    def _select_option(self) -> None:
        """Handle option selection"""
        if self.selected_option == 0:
            # Toggle mouse control
            self.mouse_control = not self.mouse_control
            self._update_option_text()
        elif self.selected_option == 1:
            # Toggle sound
            self.sound_enabled = not self.sound_enabled
            self._update_option_text()
        elif self.selected_option == 2:
            # Back to menu
            self._save_settings()
            self.game.set_state(MenuState(self.game))
    
    def _save_settings(self) -> None:
        """Save settings to game object"""
        self.game.mouse_control = self.mouse_control
        self.game.sound_enabled = self.sound_enabled
        
        # Apply sound setting
        if not self.sound_enabled:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
    
    def update(self) -> None:
        """Update settings state"""
        pass
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw settings screen"""
        surface.fill(Config.BLACK)
        
        # Draw title
        title_font = AssetManager().get_font("large")
        title_text = title_font.render("SETTINGS", True, Config.WHITE)
        title_rect = title_text.get_rect(centerx=Config.WIDTH // 2, y=100)
        surface.blit(title_text, title_rect)
        
        # Draw options
        option_font = AssetManager().get_font("medium")
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = Config.YELLOW
                text = f"> {option} <"
            else:
                color = Config.WHITE
                text = option
                
            option_text = option_font.render(text, True, color)
            option_rect = option_text.get_rect(centerx=Config.WIDTH // 2, y=200 + i * 50)
            surface.blit(option_text, option_rect)
        
        # Draw help text
        help_font = AssetManager().get_font("small")
        help_text = "Use UP/DOWN to navigate, ENTER to select, ESC to save and exit"
        help_label = help_font.render(help_text, True, Config.GRAY)
        help_rect = help_label.get_rect(centerx=Config.WIDTH // 2, bottom=Config.HEIGHT - 20)
        surface.blit(help_label, help_rect)

# =============== MAIN GAME CLASS ===============

class BrickBreakerGame:
    """Main game class"""
    
    def __init__(self):
        pygame.display.set_caption(Config.TITLE)
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = None
        self.score = 0
        self.mouse_control = False
        self.sound_enabled = True
        
        # Initialize asset manager
        self.assets = AssetManager()
        
        # Set initial state
        self.set_state(MenuState(self))
    
    def set_state(self, state: GameState) -> None:
        """Change the current game state"""
        self.current_state = state
    
    def start_game(self, difficulty: int = Config.MEDIUM) -> None:
        """Start a new game with the specified difficulty"""
        self.score = 0
        self.set_state(PlayState(self, difficulty))
    
    def run(self) -> None:
        """Main game loop"""
        while self.running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Let current state handle events
            self.current_state.handle_events(events)
            
            # Update current state
            self.current_state.update()
            
            # Draw current state
            self.current_state.draw(self.screen)
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(Config.FPS)

# =============== MAIN ENTRY POINT ===============

def main():
    """Main entry point"""
    try:
        game = BrickBreakerGame()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
