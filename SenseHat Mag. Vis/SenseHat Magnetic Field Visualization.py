import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from sense_hat import SenseHat, SenseHatError
import numpy as np
import sys

class MyPygameApp:

    def __init__(self):
        # Initialize the SenseHat module
        try:
            self.sense = SenseHat()
        except SenseHatError as err:
            sys.exit(f"Failed to initialize SenseHat: {err}")

        # Initialize Pygame
        pygame.init()

        # Define Colors
        self.text_color = (255, 255, 255)
        self.bar_color = (0, 1, 1)

        # Define the display
        self.display = (800, 600)

        # Create screen
        try:
            self.screen = pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        except pygame.error as err:
            sys.exit(f"Failed to create display: {err}")

        # Define font
        self.font = pygame.font.Font(None, 36)

        # Set up OpenGL
        self.setup_opengl()

    def setup_opengl(self):
        # Set up the perspective for OpenGL
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)

        # Shifting the perspective
        glTranslatef(-0.5, -1.0, -5)

    def run(self):
        while True:
            # Main game loop
            self.handle_events()
            self.clear_screen()

            # Draw bar and text
            self.draw_content()

            # Update screen
            pygame.display.flip()

            # Pause for 10 milliseconds
            pygame.time.wait(10)

    def handle_events(self):
        for event in pygame.event.get():
            # Close the program when the exit button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def clear_screen(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def draw_content(self):
        try:
            raw = self.sense.get_compass_raw()
            total_magnetic_strength = np.linalg.norm(list(raw.values()))
        except SenseHatError as err:
            sys.exit(f"Failed to get data from SenseHat: {err}")

        # Scale the bar height according to the total magnetic field strength
        bar_height = total_magnetic_strength / 100
        self.draw_bar(bar_height, self.bar_color)

        # Creating text strings for the total magnetic strength and its components along X, Y, and Z axes
        total_magnetic_strength_text = f"Total Magnetic Field Strength (µT): {total_magnetic_strength:.2f}"
        x_text = f"X: {raw['x']:.2f} µT"
        y_text = f"Y: {raw['y']:.2f} µT"
        z_text = f"Z: {raw['z']:.2f} µT"

        # Switch to 2D mode to display the text
        self.switch_to_2d()
        self.draw_text(total_magnetic_strength_text, 10, self.display[1] - 50)
        self.draw_text(x_text, 10, self.display[1] - 90)
        self.draw_text(y_text, 10, self.display[1] - 130)
        self.draw_text(z_text, 10, self.display[1] - 170)
        self.draw_bar_labels()
        self.switch_to_3d()

    def draw_bar(self, height, color):
        glColor3f(*color)
        glBegin(GL_QUADS)

        # The vertices for each face of the bar are defined here, with each face being a quadrilateral
        # Front face
        self.draw_face(0, 0, 0, 1, 0, 0, 1, height, 0, 0, height, 0)

        # Back face
        self.draw_face(0, 0, -1, 1, 0, -1, 1, height, -1, 0, height, -1)

        # Left face
        self.draw_face(0, 0, 0, 0, 0, -1, 0, height, -1, 0, height, 0)

        # Right face
        self.draw_face(1, 0, 0, 1, 0, -1, 1, height, -1, 1, height, 0)

        glEnd()

    def draw_face(self, *vertices):
        for i in range(0, len(vertices), 3):
            glVertex3f(*vertices[i:i+3])

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, self.text_color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width, height = text_surface.get_size()

        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, texid)
        glBegin(GL_QUADS)
        self.draw_quad(x, y, width, height)
        glEnd()

        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        glDeleteTextures(1, [texid])

    def draw_quad(self, x, y, width, height):
        glTexCoord(0, 0); glVertex(x, y)
        glTexCoord(1, 0); glVertex(x + width, y)
        glTexCoord(1, 1); glVertex(x + width, y + height)
        glTexCoord(0, 1); glVertex(x, y + height)

    def draw_bar_labels(self):
        self.draw_text("Total Field Strength", 90, 30)
        self.draw_text("X", 30, 30)
        self.draw_text("Y", 50, 30)
        self.draw_text("Z", 70, 30)

    def switch_to_2d(self):
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, self.display[0], 0, self.display[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

    def switch_to_3d(self):
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

if __name__ == "__main__":
    app = MyPygameApp()
    app.run()
