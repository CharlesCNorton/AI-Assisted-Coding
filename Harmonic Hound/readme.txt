# Harmonic Hound

Harmonic Hound is a real-time note recognition program that listens to your digital piano or any musical instrument and prints out the musical notes being played, along with their frequencies. It uses the PyAudio library to capture audio data, performs a Fast Fourier Transform (FFT) to analyze the frequencies present, and identifies the note that corresponds to the dominant frequency.

## Requirements

- Python 3.6 or later
- PyAudio
- NumPy
- SciPy
- colorama
- A microphone or other audio input device

## Usage

1. Ensure that your microphone or audio input device is connected and working.
2. Run the script using Python 3: `python note_recognizer_improved.py`
3. Play notes on your instrument. The program will print out the note and its frequency.
4. Press 'q' to quit the program at any time.

Please note that the program assumes a standard tuning of A4 = 440 Hz.

Enjoy making music with Harmonic Hound!
