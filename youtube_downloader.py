from pytube import YouTube
import os

def download_youtube_video(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Check if the URL is for a single video or a playlist
        if "list=" in url:
            print("Error: This program does not support downloading playlists.")
            return
        
        # Get the highest resolution stream with 1080p preference
        print(f"Title: {yt.title}")
        print("Searching for the best 1080p stream...")
        
        # Filter streams to find the 1080p video
        stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution="1080p").first()
        
        if not stream:
            print("1080p resolution not available. Falling back to the highest available resolution.")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not stream:
            print("No suitable stream found. Please check the URL or try again later.")
            return
        
        # Download the video
        print(f"Downloading: {yt.title} ({stream.resolution})")
        download_path = stream.download(output_path=os.getcwd())  # Downloads to the current working directory
        print(f"Download completed! File saved at: {download_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Prompt the user to enter the YouTube video URL
    video_url = input("Enter the YouTube video URL: ").strip()
    
    if not video_url:
        print("Error: No URL provided.")
    else:
        download_youtube_video(video_url)
