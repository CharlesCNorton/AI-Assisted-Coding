# YouTube Downloader

This application lets you download YouTube videos or audio files in an easy and convenient way.

## Features

- Download YouTube videos in highest available resolution.
- Download only the audio from YouTube videos.
- Informative download progress indicator.
- Advanced error handling for robust functionality.

## Usage

1. Run the python script: python youtube_downloader.py
2. Choose an option: download a video (press 1), download only audio (press 2), or exit (press 3).
3. If you choose to download, you will be prompted to enter the YouTube URL and the filename (without extension) for the downloaded content.
4. If the filename already exists in the directory, you will be asked if you want to overwrite it. Enter 'yes' or 'no'.
5. The content will be downloaded to the current directory. You can check the progress in the console.

## Requirements

- Python 3.x
- Pytube library

## Installation

1. Clone the repository
2. Install requirements using pip: pip install -r requirements.txt
3. Run the script: python youtube_downloader.py