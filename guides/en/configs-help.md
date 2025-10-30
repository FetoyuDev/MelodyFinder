# Configuration Guide - MelodyFinder

This guide explains how to configure the `configs.json` file to customize MelodyFinder's behavior.

## Structure of the Configuration File 

The `configs.json` file contains the following settings:

### API Key
- **Type**: String
- **Description**: The API key for YouTube Data API v3.
- **How to obtain a API Key**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/).
  2. Create a new project or select an existing one.
  3. Enable the YouTube Data API v3.
  4. Create credentials (API key).
  5. Copy the API key and paste it here.
- **Example**: `“AIzaSyB...”`
- **Note**: Keep this key secure and do not share it.

### Languages
- **Type**: String
- **Description**: The interface language.
- **Possible values**: `“en”` (English),  `“es”` (Spanish), `‘it’` (Italian), `“pt”` (Portuguese)
- **Example**: `“it”`

### Paths
- **Type**: Object
- **Description**: Folder paths for downloaded and temporary files.
- **Subfields**:
  - `temp`: Folder for temporary files during download.
  - `mp3`: Folder for downloaded MP3 files.
  - `mp4`: Folder for downloaded MP4 files.
  - `lyrics`: Folder for song lyrics files.
- **Example**:
```json
  {
    “temp”: “downloads/temp”,
    “mp3”: “downloads/mp3”,
    “mp4”: “downloads/mp4”,
    “lyrics”: “lyrics”
  }
```
- **Note**: Paths are relative to the script's execution directory. Make sure the folders exist or that the script can create them.

### Themes
- **Type**: String
- **Description**: The interface theme.
- **Possible values**: `“dark”`, `“light”`
- **Example**: `“dark”`

## Complete Configuration Example

```json
{
    “api_key”: “INSERT_YOUR_YOUTUBE_DATA_API_KEY_HERE”,
    “language”: “en”,
    “paths”: {
        “temp”: “downloads/temp”,
        “mp3”: “downloads/mp3”,
        “mp4”: “downloads/mp4”,
        “lyrics”: “lyrics”
    },
    “theme”: “dark”
}
```

## Important Notes
- Edit the `configs.json` file with a text editor.
- Restart the script after making changes to apply the new settings.
- If you encounter problems, check that the JSON syntax is correct (use an online JSON validation tool).
- For security reasons, do not commit the `configs.json` file with the real API key to a public repository.
