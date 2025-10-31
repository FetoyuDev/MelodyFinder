## A cross-platform music player and downloader with Discord RP integration

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## 📋 Features

- 🎵 Music playback with metadata display
- 🎨 Custom album cover support
- 🔗 Discord Rich Presence integration
- 🌍 Multi-language support (English, Portuguese, Spanish, Italian)
- 📥 YouTube music download capability
- 🎨 Dark/Light theme support
- 🔐 Discord OAuth authentication
- 📱 Mobile integration ready

## 📁 Project Structure

```
MelodyFinder/
├── init.py                    # Main application entry point
├── configs.json               # Configuration file
├── languages_manager/         # Internationalization
│   └── languages_manager.py   # Language strings
├── guides/                    # Multi-language documentation
│   ├── en/                    # English guides
│   ├── es/                    # Spanish guides
│   ├── it/                    # Italian guides
│   └── pt/                    # Portuguese guides
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Required Dependencies

```bash
pip install PyQt6 requests pypresence
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/FetoyuDev/MelodyFinder.git
cd MelodyFinder
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the application (see [Configuration](#-configuration))

4. Run the application:

```bash
python init.py
```

## ⚙️ Configuration

Before running MelodyFinder, configure `configs.json`:

```json
{
    "api_key": "YOUR_YOUTUBE_DATA_API_KEY",
    "language": "en",
    "paths": {
        "temp": "downloads/temp",
        "mp3": "downloads/mp3",
        "mp4": "downloads/mp4",
        "lyrics": "lyrics"
    },
    "theme": "dark"
}
```

### Configuration Options

|     Field      |                Description                  |      Default     |
|----------------|---------------------------------------------|------------------|
| `api_key`      | YouTube Data API v3 key for video downloads | Required         |
| `language`     | UI language (`en`, `pt`, `es`, `it`)        | `en`             |
| `paths.temp`   | Temporary download directory                |  downloads/temp` |
| `paths.mp3`    | MP3 output directory                        | `downloads/mp3`  |
| `paths.mp4`    | MP4 output directory                        | `downloads/mp4`  |
| `paths.lyrics` | Lyrics storage directory                    | `lyrics`         |
| `theme`        | UI theme (`dark` or `light`)                | `dark`           |

### Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Copy the key to `configs.json`

## 🎮 Usage

### Basic Controls

- **Open File**: Load an audio file (MP3, WAV, FLAC)
- **Play**: Start playback
- **Pause**: Pause/resume playback
- **Stop**: Stop playback and reset position
- **Album Cover**: Click "Escolher capa" to set custom cover art

### Discord Integration

MelodyFinder displays your currently playing track on Discord:

- Track title
- Playback status (Playing/Paused/Stopped)
- Custom Rich Presence images

To enable Discord Rich Presence, add your Discord Client ID to the configuration.

### Language Selection

Change the `language` field in configs.json:

- `en` - English
- `pt` - Portuguese
- `es` - Spanish
- `it` - Italian

## 📖 Documentation

Detailed guides are available in multiple languages:

- [English Guide](guides/en/README.md)
- [Portuguese Guide](guides/pt/README.md)
- [Spanish Guide](guides/es/README.md)
- [Italian Guide](guides/it/README.md)

For configuration help, see the language-specific `configs-help.md` files in the guides directory.

## 🔧 Advanced Features

Will not bake you a pie!

### Mobile Integration

MelodyFinder supports sending playback data to a mobile endpoint. Configure the `mobile_bot_url` in your config to enable this feature.

### Custom Actions

- **Listen Now**: Quick access to configured streaming service
- **Download MelodyFinder**: Direct link to latest releases

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 🔗 Links

- [GitHub Repository](https://github.com/FetoyuDev/MelodyFinder)
- [Discord Server](https://discord.com/WIP)
- [Latest Releases](https://github.com/FetoyuDev/MelodyFinder/releases)

## 📧 Support

For support, please open an issue on GitHub or join our Discord server.
