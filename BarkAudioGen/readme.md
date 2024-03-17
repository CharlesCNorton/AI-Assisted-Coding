
# BarkAudioGen README.md

## Overview
BarkAudioGen is a Python-based command-line application designed to harness the power of Suno's Bark, a state-of-the-art transformer-based text-to-audio model. Bark is capable of generating not only highly realistic, multilingual speech but also other forms of audio such as music, background noise, and simple sound effects. Additionally, it can produce nonverbal communications like laughing, sighing, and crying. This tool allows users to input text prompts and generate corresponding audio outputs, which are saved as WAV files. It's an ideal tool for developers, content creators, and researchers interested in exploring the possibilities of generative audio.

## Features
- **Text-Prompted Audio Generation**: Generate diverse audio outputs, including speech, music, and sound effects, from text prompts.
- **Highly Realistic and Multilingual Speech**: Utilize the model's capability to produce speech in various languages with high realism.
- **Nonverbal Sound Production**: Explore the generation of nonverbal sounds like laughter, sighs, and cries for a wide range of applications.
- **Simple Command-Line Interface**: Easily generate and play back audio files directly from the command line.
- **Automatic File Naming**: Saves generated audio with a unique timestamped name for easy organization.
- **Immediate Audio Playback**: Listen to the generated audio immediately after creation through integrated playback functionality.

## Installation

To use BarkAudioGen, ensure you have Python installed on your system. Clone the repository or download the source code to your local machine. Before running the program, install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install all necessary libraries, including `pygame` for audio playback and `colorama` for colored terminal output, among others.

## Usage

Run the program by executing the main script from your terminal:

```bash
python BarkAudioGen.py
```

Follow the on-screen prompts to generate audio. You'll be able to:
1. Generate audio from a text prompt.
2. Exit the program.

When generating audio, enter your text prompt when prompted, and the program will handle the rest, including saving the audio file and playing it back.

## Dependencies
- `pygame`: For audio playback.
- `colorama`: For colored terminal output.
- `scipy`: Specifically `scipy.io.wavfile` for writing WAV files.
- `datetime`: For generating timestamped filenames.
- Suno's Bark libraries: For generating audio from text prompts.

## Contribution
Contributions are welcome! If you'd like to improve BarkAudioGen or extend its capabilities, feel free to fork the repository and submit a pull request with your changes.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.

## Acknowledgments
Special thanks to Suno for developing the Bark model, which has made this project possible. BarkAudioGen is a testament to the capabilities of modern AI in the audio generation space, and we're excited to see how it evolves with contributions from the community.
