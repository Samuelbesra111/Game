# YouTube Video Downloader

A comprehensive Python-based YouTube video downloader with both GUI and CLI interfaces. Built on top of the powerful `yt-dlp` library.

## Features

### 🎯 Core Features
- **Dual Interface**: Both graphical (GUI) and command-line (CLI) interfaces
- **Multiple Quality Options**: Download in best, worst, 720p, 480p, or 360p quality
- **Audio Extraction**: Download audio-only files in MP3 format
- **Video Information**: Get detailed video metadata before downloading
- **Format Selection**: View all available formats for any video
- **Custom Output Path**: Choose where to save your downloads
- **Real-time Progress**: Live download progress and logging
- **Error Handling**: Comprehensive error reporting and handling

### 🖥️ GUI Features
- **Modern Interface**: Clean, user-friendly tkinter-based GUI
- **Progress Tracking**: Visual progress bar and detailed logging
- **Video Info Preview**: Get video details before downloading
- **Path Browser**: Easy directory selection for downloads
- **Threading**: Non-blocking downloads that don't freeze the interface

### 💻 CLI Features
- **Command-line Arguments**: Full control via terminal commands
- **Batch Processing**: Perfect for scripts and automation
- **Information Mode**: Get video details without downloading
- **Format Listing**: View all available formats
- **Flexible Quality Selection**: Choose exact quality or let it auto-select

## Installation

### Prerequisites
- **Python 3.7+** (with tkinter for GUI support)
- **yt-dlp** (YouTube downloader)
- **ffmpeg** (for audio conversion, installed automatically)

### System Installation (Recommended)
```bash
# Install yt-dlp and dependencies via system package manager
sudo apt update
sudo apt install yt-dlp python3 python3-tk

# Clone or download the script
# Make scripts executable
chmod +x youtube_downloader.py
chmod +x download_youtube.sh
```

### Alternative: pip Installation
```bash
# If you prefer pip over system packages
pip install yt-dlp

# Then make scripts executable
chmod +x youtube_downloader.py
chmod +x download_youtube.sh
```

## Usage

### 🎨 GUI Mode (Recommended for Beginners)

Launch the graphical interface:
```bash
python3 youtube_downloader.py
# or
./youtube_downloader.py
# or
./download_youtube.sh
```

**GUI Workflow:**
1. **Enter URL**: Paste the YouTube video URL in the text field
2. **Get Info** (optional): Click "Get Video Info" to see video details
3. **Select Quality**: Choose from dropdown (best, worst, 720, 480, 360)
4. **Audio Only** (optional): Check the box to download MP3 audio only
5. **Choose Path** (optional): Click "Browse" to select download location
6. **Download**: Click "Download" and monitor progress in the log area

### ⌨️ CLI Mode (Advanced Users)

#### Basic Download
```bash
# Download best quality video
python3 youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Using the shell launcher
./download_youtube.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Quality Selection
```bash
# Download specific quality
python3 youtube_downloader.py "URL" --quality 720

# Download worst quality (smallest file)
python3 youtube_downloader.py "URL" --quality worst
```

#### Audio Only
```bash
# Download audio as MP3
python3 youtube_downloader.py "URL" --audio-only
```

#### Custom Output Directory
```bash
# Download to specific directory
python3 youtube_downloader.py "URL" --output "/path/to/downloads"
```

#### Video Information
```bash
# Get video info without downloading
python3 youtube_downloader.py "URL" --info

# List all available formats
python3 youtube_downloader.py "URL" --formats
```

#### Complete CLI Examples
```bash
# Download 720p video to Downloads folder
python3 youtube_downloader.py "https://youtu.be/dQw4w9WgXcQ" -q 720 -o ~/Downloads

# Download audio only
python3 youtube_downloader.py "https://youtu.be/dQw4w9WgXcQ" --audio-only

# Get video information
python3 youtube_downloader.py "https://youtu.be/dQw4w9WgXcQ" --info

