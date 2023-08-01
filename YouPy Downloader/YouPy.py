
from pytube import YouTube, Playlist
from pytube.exceptions import PytubeError
import os
import re
import unittest

def get_user_input(prompt, validation_func=None, error_message="Invalid input. Please try again."):
    while True:
        value = input(prompt)
        if validation_func is None or validation_func(value):
            return value
        print(error_message)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    if total_size > 0:
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(f"\rDownloading... {percentage_of_completion:.2f}%", end='')
    else:
        print(f"\rDownloading... completed", end='')

def handle_error(e):
    print(f"An error occurred: {type(e).__name__}, {str(e)}")

def get_youtube_object(url):
    try:
        return YouTube(url, on_progress_callback=progress_function)
    except PytubeError as e:
        handle_error(e)
    except Exception as e:
        handle_error(e)

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

def download_youtube_video(url, filename, audio_only=False):
    yt = get_youtube_object(url)
    if yt is None:
        return

    stream, filename_ext = get_youtube_stream(yt, audio_only)
    if stream is None:
        return

    filename += filename_ext

    if os.path.exists(filename):
        overwrite = get_user_input(f"File '{filename}' already exists. Do you want to overwrite it? (yes/no): ",
                                   lambda x: x.lower() in ['yes', 'no'])
        if overwrite.lower() != 'yes':
            return

    print(f"\nDownloading: {yt.title}")
    try:
        stream.download(filename=filename)
    except Exception as e:
        handle_error(e)
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
        choice = get_user_input("Choose an option: ", lambda x: x in ['1', '2', '3'])

        if choice in ['1', '2']:
            url = get_user_input("Enter the YouTube URL: ", is_youtube_url)
            filename = get_user_input("Enter the filename for the downloaded content (without extension): ")
            audio_only = choice == '2'

            download_youtube_video(url, filename, audio_only)
        elif choice == '3':
            break

class TestYouPy(unittest.TestCase):

    def test_is_youtube_url(self):
        self.assertTrue(is_youtube_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
        self.assertFalse(is_youtube_url('https://www.notarealwebsite.com/watch?v=dQw4w9WgXcQ'))

if __name__ == "__main__":
    unittest.main()
