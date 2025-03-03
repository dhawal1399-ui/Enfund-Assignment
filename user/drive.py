import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE_DIR = Path(__file__).resolve().parent.parent  
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "myAssignment/config", "google_credentials.json")

SCOPES = ['https://www.googleapis.com/auth/drive']

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API client
service = build('drive', 'v3', credentials=credentials)

def get_drive_service():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Google credentials file not found at: {SERVICE_ACCOUNT_FILE}")

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

def upload_file(file_path, mime_type, folder_id='15mSKfKaH7gcIAjWxMBw_DSfvG_1M78C0'):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at: {file_path}")

    file_metadata = {'name': os.path.basename(file_path)}
    
    if folder_id:
        file_metadata['parents'] = [folder_id]
        print(f"Uploading to Folder ID: {folder_id}")  

    media = MediaFileUpload(file_path, mimetype=mime_type)

    drive_service = get_drive_service()
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, parents'
    ).execute()

    print(f"✅ File uploaded successfully! File ID: {file.get('id')}, Parent Folder: {file.get('parents')}")
    return file.get('id')

# def get_drive_service():
#     """Authenticate and return the Google Drive service instance."""
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES
#     )
#     return build('drive', 'v3', credentials=credentials)

def list_drive_files():
    """Fetches and prints the list of files from Google Drive."""
    drive_service = get_drive_service()
    results = drive_service.files().list(
        pageSize=10, fields="files(id, name)"
    ).execute()

    files = results.get('files', [])
    if not files:
        print("No files found.")
    else:
        print("Files:")
        for file in files:
            print(f"{file['name']} (ID: {file['id']})")

if __name__ == "__main__":
    list_drive_files()