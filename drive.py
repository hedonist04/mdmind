from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

import io
from pathlib import Path
from datetime import datetime


def get_creds(client_secrets_path, token_path, scopes):
    client_secrets_path = Path(client_secrets_path)
    token_path = Path(token_path)

    c = None
    if token_path.exists():
        c = Credentials.from_authorized_user_file(str(token_path), scopes)
    if c and c.valid:
        return c

    flow = InstalledAppFlow.from_client_secrets_file(
        str(client_secrets_path), scopes
    )
    c = flow.run_local_server()

    with open(token_path, "w") as f:
        f.write(c.to_json())

    return c


def get_default_creds():
    return get_creds(
        'google_drive_secrets/client_secret.json',
        'google_drive_secrets/token.json',
        ['https://www.googleapis.com/auth/drive'],
    )


def build_service(creds=get_default_creds()):
    return build("drive", "v3", credentials=creds)


def create_working_folder(service, folder_name, parents=['root']):
    res = service.files().create(body={
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': parents
    }).execute()

    return res['id']


def get_working_folder_id(service, folder_name):
    res = service.files().list(
        q=f"'root' in parents and name = '{folder_name}' and not trashed"
    ).execute()
    if not res['files']:
        return create_working_folder(service, folder_name)
    print(res)
    return res['files'][0]['id']


def upload(service, parent_folder_id, path):
    path = Path(path)
    res = service.files().create(
        body={
            'name': path.name,
            'parents': [parent_folder_id]
        },
        media_body=MediaFileUpload(path)
    ).execute()
    return res


def download(service, file_id, path):
    stream = io.BytesIO()
    downloader = MediaIoBaseDownload(
        fd=stream, 
        request=service.files().get_media(fileId=file_id)
    )

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(status.progress() * 100)

    stream.seek(0)

    with open(path, 'wb') as f:
        f.write(stream.read())


def download_latest_from_folder(service, folder_id, path):
    res = service.files().list(
        q=f"'{folder_id}' in parents",
        fields='files(id, name, modifiedTime)'
    ).execute()

    x = None
    file_id = None
    for f in res['files']:
        t = datetime.strptime(f['modifiedTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not x or t > x:
            x = t
            print(f)
            file_id = f['id']

    if file_id:
        download(service, file_id, path)

