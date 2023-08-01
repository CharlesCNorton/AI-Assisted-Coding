
# Enhanced YouTube Downloader

Welcome to the Enhanced YouTube Downloader, an efficient and reliable tool that takes your YouTube content offline in the most user-friendly way. With its new and improved features, it makes downloading videos or audio from YouTube a breeze!

## Features

- Download YouTube videos in the highest available resolution.
- Download audio-only files from YouTube videos.
- Informative download progress indicator.
- Advanced error handling for robust functionality.
- Improved user interface for a better user experience.
- More modular code structure for easier maintenance and enhancement.
- File overwrite protection with user preference settings.
- Added unit tests to ensure functionality and facilitate future debugging or enhancements.

## Usage

1. Run the Python script: `python YouPy_improved.py`
2. Choose an option: download a video (press 1), download only audio (press 2), or exit (press 3).
3. If you choose to download, you will be prompted to enter the YouTube URL and the filename (without extension) for the downloaded content.
4. If the filename already exists in the directory, you will be asked if you want to overwrite it. Enter 'yes' or 'no'.
5. The content will be downloaded to the current directory. You can check the progress in the console.
6. To run the unittest, execute `python -m unittest YouPy_improved.py`

## Requirements

- Python 3.x
- Pytube library

## Installation

1. Clone the repository
2. Install requirements using pip: `pip install -r requirements.txt`
3. Run the script: `python YouPy_improved.py`
