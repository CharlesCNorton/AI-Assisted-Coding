# MidiModifier

MidiModifier is a Python utility designed to modify MIDI files, specifically to ensure that MIDI files consisting of a single track are compatible with software that expects MIDI files with at least two tracks. It achieves this by adding an additional, essentially empty track to the MIDI file, without altering the original content of the MIDI file.

## Features

- **Convert Single-Track MIDI Files**: Converts any single-track MIDI file to a two-track MIDI file by adding an empty second track, ensuring compatibility with software requiring multi-track MIDI files.
- **User-Friendly Interface**: Offers a simple CLI and GUI for selecting MIDI files and specifying the output location, making it accessible for users with varying levels of technical expertise.
- **Extensibility**: Designed with future expansions in mind, providing a foundation for adding more complex MIDI file modifications.

## Installation

Ensure you have Python installed on your system. MidiModifier requires the `mido` and `colorama` packages. Install them using pip:

```bash
pip install mido colorama
```

## Usage

Run `MidiModifier` from the command line:

```bash
python MidiModifier.py
```

Follow the on-screen prompts to select your input MIDI file and specify the output file location.

## License

MidiModifier is MIT licensed, as found in the LICENSE file.

MidiModifier © 2024 by PortfolioAI
