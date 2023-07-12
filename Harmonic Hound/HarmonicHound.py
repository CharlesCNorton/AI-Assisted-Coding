import pyaudio
import numpy as np
from scipy.fftpack import fft
import threading
from collections import deque
from scipy.signal import find_peaks, butter, lfilter
import time
from colorama import init, Fore, Back, Style

# Initial setup for colored console output
init()

# Configuration
RATE = 44100
SMOOTHING_WINDOW_SIZE = 10
MIN_NOTE_DURATION = 0.4
NOISE_LEVEL = 0.001
SENSITIVITY = 0.97

# Create a dictionary of note frequencies, assuming A4 = 440 Hz
A4_FREQ = 440
NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
NOTE_FREQS = {note + str(octave): A4_FREQ * 2 ** ((i - 9 + 12 * (octave - 4)) / 12) for octave in range(0, 8) for i, note in enumerate(NOTES)}

# Create a dictionary of colors for each note
NOTE_COLORS = {
    'A': Fore.RED,
    'A#': Fore.GREEN,
    'B': Fore.YELLOW,
    'C': Fore.BLUE,
    'C#': Fore.MAGENTA,
    'D': Fore.CYAN,
    'D#': Fore.RED,
    'E': Fore.GREEN,
    'F': Fore.YELLOW,
    'F#': Fore.BLUE,
    'G': Fore.MAGENTA,
    'G#': Fore.CYAN,
    'Note out of defined range': Style.RESET_ALL,
    'reset': Style.RESET_ALL
}

# Define a function to map any frequency to the nearest note
def freq_to_note(freq):
    # Find the note that is closest in frequency
    closest_note = min(NOTE_FREQS, key=lambda note: abs(freq - NOTE_FREQS[note]))
    return closest_note

# Define a deque for smoothing the audio data over time
audio_data_buffer = deque(maxlen=SMOOTHING_WINDOW_SIZE)

# Variable to hold the last printed note
last_note = None

# Variable to hold the start time of the last note
note_start_time = time.time()

# Variable to hold the noise level
noise_level = NOISE_LEVEL

# Variable to check if the user wants to quit
quit_flag = False

# Function to create a butterworth bandpass filter
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Define a function to run in a separate thread for user interaction
def user_interaction():
    global quit_flag
    while True:
        user_input = input()
        if user_input.lower() == 'q':
            quit_flag = True
            break

# Start the user interaction thread
user_interaction_thread = threading.Thread(target=user_interaction)
user_interaction_thread.start()

# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the callback function that will be called in a loop
def callback(in_data, frame_count, time_info, status):
    global last_note, note_start_time, noise_level
    audio_data = np.frombuffer(in_data, dtype=np.float32)

    # Filter the audio data
    audio_data = butter_bandpass_filter(audio_data, 27.5, 4186, RATE, order=3)

    # Add the audio data to the buffer
    audio_data_buffer.append(audio_data)
    # Smooth the audio data over time
    smoothed_audio_data = np.mean(audio_data_buffer, axis=0)

    # Calculate the volume
    volume = np.linalg.norm(smoothed_audio_data)

    # Update the noise level
    new_noise_level = noise_level * SENSITIVITY + volume * (1 - SENSITIVITY)
    # Check for potential overflow
    if np.isfinite(new_noise_level):
        noise_level = new_noise_level

    # Perform FFT
    fft_data = np.abs(fft(smoothed_audio_data))

    # Find peaks
    peaks, _ = find_peaks(fft_data, distance=20)
    if peaks.size:
        freq_bin = peaks[0]  # pick the first (highest) peak
        # Compute the frequency of the bin in Hz
        freq = freq_bin * RATE / len(smoothed_audio_data)

        # Only print the note if the volume is above a certain threshold
        if volume > noise_level:
            # Convert frequency to note
            note = freq_to_note(freq)
            if note != last_note:
                # Print the note if it has been held for long enough
                if time.time() - note_start_time > MIN_NOTE_DURATION:
                    note_core = note[:-1] if '#' in note else note[:-1]
                    color = NOTE_COLORS[note_core] if note_core in NOTE_COLORS else NOTE_COLORS['Note out of defined range']
                    print(color + "Note: {}, Freq: {:.2f} Hz".format(note, freq) + NOTE_COLORS['reset'])
                # Update the last note and its start time
                last_note = note
                note_start_time = time.time()

    # The callback function must return the output data and a flag indicating whether to continue
    return (in_data, pyaudio.paContinue)

try:
    # Open a stream and start it
    stream = p.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=1024,
                    stream_callback=callback)

    # Start the audio stream
    stream.start_stream()

    # Print a welcome message
    print("\\nWelcome to the Digital Piano Assistant!")
    print("The program will print the note it hears from your digital piano.")
    print("Press 'q' to quit the program at any time.\\n")

    # Let the program run until the user decides to quit
    while True:
        try:
            if input() == 'q':
                break
            time.sleep(0.1)
        except (EOFError, KeyboardInterrupt):
            break

    # Stop the audio stream
    stream.stop_stream()
    stream.close()

    # Terminate the audio host API
    p.terminate()

except Exception as e:
    print(f"An error occurred: {e}")
