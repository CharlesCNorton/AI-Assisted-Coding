import numpy as np
import sounddevice as sd
import tkinter as tk
from scipy.signal import butter, lfilter
import sys

class TinnitusApp:
    def __init__(self, master):
        self.master = master
        master.title("Tinnitus Relief App")
        self.fs = 192000  # Sample rate

        # Initialize control variables
        self.amplitude = tk.DoubleVar(value=0.0)
        self.frequency = tk.DoubleVar(value=14000)
        self.noise_amplitude = tk.DoubleVar(value=0.0)

        # Create control widgets
        self.create_widgets()

        # Initialize audio data and output stream
        self.myarray = self.generate_tone()
        self.stream = sd.OutputStream(callback=self.callback, samplerate=self.fs)

    def create_widgets(self):
        """Create and pack control widgets"""
        self.freq_scale = self.create_scale(from_=1000, to=20000, resolution=10,
                                            variable=self.frequency, label="Frequency (Hz)")
        self.volume_scale = self.create_scale(from_=0.0, to=1.0, resolution=0.01,
                                              variable=self.amplitude, label="Volume")
        self.noise_scale = self.create_scale(from_=0.0, to=0.25, resolution=0.01,
                                             variable=self.noise_amplitude, label="White Noise Volume")
        self.sound_on = tk.BooleanVar(value=False)
        self.on_button = tk.Button(self.master, text="Turn On", command=self.turn_on)
        self.on_button.pack()
        self.off_button = tk.Button(self.master, text="Turn Off", command=self.turn_off)
        self.off_button.pack()

    def create_scale(self, **kwargs):
        """Create and pack a tkinter Scale widget with a command to update the tone"""
        scale = tk.Scale(self.master, length=600, orient=tk.HORIZONTAL, command=self.update_tone, **kwargs)
        scale.pack()
        return scale

    def generate_tone(self):
        """Generate a tone with current control variables"""
        duration = 5.0
        t = np.arange(self.fs * duration) / self.fs
        tone = self.amplitude.get() * np.sin(2 * np.pi * self.frequency.get() * t)
        tone = self.bandpass_filter(tone)
        tone += self.noise_amplitude.get() * np.random.normal(0, 1, len(t))
        return tone.reshape(-1, 1)

    def bandpass_filter(self, data):
        """Apply a bandpass filter to the data"""
        order = 2
        center_freq = self.frequency.get()
        lowcut = center_freq - 50
        highcut = center_freq + 50
        nyquist_freq = 0.5 * self.fs
        low = lowcut / nyquist_freq
        high = highcut / nyquist_freq
        b, a = butter(order, [low, high], btype='band')
        return lfilter(b, a, data)

    def update_tone(self, event):
        """Update the tone with current control variables"""
        self.myarray = self.generate_tone()

    def callback(self, outdata, frames, time, status):
        """Callback for the audio output stream"""
        if status:
            print(status, file=sys.stderr)
        frames_needed = min(len(self.myarray), frames)
        outdata[:frames_needed] = self.myarray[:frames_needed] * self.sound_on.get()
        self.myarray = np.roll(self.myarray, -frames_needed)

    def turn_on(self):
        """Start the audio output stream"""
        self.sound_on.set(True)
        self.stream.start()

    def turn_off(self):
        """Stop the audio output stream"""
        self.sound_on.set(False)
        self.stream.stop()

def main():
    """Create and run the tinnitus relief application"""
    try:
        root = tk.Tk()
        app = TinnitusApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
