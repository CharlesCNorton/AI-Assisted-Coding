import sys
import os
import torch
import sounddevice as sd
import numpy as np
import torchaudio

sys.path.append('ENTER_PATH_HERE')

from seamless_communication.models.inference import Translator

def record_audio(samplerate=16000, duration=10):
    """Record audio from the microphone."""
    try:
        audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()
        if audio is None:
            raise ValueError("No audio data recorded.")
        return audio.squeeze()
    except Exception as e:
        print(f"Error recording audio: {e}")
        return None

def save_audio_to_file(audio, filename='temp_recording.wav', samplerate=16000):
    """Save audio to a file."""
    if audio is None:
        print("No audio data to save.")
        return
    try:
        torchaudio.save(filename, torch.tensor(audio).unsqueeze(0), samplerate)
    except Exception as e:
        print(f"Error saving audio file: {e}")

def transcribe_audio(model, audio_path=None):
    """Transcribe audio using the ASR model."""
    if not audio_path:
        audio = record_audio()
        if audio is None:
            return "Recording failed. Cannot transcribe."
        audio_path = 'temp_recording.wav'
        save_audio_to_file(audio, audio_path)
    if not os.path.exists(audio_path):
        return "Audio file does not exist. Cannot transcribe."
    try:
        transcribed_text, _, _ = model.predict(audio_path, "asr", "en")
        return transcribed_text
    except Exception as e:
        return f"Error in transcription: {e}"

def get_user_input(prompt):
    """Get user input with a prompt."""
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)

def main():
    print("Initializing the SeamlessM4T model...")
    model_checkpoint = "ENTER_MODEL_CHECKPOINT_PATH"
    vocoder_checkpoint = "ENTER_VOCODER_CHECKPOINT_PATH"
    try:
        translator = Translator(model_checkpoint, vocoder_name_or_card=vocoder_checkpoint, device=torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
    except Exception as e:
        print(f"Failed to initialize the model: {e}")
        sys.exit(1)
    print("\nSeamlessM4T model initialized!")

    while True:
        print("\nChoose an option:")
        print("1. Transcribe from a pre-recorded audio file.")
        print("2. Transcribe directly from the microphone.")
        print("3. Exit.")

        choice = get_user_input("\nEnter your choice: ")
        if choice == '1':
            audio_path = get_user_input("Enter the path to the audio file: ")
            if not audio_path:
                continue
            print("\nTranscribing...")
            text = transcribe_audio(translator, audio_path)
            print("\nTranscribed Text:\n", text)
        elif choice == '2':
            print("\nRecording audio from the microphone... (Duration: 10 seconds)")
            text = transcribe_audio(translator)
            print("\nTranscribed Text:\n", text)
        elif choice == '3':
            break
        else:
            print("\nInvalid choice. Please select a valid option.")

    print("\nThank you for using SeamlessM4T!")

if __name__ == "__main__":
    main()
