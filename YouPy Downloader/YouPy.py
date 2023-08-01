
from pytube import YouTube, Playlist
from pytube.exceptions import PytubeError
import os
import re

USER_PROMPTS = {
    "main_menu": "\n1. Download a YouTube video\n2. Download audio from a YouTube video\n3. Exit\nChoose an option: ",
    "filename": "Enter the filename for the downloaded content (without extension): ",
    "youtube_url": "Enter the YouTube URL: "
}

def get_user_input(prompt, validation_func=None):
    while True:
        value = input(prompt)
        if validation_func is None or validation_func(value):
            return value
        print("Invalid input. Please try again.")

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    progress = (bytes_downloaded / total_size) * 100  # Progress in percentage
    filled_len = int(progress) // 2  # Assuming the total length of progress bar is 50
    bar = '█' * filled_len + '-' * (50 - filled_len)
    print(f'\rDownloading: |{bar}| {progress:.2f}%', end='')

def get_youtube_object():
    while True:
        url = input(USER_PROMPTS["youtube_url"])
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

def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )

    youtube_regex_match = re.match(youtube_regex, url)
    return youtube_regex_match is not None

def download_youtube_video(filename, audio_only=False):
    yt = get_youtube_object()
    if yt is None:
        return

    stream, filename_ext = get_youtube_stream(yt, audio_only)
    if stream is None:
        return

    filename = get_filename(filename, filename_ext)

    download_stream(yt, stream, filename)

def main():
    while True:
        choice = get_user_input(USER_PROMPTS["main_menu"], lambda x: x in ['1', '2', '3'])

        if choice in ['1', '2']:
            filename = get_user_input(USER_PROMPTS["filename"])
            audio_only = choice == '2'
            
            download_youtube_video(filename, audio_only)
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
