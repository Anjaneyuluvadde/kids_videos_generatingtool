# 🎨 AI-Powered Kid Video Generator

A completely local, offline automation tool to generate engaging, beat-synced videos for kids.

## ✨ Features
- **100% Offline & Free**: No API keys, no paid services! Uses local AI.
- **Beat Syncing**: Uses Librosa to automatically transition visuals to the beat of the background music.
- **Auto Captions**: Uses local Whisper AI to generate accurate subtitles.
- **Kid-Friendly Effects**: Colorful captions, cartoon effects, and sticker overlays.
- **Multiple Formats**: Supports 1080p Landscape and YouTube Shorts/TikTok formats.
- **Templates**: Pre-configured templates for ABC Learning, Animal Stories, etc.

## 🛠️ Setup Instructions

### 1. Install Prerequisites
You need Python 3.9+ and FFmpeg installed on your system.

**Installing FFmpeg:**
- **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract, and add the `bin` folder to your system PATH.
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### 2. Install Dependencies
Run the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Run the App
Use the provided startup scripts:
- **Windows**: Double click `start.bat`
- **Mac/Linux**: Run `./start.sh`

Alternatively, manually run:
```bash
streamlit run app.py
```

## 📁 Folder Structure
- `assets/`: Place your images, videos, music, and stickers here.
- `output/`: Generated videos are saved here.
- `modules/`: Core Python logic (scene detection, rendering, etc.).
- `templates/`: Settings for different video styles.
- `configs/`: Additional configuration files.
