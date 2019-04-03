import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRET = 'secrets/client_secret.json'
TOKEN_STORAGE = 'secrets/token.pickle'

def get_credentials():
    creds = None

    if os.path.exists('secrets/token.pickle'):
        with open(TOKEN_STORAGE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(TOKEN_STORAGE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


credentials = get_credentials()
service = build('gmail', 'v1', credentials=credentials)

# Call the Gmail API
# results = service.users().labels().list(userId='me').execute()
# labels = results.get('labels', [])
