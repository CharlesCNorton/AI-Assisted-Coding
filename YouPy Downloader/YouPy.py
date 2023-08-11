from pytube import YouTube
from pytube.exceptions import PytubeError
import os
import re

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    progress = (bytes_downloaded / total_size) * 100  # Progress in percentage
    filled_len = int(progress) // 2  # Assuming the total length of the progress bar is 50
    bar = '█' * filled_len + '-' * (50 - filled_len)
    print(f'\rDownloading: |{bar}| {progress:.2f}%', end='')

def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    youtube_regex_match = re.match(youtube_regex, url)
    return youtube_regex_match is not None

def get_youtube_object():
    while True:
        url = input("Enter the YouTube URL: ")
        if not is_youtube_url(url):
            print("Invalid YouTube URL. Please try again.")
            continue

        try:
            return YouTube(url, on_progress_callback=progress_function)
        except PytubeError as e:
            print(f"Pytube error occurred: {type(e).__name__}, {str(e)}")
            print("Please try another URL.")
        except Exception as e:
            print(f"An error occurred: {type(e).__name__}, {str(e)}")
            print("Please try another URL.")

def get_youtube_stream(yt, audio_only):
    if audio_only:
        stream = yt.streams.filter(only_audio=True).first()
        filename_ext = '.mp3'
    else:
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        filename_ext = '.mp4'
    if stream is None:
        print(f"No suitable stream found for {'audio only' if audio_only else 'video'}.")
    return stream, filename_ext

def get_filename(filename, filename_ext):
    base_filename = filename
    counter = 1
    while os.path.exists(filename + filename_ext):
        filename = f"{base_filename}({counter})"
        counter += 1
    return filename + filename_ext

def download_stream(yt, stream, filename):
    print(f"\nDownloading: {yt.title}")
    try:
        stream.download(filename=filename)
    except Exception as e:
        print(f"Error occurred during downloading: {type(e).__name__}, {str(e)}")
        return
    print(f"\nDownloaded as {filename}")

def download_youtube_video(filename, audio_only=False):
    yt = get_youtube_object()
    if yt is None:
        print("YouTube object could not be retrieved. Exiting.")
        return

    stream, filename_ext = get_youtube_stream(yt, audio_only)
    if stream is None:
        print("Stream could not be found. Exiting.")
        return

    filename = get_filename(filename, filename_ext)
    download_stream(yt, stream, filename)

def get_user_choice():
    print("\n1. Download a YouTube video")
    print("2. Download audio from a YouTube video")
    print("3. Exit")
    return input("Choose an option: ")

def main():
    while True:
        choice = get_user_choice()

        if choice in ['1', '2']:
            filename = input("Enter the filename for the downloaded content (without extension): ")
            audio_only = choice == '2'
            download_youtube_video(filename, audio_only)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
