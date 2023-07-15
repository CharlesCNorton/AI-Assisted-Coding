from pytube import YouTube, Playlist
from pytube.exceptions import PytubeError
import os
import re

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage_of_completion = bytes_downloaded / total_size * 100
    print(f"\rDownloading... {percentage_of_completion:.2f}%", end='')

def download_youtube_video(url, filename, audio_only=False):
    try:
        yt = YouTube(url, on_progress_callback=progress_function)
    except PytubeError as e:
        print(f"Pytube error occurred: {type(e).__name__}, {e.args}")
        return
    except Exception as e:
        print(f"An error occurred: {type(e).__name__}, {e.args}")
        return

    if audio_only:
        stream = yt.streams.get_audio_only()
        filename += '.mp3'
    else:
        stream = yt.streams.get_highest_resolution()
        filename += '.mp4'

    if os.path.exists(filename):
        overwrite = input(f"File '{filename}' already exists. Do you want to overwrite it? (yes/no): ")
        if overwrite.lower() != 'yes':
            return

    print(f"\nDownloading: {yt.title}")
    try:
        stream.download(filename=filename)
    except Exception as e:
        print(f"Error occurred during downloading: {type(e).__name__}, {e.args}")
        return

    print(f"\nDownloaded as {filename}")

def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    youtube_regex_match = re.match(youtube_regex, url)
    return youtube_regex_match is not None

def main():
    while True:
        print("\n1. Download a YouTube video")
        print("2. Download audio from a YouTube video")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice in ['1', '2']:
            url = input("Enter the YouTube URL: ")
            while not is_youtube_url(url):
                print("Invalid YouTube URL. Please enter a valid YouTube URL.")
                url = input("Enter the YouTube URL: ")

            filename = input("Enter the filename for the downloaded content (without extension): ")
            audio_only = choice == '2'
            
            download_youtube_video(url, filename, audio_only)
        elif choice == '3':
            break
        else:
            print("Error: Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()