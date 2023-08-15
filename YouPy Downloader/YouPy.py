import yt_dlp
import os
import re

def validate_url(url):
    # A basic regex to check if the URL seems like a valid YouTube URL
    youtube_regex = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$')
    return youtube_regex.match(url)

def download_video_yt_dlp(url, output_path):
    options = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'progress_hooks': [hook],
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def hook(d):
    if d['status'] == 'downloading':
        # Display the progress bar
        print(d['_percent_str'], end="\r")

def main():
    while True:
        # Prompt the user for the video URL
        url = input("\nEnter the YouTube video URL: ").strip()

        # Validate the URL
        if not validate_url(url):
            print("Invalid YouTube URL. Please try again.")
            continue

        # Prompt the user for the desired output path
        output_path = input("Enter the desired output path: ").strip()

        # Check if the directory exists
        if not os.path.exists(output_path):
            choice = input(f"The directory '{output_path}' does not exist. Would you like to create it? (yes/no): ").strip().lower()
            if choice == 'yes':
                os.makedirs(output_path)
            else:
                print("Please provide a valid directory.")
                continue

        # Attempt to download the video
        try:
            download_video_yt_dlp(url, output_path)
            print("\nVideo downloaded successfully!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

        # Ask the user if they want to download another video or exit
        choice = input("\nDo you want to download another video? (yes/no): ").strip().lower()
        if choice != 'yes':
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    print("Welcome to YouPy!!")
    main()