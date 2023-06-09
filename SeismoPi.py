# Created with the assistance of GPT-4 on 6/8/2023
# This name combines the functionality of the program (Seismo- from seismometer, measuring vibrations) with the hardware it's designed for (the Raspberry Pi).

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from sense_hat import SenseHat
import numpy as np
import sys
import datetime
import collections

# Initialize the SenseHat module
try:
    sense = SenseHat()
except Exception as e:
    print(f"Error initializing SenseHat module: {e}")
    sys.exit()

# Initialize a deque to store acceleration values
acceleration_values = collections.deque(maxlen=100)

# Function to draw a bar in 3D using the OpenGL library
def draw_bar(height, color):
    glColor3f(*color)
    glBegin(GL_QUADS)

    # The vertices for each face of the bar are defined here, with each face being a quadrilateral
    # Front face
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, height, 0)
    glVertex3f(0, height, 0)

    # Back face
    glVertex3f(0, 0, -1)
    glVertex3f(1, 0, -1)
    glVertex3f(1, height, -1)
    glVertex3f(0, height, -1)

    # Left face
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -1)
    glVertex3f(0, height, -1)
    glVertex3f(0, height, 0)

    # Right face
    glVertex3f(1, 0, 0)
    glVertex3f(1, 0, -1)
    glVertex3f(1, height, -1)
    glVertex3f(1, height, 0)

    glEnd()

# Function to draw text on the screen, utilizing Pygame for font rendering and OpenGL to display
def draw_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
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
    glTexCoord(0, 0); glVertex(x, y)
    glTexCoord(1, 0); glVertex(x + width, y)
    glTexCoord(1, 1); glVertex(x + width, y + height)
    glTexCoord(0, 1); glVertex(x, y + height)
    glEnd()

    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)
    glDeleteTextures(1, [texid])

# Function to draw a line graph using OpenGL
def draw_line_graph(values, color):
    glColor3f(*color)
    glBegin(GL_LINE_STRIP)
    for i, value in enumerate(values):
        glVertex3f(i / len(values), value, 0)
    glEnd()

# The main function where the Pygame and OpenGL setup happens, as well as the main game loop
def main():
    pygame.init()  # Pygame initialization
    display = (800, 600)  # Defining the size of the display
    pygame.display.set_caption('Raspberry Pi Seismometer')  # Set the window title
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # Setting up the display
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Setting up the perspective for OpenGL
    glTranslatef(-0.5, -1.0, -5)  # Shifting the perspective

    font = pygame.font.Font(None, 36)  # Setting up the font for text rendering
    text_color = (255, 255, 255)  # Color of the text
    bar_color = (0, 1, 1)  # Color of the bar

    # Open the log file
    try:
        with open('seismometer_log.txt', 'w') as log_file:
            # Main game loop
            while True:
                for event in pygame.event.get():
                    # Close the program when the exit button is pressed
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen

                # Get raw acceleration data from the SenseHat module
                raw = sense.get_accelerometer_raw()
                total_acceleration = np.linalg.norm(list(raw.values()))  # Calculating the total acceleration

                # Log the data with a timestamp
                timestamp = datetime.datetime.now()
                log_file.write(f'{timestamp}, {total_acceleration}, {raw["x"]}, {raw["y"]}, {raw["z"]}\n')

                # Add the total acceleration to the deque
                acceleration_values.append(total_acceleration)

                # Scale the bar height according to the total acceleration
                bar_height = total_acceleration / 10
                draw_bar(bar_height, bar_color)  # Draw the bar

                # Draw the line graph
                draw_line_graph(acceleration_values, bar_color)

                # Switch to 2D mode to display the text
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                gluOrtho2D(0, display[0], 0, display[1])
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()

                # Creating text strings for the total acceleration and its components along X, Y, and Z axes
                total_acceleration_text = f"Total Acceleration (g): {total_acceleration:.2f}"
                x_text = f"X: {raw['x']:.2f} g"
                y_text = f"Y: {raw['y']:.2f} g"
                z_text = f"Z: {raw['z']:.2f} g"

                # Display the text strings on the screen
                draw_text(total_acceleration_text, 10, display[1] - 50, font, text_color)
                draw_text(x_text, 10, display[1] - 90, font, text_color)
                draw_text(y_text, 10, display[1] - 130, font, text_color)
                draw_text(z_text, 10, display[1] - 170, font, text_color)

                # Display labels for the bar graph
                draw_text("Total Acceleration", 90, 30, font, bar_color)
                draw_text("X", 30, 30, font, (1, 0, 0))
                draw_text("Y", 50, 30, font, (0, 1, 0))
                draw_text("Z", 70, 30, font, (0, 0, 1))

                # Switch back to 3D mode
                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPopMatrix()

                pygame.display.flip()  # Update the display
                pygame.time.wait(10)  # Pause for 10 milliseconds

    except Exception as e:
        print(f"Error opening log file: {e}")
        sys.exit()

if __name__ == "__main__":
    main()
