import os
import subprocess

def install_dependencies():
    required_packages = ['pytube', 'tqdm', 'colorama']
    installed_packages = [package.split('==')[0] for package in os.popen('pip list').read().split('\n')[2:-1]]

    missing_packages = [package for package in required_packages if package not in installed_packages]

    if missing_packages:
        print(f"{Fore.YELLOW}Installing missing dependencies...{Fore.RESET}")
        for package in missing_packages:
            subprocess.run(['pip', 'install', package])
        print(f"{Fore.GREEN}Dependencies installed successfully!{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}All required dependencies are already installed.{Fore.RESET}")

# Call the function to install dependencies
install_dependencies()

# Rest 
from pytube import Playlist, YouTube
import os
from tqdm import tqdm
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Logo
logo = f"""{Fore.GREEN}
    _______  _______  _______  _        _______  _______ 
   (  ____ \(  ___  )(  ____ \| \    /\(  ____ \(  ___  )
   | (    \/| (   ) || (    \/|  \  / /| (    \/| (   ) |
   | |      | (___) || (__    |  (_/ / | (__    | (___) |
   | |      |  ___  ||  __)   |   _ (  |  __)   |  ___  |
   | |      | (   ) || (      |  ( \ \ | (      | (   ) |
   | (____/\| )   ( || (____/\|  /  \ \| (____/\| )   ( |
   (_______/|/     \|(_______/|_/    \/(_______/|/     \|
                                                          
{Fore.RESET}"""

def download_playlist(playlist, channel_name):
    print(f"{Fore.YELLOW}Downloading playlist: {playlist.title}{Fore.RESET}")
    directory = f"{channel_name}/{playlist.title}"
    os.makedirs(directory, exist_ok=True)

    for video in playlist.videos:
        download_video_with_progress(video, directory)

def download_video_with_progress(video, directory):
    stream = video.streams.filter(progressive=True, file_extension='mp4').first()
    file_size = stream.filesize
    temp_filename = f"{directory}/temp_{stream.default_filename}"
    with open(temp_filename, 'wb') as f, tqdm(
            desc=f"{video.title}",
            total=file_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            ascii=True
    ) as progress_bar:
        stream.download(output_path=directory, filename_prefix="temp", filename=stream.default_filename)
        progress_bar.update(file_size)
    
    os.rename(temp_filename, f"{directory}/{stream.default_filename}")

def download_channel(url):
    print(f"{Fore.GREEN}Analyzing channel...{Fore.RESET}")
    playlist_urls = []
    channel_name = None

    # Analyze the channel
    channel = Playlist(url)
    channel_name = channel.title

    # Extract all playlist URLs from the channel
    for video in channel.videos:
        if video.playlist_url and video.playlist_url not in playlist_urls:
            playlist_urls.append(video.playlist_url)

    # Show total number of videos and playlists
    total_videos = len(channel.videos)
    total_playlists = len(playlist_urls)
    print(f"{Fore.GREEN}Total number of videos: {total_videos}")
    print(f"Total number of playlists: {total_playlists}{Fore.RESET}")

    # Download all playlists of the channel
    for playlist_url in playlist_urls:
        playlist = Playlist(playlist_url)
        download_playlist(playlist, channel_name)

if __name__ == "__main__":
    print(logo)
    print(f"{Fore.CYAN}[1] Download a Single Video")
    print(f"{Fore.CYAN}[2] Download a Playlist")
    print(f"{Fore.CYAN}[3] Download a Channel")
    option = input(f"{Fore.GREEN}Enter the option number: {Fore.RESET}")

    if option == "1":
        video_url = input(f"{Fore.GREEN}Enter the URL of the YouTube video: {Fore.RESET}")
        download_video(video_url)
    elif option == "2":
        playlist_url = input(f"{Fore.GREEN}Enter the URL of the YouTube playlist: {Fore.RESET}")
        download_playlist(playlist_url)
    elif option == "3":
        channel_url = input(f"{Fore.GREEN}Enter the URL of the YouTube channel: {Fore.RESET}")
        download_channel(channel_url)
    else:
        print(f"{Fore.RED}Invalid option.{Fore.RESET}")
        
