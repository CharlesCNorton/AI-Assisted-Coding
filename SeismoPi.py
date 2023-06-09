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

# Other functions remain the same...

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
