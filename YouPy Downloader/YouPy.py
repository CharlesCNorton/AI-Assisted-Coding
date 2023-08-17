import yt_dlp
import os
import re

MAX_RETRIES = 3  # Max number of retries for a failed download

def validate_url_using_yt_dlp(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            ydl.extract_info(url, download=False)
            return True
    except Exception:
        return False

def download_video_yt_dlp(url, output_path, output_name=None, ffmpeg_path=None):
    outtmpl = f'{output_path}/'
    if output_name:
        outtmpl += f'{output_name}.%(ext)s'
    else:
        outtmpl += '%(title)s.%(ext)s'

    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': outtmpl,
        'progress_hooks': [hook],
        'postprocessors': [{
            'key': 'FFmpegMetadata'
        }],
        'merge_output_format': 'mp4',
    }
    
    if ffmpeg_path:
        options['ffmpeg_location'] = ffmpeg_path

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def hook(d):
    if d['status'] == 'downloading':
        print(d['_percent_str'], end="\r")

def sanitize_filename(filename):
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c in (' ', '.', '-', '_')]).rstrip()

def main():
    print("Welcome to YouPy!!")
    
    # Get the FFmpeg path from the user
    ffmpeg_path = input("Enter the path to your ffmpeg bin directory (e.g., C:/path/to/ffmpeg/bin): ").strip()
    
    while True:
        url = input("\nEnter the YouTube video URL: ").strip()
        if not validate_url_using_yt_dlp(url):
            print("Invalid YouTube URL or video might be restricted. Please try again.")
            continue

        output_path = input("Enter the desired output path: ").strip()
        if not os.path.exists(output_path):
            choice = input(f"The directory '{output_path}' does not exist. Would you like to create it? (yes/no): ").strip().lower()
            if choice == 'yes':
                os.makedirs(output_path)
            else:
                print("Please provide a valid directory.")
                continue

        output_name = input("Enter a name for the output file (Leave empty for the video's title): ").strip()
        output_name = sanitize_filename(output_name)

        retries = 0
        while retries < MAX_RETRIES:
            try:
                download_video_yt_dlp(url, output_path, output_name, ffmpeg_path)
                print("\nVideo downloaded successfully!")
                break
            except Exception as e:
                retries += 1
                print(f"\nAn error occurred: {str(e)}")
                if retries < MAX_RETRIES:
                    choice = input(f"Do you want to retry? ({MAX_RETRIES - retries} retries left) (yes/no): ").strip().lower()
                    if choice != 'yes':
                        break
                else:
                    print("Max retries reached. Moving on.")

        choice = input("\nDo you want to download another video? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()