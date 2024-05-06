import os
import sys
from googleapiclient.discovery import build
from pytube import YouTube, Playlist
from tqdm import tqdm
from colorama import init, Fore
import requests
from bs4 import BeautifulSoup

# Import API key from config.py
from config import YOUTUBE_API_KEY

# Initialize colorama
init(autoreset=True)

# ASCII art representation of the logo
logo = r"""
  _____              _             _   _      _   _               _             
 |  __ \            (_)           | \ | |    | | | |             | |            
 | |__) | __ ___   ___  __ _  ___ |  \| | ___| |_| |__   ___   __| | __ _ _   _ 
 |  ___/ '__/ _ \ / _ \/ _` |/ _ \| . ` |/ _ \ __| '_ \ / _ \ / _` |/ _` | | | |
 | |   | | | (_) |  __/ (_| | (_) | |\  |  __/ |_| | | | (_) | (_| | (_| | |_| |
 |_|   |_|  \___/ \___|\__, |\___/|_| \_|\___|\__|_| |_|\___/ \__,_|\__,_|\__, |
                        __/ |                                              __/ |
                       |___/                                              |___/ 
"""

def download_video(video_url, output_path):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        if stream:
            print(f"Downloading video '{yt.title}'...")
            with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc=f"Downloading {yt.title}", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET)) as progress_bar:
                stream.download(output_path, filename=yt.title, filename_prefix='[IN PROGRESS] ')
                progress_bar.update(stream.filesize)
            print("Download completed!")
        else:
            print("No available progressive stream for this video.")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_playlist(playlist_url, channel_name):
    try:
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title.replace("/", "_")  # Replace invalid characters in folder name
        output_folder = os.path.join(os.getcwd(), channel_name, playlist_title)
        os.makedirs(output_folder, exist_ok=True)
        print(f"Downloading playlist '{playlist_title}' to '{output_folder}'")
        for video_url in playlist.video_urls:
            download_video(video_url, output_folder)
    except Exception as e:
        print(f"An error occurred: {e}")


def download_channel(channel_url):
    try:
        # Extract channel ID from channel URL
        if "/channel/" in channel_url:
            channel_id = channel_url.split("/channel/")[-1]
        elif "/@" in channel_url:
            channel_name = channel_url.split("/@")[-1]
            # Fetch HTML content of the channel page
            response = requests.get(f"https://www.youtube.com/{channel_name}")
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the channel ID from the meta tags
            channel_id = soup.find("meta", {"property": "channelId"})["content"]
        else:
            print("Invalid channel URL.")
            return

        # Build YouTube Data API service
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # Initialize empty list to store playlist IDs
        playlist_ids = []

        # Retrieve playlists from the channel
        next_page_token = None
        while True:
            playlists_request = youtube.playlists().list(part='snippet', channelId=channel_id, maxResults=50, pageToken=next_page_token)
            playlists_response = playlists_request.execute()
            
            # Append playlist IDs to the list
            for playlist in playlists_response['items']:
                playlist_ids.append(playlist['id'])
            
            # Check if there are more playlists to fetch
            next_page_token = playlists_response.get('nextPageToken')
            if not next_page_token:
                break

        # Download each playlist
        for playlist_id in playlist_ids:
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            download_playlist(playlist_url, channel_name=channel_id)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print(Fore.YELLOW + logo)
    print(Fore.CYAN + "Welcome to YouTube Downloader!")
    while True:
        print(Fore.GREEN + "[1] Download a Video")
        print(Fore.MAGENTA + "[2] Download a Playlist")
        print(Fore.BLUE + "[3] Download a Channel")
        print(Fore.RED + "[4] Exit")
        choice = input(Fore.WHITE + "Enter your choice: ")

        if choice == '1':
            url = input("Enter the video URL: ")
            download_video(url, os.getcwd())
        elif choice == '2':
            url = input("Enter the playlist URL: ")
            download_playlist(url, os.getcwd())
        elif choice == '3':
            print(Fore.YELLOW + """
## Downloading a YouTube Channel

To download content from a YouTube channel, you'll need the channel's ID. Follow these steps to obtain the channel ID:

1. Go to the [YouTube Channel ID Finder](https://commentpicker.com/youtube-channel-id.php).
2. Enter the URL of the YouTube channel you want to download content from (e.g., `https://www.youtube.com/@Anonymous_Amit`).
3. Click on the "Get Channel ID" button.
4. Copy the generated channel ID, which will typically be in the format `https://www.youtube.com/channel/UC1YPqg1KPgZoZ9akpCfsAWw`.

5. Use the copied channel ID URL when prompted for the channel URL in the downloader script.
""")
            url = input("Enter the channel URL: ")
            download_channel(url)
        elif choice == '4':
            sys.exit("Exiting program.")
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
