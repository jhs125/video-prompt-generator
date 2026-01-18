# 🎬 Viral Video Prompt Generator

Generate AI prompts for creating viral YouTube Shorts based on successful videos.

## 🚀 Features
- Upload JSON file with viral video data
- Automatically generate prompts for ALL videos
- Download prompts as JSON, CSV, or individual TXT files
- Built with Streamlit

## 📦 Installation

```bash
pip install -r requirements.txt

## 📊 Input JSON Format

Your JSON file should have this structure:

```json
[
  {
    "Video ID": "abc123",
    "Video Title": "Your video title",
    "Video URL": "https://youtube.com/shorts/abc123",
    "Views": 100000,
    "Likes": 1000,
    "Duration (sec)": 15,
    "Niche": "Wealth & Money Stories",
    "Keyword": "success tips",
    "Description": "Video description...",
    "Idea Angle": "Recreate this viral format..."
  }
]
