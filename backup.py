import os
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

class GDrive():
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('drive', 'v3', credentials=creds)

    def update(self, filename, path, id):
        media = MediaFileUpload(f"{path}{filename}")
        modification_time = datetime.datetime.utcfromtimestamp(os.path.getmtime(path + filename)).strftime('%Y-%m-%dT%H:%M:%S')

        search = self.service.files().list(
            q=f"name='{filename}' and parents='{id}'",
            spaces='drive',
            fields='nextPageToken, files(id, name)',
            pageToken=None).execute()

        time = self.service.files().list(
            q=f"name='{filename}' and parents='{id}' and modifiedTime<'{modification_time}'",
            spaces='drive',
            fields='nextPageToken, files(id, name, modifiedTime)',
            pageToken=None).execute()

        if len(search['files']) == 0:
            metadata = {'name': filename, 'parents': [id]}
            self.service.files().create(body=metadata, media_body=media, fields='id').execute()

        else:
            for file in time.get('files', []):
                self.service.files().update(
                    fileId=file.get('id'),
                    media_body=media,
                ).execute()

    def folder(self, name):
        get_folder = self.service.files().list(q=f"name='{name}' and mimeType='application/vnd.google-apps.folder'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=None).execute()
        for file in get_folder.get('files', []):
            return file.get('id')

def main():
    drive = GDrive()
    path = "Your Folder's Path"
    drive_folder_name = "Your Google Drive Folder Name"
    id = drive.folder(drive_folder_name)
    new_files = [os.path.join(path, name) for path, subdirs, files in os.walk(path) for name in files]
    for item in new_files:
        name = os.path.basename(item)
        location = item.replace(name,"")
        drive.update(name, location, id)

if __name__ == '__main__':
    main()