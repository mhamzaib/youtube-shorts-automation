import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Ensure .env is in the project root (youtube_automation/)
load_dotenv()

# =======================================================================================
#                             COMMON CONFIGURATION (for both collector & automator)
# =======================================================================================

# --- API Keys & Credentials ---
# WHERE TO GET THESE:
#   - Google Cloud Console (console.cloud.google.com).
#   - Select your project or create a new one.
#   - Navigate to "APIs & Services" -> "Credentials".

# YouTube Data API Key: For searching videos.
#   - TODO: Add to .env: YOUTUBE_API_KEY="YOUR_YOUTUBE_DATA_API_KEY"
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in .env file. Please add it.")

# Gemini API Key: For story generation.
#   - Go to Google AI Studio (aistudio.google.com) or Google Cloud Console -> Vertex AI.
#   - Create a new API key. Add it to .env: GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please add it.")

# Google Cloud Text-to-Speech (TTS) Service Account Key Path: For narration voiceover.
#   - Enable "Cloud Text-to-Speech API" in Google Cloud Console.
#   - Go to "IAM & Admin" -> "Service Accounts". Create new, grant "Cloud Text-to-Speech User" role.
#   - Create a new key (JSON type) and download it.
#   - Add path to .env: GOOGLE_TTS_SERVICE_ACCOUNT_PATH="/path/to/your/google-tts-service-account.json"
GOOGLE_TTS_SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_TTS_SERVICE_ACCOUNT_PATH")
# If using another TTS provider with a simple API key, configure it here instead:
# TTS_API_KEY = os.getenv("TTS_API_KEY")

# OAuth 2.0 Client ID File: For Google Drive (upload/read) and YouTube Upload.
#   - Create in Google Cloud Console -> Credentials -> "OAuth client ID" -> "Desktop app".
#   - Download JSON and place it in the project root.
CLIENT_SECRETS_FILE = 'client_secrets.json'
if not os.path.exists(CLIENT_SECRETS_FILE):
    raise FileNotFoundError(f"{CLIENT_SECRETS_FILE} not found. Please download it from Google Cloud Console and place it in the project root.")

# --- API Scopes (Permissions) ---
# YOUTUBE_READ_SCOPE: For searching YouTube videos.
YOUTUBE_READ_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
# YOUTUBE_UPLOAD_SCOPE: For uploading videos to your YouTube channel.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
# DRIVE_FILE_SCOPE: For uploading files to Google Drive (collector). Allows app to only manage files it creates.
DRIVE_FILE_SCOPE = "https://www.googleapis.com/auth/drive.file"
# DRIVE_READONLY_SCOPE: For reading (listing/downloading) files from Google Drive (automator).
DRIVE_READONLY_SCOPE = "https://www.googleapis.com/auth/drive.readonly"

# --- Local & Google Drive Folder Paths ---
# LOCAL_DOWNLOAD_FOLDER: Where collected CC videos are temporarily stored before Drive upload.
LOCAL_DOWNLOAD_FOLDER = 'downloaded_cc_videos'
# LOCAL_PROCESSED_FOLDER: Where generated audio/video are temporarily stored before YouTube upload.
LOCAL_PROCESSED_FOLDER = 'processed_videos'
# GOOGLE_DRIVE_CC_FOLDER_NAME: Name of the folder in your Google Drive for collected CC videos.
GOOGLE_DRIVE_CC_FOLDER_NAME = 'Automated YT Backgrounds CC Shorts'

# =======================================================================================
#                            COLLECTOR SPECIFIC CONFIGURATION
# =======================================================================================

# --- Youtube Parameters ---
# Search queries for the `cc_video_collector`. Add terms relevant to Shorts!
COLLECTOR_SEARCH_QUERIES = [
    "minecraft parkour shorts creative commons",
    "subway surfers gameplay vertical creative commons",
    "mobile game endless runner creative commons short",
    "satisfying animation short creative commons",
    "asmr gameplay no commentary short creative commons"
]
COLLECTOR_NUM_VIDEOS_PER_QUERY = 5 # Target number of successfully downloaded/uploaded videos per query.
COLLECTOR_LATEST_DAYS = 180       # Look for videos published in the last N days (to keep content fresh).

# --- YouTube-DLP Download Settings for Shorts ---
# YouTube Shorts must be 60 seconds or less. We download slightly longer to allow for trimming.
MIN_VIDEO_DURATION_SECONDS = 20 # Minimum duration for downloaded videos
MAX_VIDEO_DURATION_SECONDS = 70 # Maximum duration for downloaded videos (a bit over 60s for trimming)
MAX_DOWNLOAD_FILESIZE_MB = 100  # Max file size in MB. Shorts are typically small.

# =======================================================================================
#                            AUTOMATOR SPECIFIC CONFIGURATION
# =======================================================================================

# --- Video Output Settings for YouTube Shorts ---
VIDEO_FPS = 30 # Frames per second for the output video (30 or 60 are common for Shorts)
# YouTube Shorts require a vertical aspect ratio (9:16).
# (width, height)
VIDEO_RESOLUTION = (1080, 1920) # 1080p Full HD vertical

# --- Narration & Story Generation Settings ---
# Target duration for the generated narration to fit within 60-second Shorts limit.
# A 50-second narration gives some buffer for intro/outro/music if added later.
TARGET_NARRATION_DURATION_SECONDS = 50
# Speaking rate for TTS: 1.0 is normal. Adjust if your generated scripts are too long/short for target duration.
TTS_SPEAKING_RATE = 1.0
# Google Cloud TTS Voice Name: Choose from https://cloud.google.com/text-to-speech/docs/voices
TTS_VOICE_NAME = "en-US-Standard-C" # A common, balanced voice. Try 'en-US-Wavenet-F' or 'en-US-Neural2-D' for higher quality.
TTS_VOICE_GENDER = "FEMALE" # Options: FEMALE, MALE, NEUTRAL

# --- YouTube Upload Settings ---
# YouTube Category ID: 22 for 'People & Blogs' (common for storytime).
# See: https://developers.google.com/youtube/v3/docs/videoCategories/list
YOUTUBE_CATEGORY_ID = '22'
# Privacy status for uploaded videos: 'public', 'unlisted', or 'private'.
# 'unlisted' is highly recommended for initial review before making public.
YOUTUBE_UPLOAD_PRIVACY_STATUS = 'unlisted'
# Whether content is made for kids (affects monetization/features).
YOUTUBE_MADE_FOR_KIDS = False