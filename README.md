# youtube-shorts-automation
Attempt at Automated YouTube Shorts Creation

## Purpose
This project is an attempt to build a fully automated pipeline for generating and uploading YouTube Shorts. It aims to combine AI-generated content (via Google's Gemini API) with Creative Commons background videos, automatically handling narration (Google Cloud Text-to-Speech), video editing (MoviePy), and YouTube uploads. The entire system is designed to run on a Google Cloud "Always Free" VM, exploring the possibilities of hands-free content creation.

## Proposed Structure
The system will leverage Google's Gemini AI for script generation, Google Cloud Text-to-Speech for narration, MoviePy for video editing, and yt-dlp for background video collection, all hosted on a Google Cloud "Always Free" tier VM.
This project is designed to be refactored into modular components for better readability, maintainability, and reusability.

youtube_automation/

├── .env                              # Stores API keys and sensitive paths

├── client_secrets.json               # Google OAuth 2.0 Client ID JSON

├── google-tts-service-account.json   # Google Cloud TTS Service Account JSON (if used)

├── config.py                         # All configurable constants

├── utils/                            # Shared utility functions

│   ├── __init__.py                   # Makes 'utils' a Python package

│   ├── google_auth.py                # Handles all Google API authentication

│   └── drive_helpers.py              # Google Drive specific common operations

├── collector/                        # Modules for the video collection process

│   ├── __init__.py                   # Makes 'collector' a Python package

│   ├── main.py                       # Main script to run the collector

│   └── Youtube.py             # Handles YouTube Data API searches

├── automator/                        # Modules for the video creation and upload process

│   ├── __init__.py                   # Makes 'automator' a Python package

│   ├── main.py                       # Main script to run the automator

│   ├── ai_content.py                 # Gemini API interaction for content generation

│   ├── tts_audio.py                  # Text-to-Speech generation

│   ├── video_editor.py               # Video composition using MoviePy

│   └── youtube_uploader.py           # YouTube API interaction for uploads

├── downloaded_cc_videos/             # Local temporary storage for collected videos

└── processed_videos/                 # Local temporary storage for generated videos/audio


## Secrets
To ensure the security of personal API keys and credentials, the following files must NOT be committed to the Git repository. These files contain sensitive information that should remain private.

Files to Exclude from Repository:

`.env`

This file stores your YOUTUBE_API_KEY, GEMINI_API_KEY, and the GOOGLE_TTS_SERVICE_ACCOUNT_PATH. Exposing these keys could lead to unauthorized access to your Google Cloud services and incur unexpected costs.

`client_secrets.json`

This JSON file contains your Google OAuth 2.0 Client ID and Client Secret. It's crucial for authenticating with Google Drive and YouTube for uploads. Sharing this would compromise your Google account's access.

`google-tts-service-account.json`

This JSON file contains the private key for your Google Cloud Text-to-Speech service account. It grants programmatic access to the TTS API.

`token.json`

This file is generated automatically after your first successful Google API authentication. It stores your OAuth access and refresh tokens. It should always remain local to your VM and never be shared.
