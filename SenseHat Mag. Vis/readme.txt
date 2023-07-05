# 3D Magnetic Field Strength Visualizer

This program uses the Sense Hat module to measure the magnetic field strength along the X, Y, and Z axes. The strength is visualized as a 3D bar using the OpenGL library and Pygame.

## Dependencies

The program requires the following Python libraries:
- Pygame
- OpenGL
- numpy
- sense_hat

## How to Run

1. Ensure that the dependencies are installed. You can install them using pip.
2. Run the program by executing `main.py` in Python.

## Program Description

The program draws a 3D bar whose height corresponds to the total magnetic field strength detected by the Sense Hat module. The program also displays the magnetic field strength along each of the X, Y, and Z axes as text on the screen.

The 3D graphics are handled by the OpenGL library, while Pygame is used for creating the display and handling events.

