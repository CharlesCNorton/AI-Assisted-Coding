import os
import sounddevice as sd
import numpy as np
import torch
import librosa
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from typing import Tuple, Optional, List

FS = 16000
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if torch.cuda.is_available() else torch.float32
MODEL_PATH = "ENTER_PATH_TO_WHISPER_HERE"

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def list_audio_devices() -> None:
    """ Lists available audio input devices. """
    print("Available audio input devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            print(f"{i}: {device['name']}")

def select_audio_device() -> int:
    """ Allows the user to select an audio input device. """
    list_audio_devices()
    try:
        device_id = int(input("Enter the ID of the desired input device: "))
        print(f"Selected device ID: {device_id}")
        return device_id
    except ValueError:
        print("Invalid input. Please enter a valid device ID.")
        return select_audio_device()

def preprocess_audio(audio: np.ndarray) -> np.ndarray:
    """ Preprocesses the audio by normalizing and removing NaNs. """
    audio = np.nan_to_num(audio)
    normalized_audio = librosa.util.normalize(audio)
    return normalized_audio

def record_until_silence(device_id: int, silence_threshold: float = 0.01,
                         silence_duration: float = 2, initial_delay: float = 2) -> np.ndarray:
    """ Records audio from the device until silence is detected. """
    silent_frames = 0
    elapsed_time = 0
    recording = True
    recorded_audio = []

    def callback(indata, frames, time, status):
        nonlocal silent_frames, recording, elapsed_time
        if elapsed_time < initial_delay:
            elapsed_time += frames / FS
            return
        volume = np.abs(indata).mean()
        if volume < silence_threshold:
            silent_frames += 1
        else:
            silent_frames = 0
        if silent_frames > silence_duration * FS / 1024:
            recording = False

    with sd.InputStream(device=device_id, callback=callback, dtype='float32', channels=1, samplerate=FS):
        while recording:
            sd.sleep(100)
            recorded_audio.append(sd.rec(int(FS / 10), samplerate=FS, channels=1))
    recorded_audio_data = np.concatenate(recorded_audio, axis=0)
    return recorded_audio_data

def record_fixed_duration_audio(device_id: int, duration: float = 5) -> np.ndarray:
    """ Records audio for a fixed duration. """
    audio = sd.rec(int(duration * FS), samplerate=FS, channels=1, device=device_id, blocking=True)
    audio = audio.flatten()
    processed_audio = preprocess_audio(audio)
    return processed_audio

def setup_whisper_model() -> pipeline:
    """ Sets up the Whisper model pipeline. """
    model = AutoModelForSpeechSeq2Seq.from_pretrained(MODEL_PATH, torch_dtype=TORCH_DTYPE)
    model.to(DEVICE)
    processor = AutoProcessor.from_pretrained(MODEL_PATH)
    whisper_pipe = pipeline("automatic-speech-recognition", model=model,
                            tokenizer=processor.tokenizer, feature_extractor=processor.feature_extractor,
                            device=DEVICE)
    return whisper_pipe

def convert_to_mono(audio: np.ndarray) -> np.ndarray:
    """ Converts stereo audio to mono. """
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    return audio

def transcribe_audio(audio: np.ndarray, whisper_pipe: pipeline) -> str:
    """ Transcribes audio using the Whisper model. """
    audio = convert_to_mono(audio)
    result = whisper_pipe(audio)
    return result["text"]

def main_menu() -> str:
    """ Displays the main menu and returns the user's choice. """
    choices = {
        '1': "Begin Adaptive Duration Transcription",
        '2': "Begin Fixed Duration Transcription",
        '3': "Change Fixed Duration Settings",
        '4': "Exit"
    }
    for key, value in choices.items():
        print(f"{key}. {value}")
    return input("Enter your choice: ")

def calibrate(device_id: int, calibration_phrase: str = "test") -> Tuple[Optional[float], Optional[float]]:
    """ Calibrates the audio input device. """
    print(f"Please say '{calibration_phrase}' into the microphone and stay silent after.")
    audio = sd.rec(int(3 * FS), samplerate=FS, channels=1, device=device_id, blocking=True)
    audio = audio.flatten()
    if np.any(np.isnan(audio)) or np.all(audio == 0):
        print("Calibration failed: Invalid audio recorded.")
        return None, None
    ambient_noise = record_ambient_noise()
    speech_level = np.mean(np.abs(audio))
    silence_level = np.mean(np.abs(ambient_noise))
    threshold = max((speech_level + silence_level) / 2, 0.01)
    return threshold, silence_level

def record_ambient_noise(duration: float = 1) -> np.ndarray:
    """ Records ambient noise for calibration. """
    print("Recording ambient noise for calibration. Please be quiet...")
    ambient_noise = sd.rec(int(duration * FS), samplerate=FS, channels=1)
    sd.wait()
    return ambient_noise.flatten()

def set_fixed_duration() -> float:
    """ Sets the duration for fixed duration recording. """
    try:
        duration = float(input("Enter the duration for fixed recording in seconds: "))
        return duration
    except ValueError:
        print("Invalid input. Please enter a valid duration.")
        return set_fixed_duration()

def main() -> None:
    """ Main function to run the application. """
    whisper_pipe = setup_whisper_model()
    device_id = select_audio_device()
    fixed_duration = 5

    print("Starting calibration process...")
    threshold, silence_level = calibrate(device_id)
    if threshold is None:
        print("Calibration failed, please restart the application.")
        return

    while True:
        choice = main_menu()
        if choice == '1':
            print("Recording until silence is detected...")
            audio = record_until_silence(device_id, silence_threshold=threshold)
            processed_audio = preprocess_audio(audio)
            transcription = transcribe_audio(processed_audio, whisper_pipe)
            print("Transcription complete.")
            print("Transcription:", transcription)
        elif choice == '2':
            print(f"Recording for a fixed duration of {fixed_duration} seconds...")
            audio = record_fixed_duration_audio(device_id, duration=fixed_duration)
            processed_audio = preprocess_audio(audio)
            transcription = transcribe_audio(processed_audio, whisper_pipe)
            print("Transcription complete.")
            print("Transcription:", transcription)
        elif choice == '3':
            fixed_duration = set_fixed_duration()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
