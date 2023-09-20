# SeamlessTranscriber

SeamlessTranscriber is a powerful and user-friendly tool that utilizes the capabilities of the `SeamlessM4T` model from the `seamless_communication` repository. It allows users to transcribe audio, either from a pre-recorded file or directly from a microphone, into English text.

## Features

- **Transcription Modes**: Choose between transcribing from a pre-recorded audio file or capture your voice in real-time using a microphone.
- **High Accuracy**: Utilizes the large variant of the SeamlessM4T model for improved transcription accuracy.
- **User-Friendly Interface**: A simple, menu-driven console application making transcription as easy as a few key presses.

## Prerequisites

- Python 3.8 or newer
- PyTorch
- torchaudio
- sounddevice (for microphone input)

You also need to have the `seamless_communication` repository cloned to your local machine. You can find it here: https://github.com/facebookresearch/seamless_communication

## Setup

1. Ensure you have all the required dependencies installed.
2. Clone this repository to your local machine.
3. Make sure the required model files (`multitask_unity_large.pt`, `tokenizer.model`, etc.) are present in the same directory as `SeamlessTranscriber`.

## Usage

Navigate to the directory where `SeamlessTranscriber.py` is located and run.

Follow the on-screen prompts to choose your transcription mode and input details.

## Contribution

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

