import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("Error: 'credentials.json' file not found.")
                print("Please follow these steps:")
                print("1. Go to the Google Cloud Console (https://console.cloud.google.com/)")
                print("2. Create a project and enable the Gmail API")
                print("3. Create OAuth 2.0 credentials (OAuth client ID, Desktop app)")
                print("4. Download the client configuration and save it as 'credentials.json' in this directory")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def delete_old_emails():
    service = get_gmail_service()
    if not service:
        return

    one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y/%m/%d')
    query = f'before:{one_year_ago}'
    
    page_token = None
    total_deleted = 0
    total_errors = 0

    while True:
        try:
            results = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
            messages = results.get('messages', [])
            
            if not messages:
                print('No more messages found.')
                break
            
            for message in messages:
                try:
                    service.users().messages().trash(userId='me', id=message['id']).execute()
                    total_deleted += 1
                    print(f"Message {message['id']} moved to trash. Total deleted: {total_deleted}")
                except HttpError as error:
                    if error.resp.status == 400 and 'Precondition check failed' in str(error):
                        print(f"Message {message['id']} already deleted or moved. Skipping.")
                        total_errors += 1
                    else:
                        raise  # Re-raise the exception if it's not the specific error we're handling
            
            page_token = results.get('nextPageToken')
            if not page_token:
                break

        except Exception as e:
            print(f"An error occurred while processing a batch: {e}")
            print("Continuing with the next batch...")
            page_token = results.get('nextPageToken')
            if not page_token:
                break

    print(f"Process completed. Total messages deleted: {total_deleted}")
    print(f"Total errors encountered: {total_errors}")

if __name__ == '__main__':
    delete_old_emails()