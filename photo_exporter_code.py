from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import os

# Path to your Google API credentials JSON file
CREDENTIALS_FILE = "credentials.json"

# Folder containing your iCloud photos/videos
LOCAL_FOLDER = "path/to/icloud/downloads"

# Optional: Google Drive folder ID where files will be uploaded
GDRIVE_FOLDER_ID = "your_google_drive_folder_id"  # Leave blank to upload to root

# Authenticate and build the Drive API service
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
creds = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
service = build("drive", "v3", credentials=creds)

def upload_to_drive(file_path):
    file_name = os.path.basename(file_path)
    
    # Metadata for the file
    file_metadata = {"name": file_name}
    if GDRIVE_FOLDER_ID:
        file_metadata["parents"] = [GDRIVE_FOLDER_ID]

    # Upload the file
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    print(f"Uploaded {file_name} - File ID: {uploaded_file.get('id')}")

# Loop through all files in the folder and upload them
for file in os.listdir(LOCAL_FOLDER):
    file_path = os.path.join(LOCAL_FOLDER, file)
    if os.path.isfile(file_path):
        upload_to_drive(file_path)
