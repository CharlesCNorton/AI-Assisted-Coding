Raspberry Pi Seismometer
--------------------------

This project is a simple seismometer that uses a Raspberry Pi and a Sense HAT to measure and log accelerometer data.

The seismometer displays a real-time graph of acceleration values on a Pygame window and logs the data to a file named 'seismometer_log.txt'.

How to run:
------------

1. Ensure you have all the necessary dependencies installed. These include:
    - Python 3
    - Pygame
    - PyOpenGL
    - numpy
    - sense_hat

2. Run the script using Python 3:
    ```bash
    python3 seismometer.py
    ```

Note: This code is intended to be run on a Raspberry Pi with a Sense HAT. If you're using a different setup, you may need to make adjustments to the code.