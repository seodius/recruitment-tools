import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_drive_service():
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)

def upload_file(service, file_path, folder_id=None):
    file_metadata = {"name": os.path.basename(file_path)}
    if folder_id:
        file_metadata["parents"] = [folder_id]
    media = MediaFileUpload(file_path)
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    return file.get("id")

def export_pdf(service, file_id):
    request = service.files().export_media(fileId=file_id, mimeType="application/pdf")
    return request

def download_file(request, output_path):
    with open(output_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

def delete_file(service, file_id):
    service.files().delete(fileId=file_id).execute()

def convert_docx_to_pdf(file_path, output_path):
    service = get_drive_service()

    # Create a folder to store the uploaded file
    folder_metadata = {'name': 'ResumeConverter', 'mimeType': 'application/vnd.google-apps.folder'}
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')

    # Upload the docx file to the created folder
    docx_file_id = upload_file(service, file_path, folder_id)

    # Export the uploaded file to PDF
    pdf_request = export_pdf(service, docx_file_id)

    # Download the PDF
    download_file(pdf_request, output_path)

    # Delete the folder and its contents
    delete_file(service, folder_id)