# View all available formats
python3 youtube_downloader.py "https://youtu.be/dQw4w9WgXcQ" --formats
```

### 📝 CLI Help
```bash
python3 youtube_downloader.py --help
```

## Configuration

### Default Settings
- **Default Quality**: best
- **Default Output**: `~/Downloads` (user's Downloads folder)
- **Default Format**: MP4 for video, MP3 for audio
- **File Naming**: Uses video title as filename

### Customization
You can modify the `YouTubeDownloader` class in `youtube_downloader.py` to change:
- Default download path
- Output filename template
- Quality preferences
- Audio format settings

## File Structure

```
youtube-downloader/
├── youtube_downloader.py    # Main Python script
├── download_youtube.sh      # Shell launcher script
├── requirements.txt         # Dependencies information
├── README_YOUTUBE_DOWNLOADER.md # This documentation
└── Downloads/              # Default download directory (created automatically)
```

## Troubleshooting

### Common Issues

**1. "yt-dlp command not found"**
```bash
# Install yt-dlp
sudo apt install yt-dlp
# or
pip install yt-dlp
```

**2. "GUI not available" error**
```bash
# Install tkinter
sudo apt install python3-tk
```

**3. "Permission denied" error**
```bash
# Make scripts executable
chmod +x youtube_downloader.py
chmod +x download_youtube.sh
```

**4. Download fails with format error**
- Try different quality settings
- Use `--formats` to see available options
- Some videos may have limited format availability

**5. Audio extraction fails**
```bash
# Ensure ffmpeg is installed
sudo apt install ffmpeg
```

### Debug Mode
For detailed error information, run with Python's verbose mode:
```bash
python3 -v youtube_downloader.py "URL"
```

## Advanced Usage

### Batch Downloads
Create a script for multiple videos:
```bash
#!/bin/bash
# batch_download.sh

URLS=(
    "https://youtu.be/VIDEO1"
    "https://youtu.be/VIDEO2"
    "https://youtu.be/VIDEO3"
)

for url in "${URLS[@]}"; do
    python3 youtube_downloader.py "$url" -q 720
done
```

### Integration with Other Tools
The CLI interface makes it easy to integrate with:
- **Cron jobs** for scheduled downloads
- **Shell scripts** for batch processing
- **Other Python programs** as a module
- **File managers** as a custom action

## Technical Details

### Dependencies
- **yt-dlp**: Core YouTube downloading functionality
- **tkinter**: GUI framework (usually included with Python)
- **subprocess**: System command execution
- **threading**: Background download processing
- **json**: Video metadata parsing
- **pathlib**: Cross-platform path handling

### Supported Platforms
- **Linux** (primary target, fully tested)
- **macOS** (should work with minor adjustments)
- **Windows** (basic compatibility, may need path adjustments)

### Video Format Support
Supports all formats that yt-dlp can handle:
- **Video**: MP4, WebM, FLV, 3GP, and more
- **Audio**: MP3, M4A, WebM, OGG, and more
- **Quality**: From 144p to 4K+ (depending on source)

## Security and Legal Notes

### Important Disclaimers
- **Respect Copyright**: Only download videos you have permission to download
- **Terms of Service**: Ensure downloads comply with YouTube's Terms of Service
- **Fair Use**: Consider fair use guidelines for downloaded content
- **Personal Use**: This tool is intended for personal use only

### Best Practices
- Don't download copyrighted content without permission
- Respect content creators and their work
- Use downloads responsibly and ethically
- Consider supporting creators through official channels

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool.

### Future Enhancements
- Playlist download support
- Download queue management
- Resume interrupted downloads
- Subtitle download options
- Integration with media players
- Configuration file support

## License

This project is provided as-is for educational and personal use. Please respect copyright laws and YouTube's terms of service.

## Support

If you encounter issues:
1. Check this README for common solutions
2. Verify yt-dlp is up to date: `yt-dlp --update`
3. Test with a simple video URL first
4. Check system dependencies are installed

---

**Happy downloading! 🎉**

Remember to use this tool responsibly and respect content creators' rights.