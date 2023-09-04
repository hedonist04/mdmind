import googleapiclient.http
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from pprint import pp
import googleapiclient.discovery
from dataclasses import dataclass
import io

from pathlib import Path

def get_credentials(secrets_path=Path.cwd() / 'google_drive_secrets'):
    secrets_path = Path(secrets_path)
    secrets_path.mkdir(parents=True, exist_ok=True)

    token_path = secrets_path / 'token.json'
    client_secrets_path = secrets_path / 'client_secrets.json'

    assert client_secrets_path.exists()

    scopes = ['https://www.googleapis.com/auth/drive']

    c = None
    if token_path.exists():
        c = Credentials.from_authorized_user_file(
            str(token_path), scopes
        )
    if c and c.valid:
        return c

    if c and c.expired and c.refresh_token:
        c.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_path), scopes
        )
        c = flow.run_local_server()

    with token_path.open('w') as f:
        f.write(c.to_json())
    return c


def get_root_folder_id(drive_service, root_folder):
    res = drive_service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{root_folder}'"
    ).execute()
    return res['files'][0]['id']


def get_remote_files(drive_service, file_id, path=''):
    res = drive_service.files().list(
        q=f"parents='{file_id}'", fields='files(id, name, mimeType)'
    ).execute()

    files = []
    for f in res.get('files', []):
        if f['mimeType'] == 'application/vnd.google-apps.folder':
            files.extend(get_remote_files(drive_service, f['id'], path=path + '/' + f['name']))
        else:
            f['path'] = path
            files.append(f)
    return files


def get_remote_mind(root_folder='mdmind'):
    drive_service = build('drive', 'v3', credentials=get_credentials())

    root_folder_id = get_root_folder_id(drive_service, root_folder)
    files = get_remote_files(drive_service, root_folder_id, path=root_folder)
    pp(files)

get_remote_mind(root_folder='tmp')
