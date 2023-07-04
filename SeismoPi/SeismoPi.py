import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from sense_hat import SenseHat
import numpy as np
import sys
import datetime
import collections
def initialize_sense_hat():
    try:
        return SenseHat()
    except Exception as e:
        print(f"Error initializing SenseHat module: {e}")
        sys.exit()
sense = initialize_sense_hat()
acceleration_values = collections.deque(maxlen=100)
def draw_bar(height, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    for x in [0, 1]:
        for y in [0, height]:
            for z in [0, -1]:
                glVertex3f(x, y, z)
    glEnd()
def setup_texture(text_surface):
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    width, height = text_surface.get_size()
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    return texid, width, height
def draw_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    texid, width, height = setup_texture(text_surface)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, texid)
    glBegin(GL_QUADS)
    for X, Y in [(0, 0), (1, 0), (1, 1), (0, 1)]:
        glTexCoord(X, Y); glVertex(x + X*width, y + Y*height)
    glEnd()
    glDisable(GL_BLEND)
    glDeleteTextures(1, [texid])
def draw_line_graph(values, color):
    glColor3f(*color)
    glBegin(GL_LINE_STRIP)
    for i, value in enumerate(values):
        glVertex3f(i / len(values), value, 0)
    glEnd()
def log_data(log_file, raw):
    total_acceleration = np.linalg.norm(list(raw.values()))
    timestamp = datetime.datetime.now()
    log_file.write(f'{timestamp}, {total_acceleration}, {raw["x"]}, {raw["y"]}, {raw["z"]}\n')
    return total_acceleration
def draw_graphs(bar_height, bar_color):
    draw_bar(bar_height, bar_color)
    draw_line_graph(acceleration_values, bar_color)
def draw_texts(display, font, text_color, total_acceleration, raw):
    draw_text(f"Total Acceleration (g): {total_acceleration:.2f}", 10, display[1] - 50, font, text_color)
    draw_text(f"X: {raw['x']:.2f} g", 10, display[1] - 90, font, text_color)
    draw_text(f"Y: {raw['y']:.2f} g", 10, display[1] - 130, font, text_color)
    draw_text(f"Z: {raw['z']:.2f} g", 10, display[1] - 170, font, text_color)
    draw_text("Total Acceleration", 90, 30, font, (0, 1, 1))
    draw_text("X", 30, 30, font, (1, 0, 0))
    draw_text("Y", 50, 30, font, (0, 1, 0))
    draw_text("Z", 70, 30, font, (0, 0, 1))
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_caption('Raspberry Pi Seismometer')
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(-0.5, -1.0, -5)
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)
    bar_color = (0, 1, 1)
    try:
        with open('seismometer_log.txt', 'w') as log_file:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                raw = sense.get_accelerometer_raw()
                total_acceleration = log_data(log_file, raw)
                acceleration_values.append(total_acceleration)
                bar_height = total_acceleration / 10
                draw_graphs(bar_height, bar_color)
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                gluOrtho2D(0, display[0], 0, display[1])
                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()
                draw_texts(display, font, text_color, total_acceleration, raw)
                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)
                glPopMatrix()
                pygame.display.flip()
                pygame.time.wait(10)
    except Exception as e:
        print(f"Error logging data or drawing graphics: {e}")
        pygame.quit()
        sys.exit()
if __name__ == "__main__":
    main()
