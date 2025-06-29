# --- File: utils/google_auth.py ---

import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
import os
import config # Import the central configuration

def get_google_credentials(scopes, client_secrets_file):
    """
    Handles Google OAuth 2.0 authentication for specified scopes.
    The first time this runs, it will open a browser window for you to grant permissions.
    Subsequent runs will use a stored token.json.

    Args:
        scopes (list): A list of Google API scopes (e.g., ["https://www.googleapis.com/auth/drive.file"]).
        client_secrets_file (str): Path to your client_secrets.json file.

    Returns:
        google.oauth2.credentials.Credentials: Authenticated Google Credentials object.
    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    # This will open a browser for you to authorize. After authorization, credentials
    # are saved in 'token.json' (by default, in the same directory as this script,
    # or the script that calls this. Better to ensure it's in the main project folder).
    credentials = flow.run_local_server(port=0)
    print(f"Google authentication successful for scopes: {', '.join(scopes)}")
    return credentials

def build_youtube_service(read_only=True):
    """
    Builds and returns an authenticated YouTube API service object.

    Args:
        read_only (bool): If True, authenticates for read-only (search) scope.
                          If False, authenticates for upload scope.
    """
    print(f"Authenticating with YouTube Data API ({'Read-Only' if read_only else 'Upload'})...")
    if read_only:
        return build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)
    else:
        credentials = get_google_credentials([config.YOUTUBE_UPLOAD_SCOPE], config.CLIENT_SECRETS_FILE)
        return build('youtube', 'v3', credentials=credentials)

def build_drive_service(read_only=True):
    """
    Builds and returns an authenticated Google Drive API service object.

    Args:
        read_only (bool): If True, authenticates for read-only scope.
                          If False, authenticates for file management (upload) scope.
    """
    print(f"Authenticating with Google Drive API ({'Read-Only' if read_only else 'File Management'})...")
    scopes = [config.DRIVE_READONLY_SCOPE] if read_only else [config.DRIVE_FILE_SCOPE]
    credentials = get_google_credentials(scopes, config.CLIENT_SECRETS_FILE)
    return build('drive', 'v3', credentials=credentials)
utils/drive_helpers.py
Python

# --- File: utils/drive_helpers.py ---

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os

def get_drive_folder_id(drive_service, folder_name):
    """
    Gets the ID of a Google Drive folder by its name. If the folder doesn't exist, it creates it.

    Args:
        drive_service: Authenticated Google Drive API service object.
        folder_name (str): The name of the folder to find or create.

    Returns:
        str: The ID of the Google Drive folder. None if creation/retrieval fails.
    """
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and 'me' in owners"
    try:
        response = drive_service.files().list(q=query, spaces='drive').execute()
        items = response.get('files', [])

        if items:
            print(f"Found existing Google Drive folder: '{folder_name}' (ID: {items[0]['id']})")
            return items[0]['id']
        else:
            print(f"Creating new Google Drive folder: '{folder_name}'...")
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive_service.files().create(body=file_metadata, fields='id').execute()
            print(f"Successfully created folder: '{folder_name}' (ID: {folder.get('id')})")
            return folder.get('id')
    except HttpError as e:
        print(f"ERROR: An HTTP error occurred accessing Google Drive folder: {e.resp.status}, {e.content.decode()}")
        return None
    except Exception as e:
        print(f"ERROR: An unexpected error occurred in get_drive_folder_id: {e}")
        return None

def upload_file_to_drive(drive_service, file_path, folder_id, drive_title, drive_description, mimetype='video/mp4'):
    """
    Uploads a file to a specified folder in Google Drive.

    Args:
        drive_service: Authenticated Google Drive API service object.
        file_path (str): The full path to the local file to upload.
        folder_id (str): The ID of the Google Drive folder to upload to.
        drive_title (str): The title to use for the file in Google Drive.
        drive_description (str): A description to add to the Drive file.
        mimetype (str): The MIME type of the file (e.g., 'video/mp4', 'audio/mp3').

    Returns:
        bool: True if upload is successful, False otherwise.
    """
    file_name_for_logging = os.path.basename(file_path)
    print(f"Attempting to upload '{file_name_for_logging}' to Google Drive...")
    file_metadata = {
        'name': drive_title,
        'parents': [folder_id],
        'description': drive_description
    }
    media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)
    try:
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name').execute()
        print(f"SUCCESS: Uploaded '{file.get('name')}' (ID: {file.get('id')}) to Google Drive.")
        return True
    except HttpError as e:
        print(f"ERROR: Error uploading '{file_name_for_logging}' to Drive: {e.resp.status}, {e.content.decode()}")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error during Drive upload of '{file_name_for_logging}': {e}")
        return False

def list_files_in_drive_folder(drive_service, folder_id):
    """
    Lists files (non-folders) in a given Google Drive folder.

    Args:
        drive_service: Authenticated Google Drive API service object.
        folder_id (str): The ID of the Google Drive folder to list files from.

    Returns:
        list: A list of dictionaries, each representing a file with 'id', 'name', 'webContentLink'.
    """
    files = []
    page_token = None
    while True:
        try:
            response = drive_service.files().list(
                q=f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'",
                spaces='drive',
                fields='nextPageToken, files(id, name, webContentLink)',
                pageToken=page_token
            ).execute()
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
        except Exception as e:
            print(f"ERROR: Could not list files in Drive folder {folder_id}: {e}")
            break
    return files