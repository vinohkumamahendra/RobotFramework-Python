
from __future__ import print_function
import httplib2
import os
import io
from apiclient.http import MediaIoBaseDownload

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Spread sheet allow'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    print(home_dir)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
def list_files(service):
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(**param).execute()
        for key in files.keys():
            print (key)
        for item in files['files']:
            print(item)
            yield item
        page_token = files.get('nextPageToken')
        if not page_token:
            break
    
def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http)
    
    results = drive_service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    download_url = "https://www.googleapis.com/drive/v3/files/1x4rSBVxQGAHk0ZqxWfnPpkL46w0t6VIx_dMIkOazlyU/export?mimeType=application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    outfile = "E:\google api\Vinoth Progress.xlsx"
    resp, content = drive_service._http.request(download_url)
    if resp.status == 200:
        if os.path.isfile(outfile):
            print ("ERROR, %s already exist" , outfile)
        else:
            with open(outfile, 'wb') as f:
                f.write(content)
            print ("OK")
if __name__ == '__main__':
    main()