
# YTLOADER 

YTLOADER is a Python script that allows you to download videos, playlists, and channels from YouTube using the YouTube Data API.

## Features

- Download individual videos by providing the video URL.
- Download entire playlists by providing the playlist URL.
- Download all playlists from a YouTube channel by providing the channel URL.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AnonAmit/ytloader
   ```

2. Navigate to the project directory:

   ```bash
   cd ytloader
   ```

3. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have obtained a YouTube Data API key. See the section below on [how to get your API key](https://github.com/AnonAmit/ytloader/blob/main/README.md#how-to-get-youtube-data-api-key).
   
2. Update the `config.py` file with your [YouTube Data API key]:

   ```python
   YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
   ```

3. Run the `main.py` script:

   ```bash
   python main.py
   ```

4. Choose the desired download option (video, playlist, or channel).
   
5. Enter the corresponding URL when prompted.

## Downloading a YouTube Channel
To download content from a YouTube channel, you'll need the channel's ID. Follow these steps to obtain the channel ID:

1. Go to the YouTube Channel ID Finder.
2. Enter the URL of the YouTube channel you want to download content from (e.g., https://www.youtube.com/@Anonymous_Amit).
3. Click on the "Get Channel ID" button.
4. Copy the generated channel ID, which will typically be in the format https://www.youtube.com/channel/UC1YPqg1KPgZoZ9akpCfsAWw.
Use the copied channel ID when prompted for the channel URL in the downloader script.

## How to Get YouTube Data API Key

To use the YouTube Data API and access features like fetching playlists and channel information, you need to obtain an API key from the Google Cloud Console. Follow these steps to get your API key:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one) from the top menu.
3. In the sidebar, navigate to "APIs & Services" > "Credentials".
4. Click on "Create credentials" and select "API key".
5. Copy the generated API key.
6. Paste the API key into the `config.py` file in the `YOUTUBE_API_KEY` variable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

