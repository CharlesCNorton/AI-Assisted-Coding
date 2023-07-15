## YouPy Downloader

YouPy Downloader is a Python script that allows you to seamlessly download YouTube videos or just the audio from the videos with progress updates. 

## Requirements

YouPy Downloader requires Python 3 and the PyTube library. You can install PyTube with pip:

pip install pytube
Usage
To use YouPy Downloader, run it in your terminal or command line:

sh
Copy code
python youpy_downloader.py
Upon execution, YouPy Downloader will display a menu with three options:

Download a YouTube video
Download audio from a YouTube video
Exit
Enter the number of the option you want to choose.

If you choose to download a video or audio, you'll be prompted to enter the YouTube URL and a filename for the downloaded content (without extension). If a file with the chosen filename already exists, you'll be asked if you want to overwrite it.

The downloaded video will be in the best available quality. If you're downloading audio, only the audio track will be downloaded. The download progress will be displayed as a percentage to keep you updated.

License##

YouPy Downloader is intended for personal use only. Always respect copyrights and the terms of service of YouTube. Do not use this script to download copyrighted content without permission.