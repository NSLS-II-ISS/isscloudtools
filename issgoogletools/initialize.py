

from __future__ import print_function
# import httplib2
# import os
#
# from googleapiclient import discovery
# from oauth2client import client
# from oauth2client import tools
# from oauth2client.file import Storage
#
# import datetime
#
# from googleapiclient.http import MediaFileUpload
#
#
#
#
# from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_gdrive_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/xf08id/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service













#
#
# def get_gdrive_service():
#     # try:
#     #     import argparse
#     #     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#     # except ImportError:
#     #     flags = None
#
#     flags = None
#
#     SCOPES = 'https://www.googleapis.com/auth/drive'
#     CLIENT_SECRET_FILE = 'client_secret.json'
#     APPLICATION_NAME = 'Drive API Python Quickstart'
#
#     """Gets valid user credentials from storage.
#
#     If nothing has been stored, or if the stored credentials are invalid,
#     the OAuth2 flow is completed to obtain the new credentials.
#
#     Returns:
#         Credentials, the obtained credential.
#     """
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     if not os.path.exists(credential_dir):
#         os.makedirs(credential_dir)
#     credential_path = os.path.join(credential_dir,
#                                    'drive-python-quickstart.json')
#
#     store = Storage(credential_path)
#     credentials = store.get()
#     if not credentials or credentials.invalid:
#         flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
#         flow.user_agent = APPLICATION_NAME
#         if flags:
#             credentials = tools.run_flow(flow, store, flags)
#         else: # Needed only for compatibility with Python 2.6
#             credentials = tools.run_flow(flow, store)
#         print('Storing credentials to ' + credential_path)
#
#     http = credentials.authorize(httplib2.Http())
#     drive_service = discovery.build('drive', 'v3', http=http)
#     return drive_service