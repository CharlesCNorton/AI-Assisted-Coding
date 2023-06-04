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
        self.amplitude = tk.DoubleVar(value=0.0)
        self.frequency = tk.DoubleVar(value=14000)
        self.noise_amplitude = tk.DoubleVar(value=0.0)

        self.freq_scale = tk.Scale(master, from_=1000, to=20000,
                                   length=600, resolution=10,
                                   orient=tk.HORIZONTAL,
                                   variable=self.frequency,
                                   label="Frequency (Hz)",
                                   command=self.update_frequency)
        self.freq_scale.pack()

        self.volume_scale = tk.Scale(master, from_=0.0, to=1.0,
                                     length=600, resolution=0.01,
                                     orient=tk.HORIZONTAL,
                                     variable=self.amplitude,
                                     label="Volume",
                                     command=self.update_amplitude)
        self.volume_scale.pack()

        self.noise_scale = tk.Scale(master, from_=0.0, to=0.25,
                                    length=600, resolution=0.01,
                                    orient=tk.HORIZONTAL,
                                    variable=self.noise_amplitude,
                                    label="White Noise Volume",
                                    command=self.update_noise_amplitude)
        self.noise_scale.pack()

        self.sound_on = tk.BooleanVar(value=False)
        self.on_button = tk.Button(master, text="Turn On", command=self.turn_on)
        self.on_button.pack()
        self.off_button = tk.Button(master, text="Turn Off", command=self.turn_off)
        self.off_button.pack()

        self.myarray = self.generate_tone(self.frequency.get(), self.amplitude.get())
        self.stream = sd.OutputStream(callback=self.callback, samplerate=self.fs)

    def generate_tone(self, frequency, amplitude):
        duration = 5.0
        t = np.arange(self.fs * duration) / self.fs
        tone = amplitude * np.sin(2 * np.pi * frequency * t)
        tone = self.bandpass_filter(tone, frequency)
        tone += self.noise_amplitude.get() * np.random.normal(0, 1, len(t))
        return tone.reshape(-1, 1)

    def bandpass_filter(self, data, center_freq):
        order = 2
        lowcut = center_freq - 50
        highcut = center_freq + 50

        nyquist_freq = 0.5 * self.fs
        low = lowcut / nyquist_freq
        high = highcut / nyquist_freq
        b, a = butter(order, [low, high], btype='band')

        return lfilter(b, a, data)

    def update_frequency(self, event):
        self.myarray = self.generate_tone(self.frequency.get(), self.amplitude.get())

    def update_amplitude(self, event):
        self.myarray = self.generate_tone(self.frequency.get(), self.amplitude.get())

    def update_noise_amplitude(self, event):
        self.myarray = self.generate_tone(self.frequency.get(), self.amplitude.get())

    def callback(self, outdata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        frames_needed = min(len(self.myarray), frames)
        outdata[:frames_needed] = self.myarray[:frames_needed] * self.sound_on.get()
        self.myarray = np.roll(self.myarray, -frames_needed)

    def turn_on(self):
        self.sound_on.set(True)
        self.stream.start()

    def turn_off(self):
        self.sound_on.set(False)
        self.stream.stop()

root = tk.Tk()
my_app = TinnitusApp(root)
root.mainloop()
