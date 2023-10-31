import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.auth

import json

from googleapiclient.http import MediaFileUpload

#Change this when changing post from test to post
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "credentials.json"

   # Try to load credentials from a file, if they exist
    credentials = load_credentials()

    if credentials is None:
        # Initialize the flow
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)

        # If no credentials file exists, initiate the OAuth flow
        credentials = flow.run_local_server()

        # Save the credentials to a file
        save_credentials(credentials)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    print(youtube)

def post(youtube):
    """""
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id="Ks-_Mh1QhMc"
    )
    response = request.execute()

    print(response)
    """""


def load_credentials():
    if os.path.exists('token.json'):
        return google.auth.credentials.Credentials.from_authorized_user_info('token.json', scopes)
    return None

def save_credentials(credentials):
    credentials.to_json()
    with open('token.json', 'w') as token_file:
        token_file.write(credentials.to_json())

if __name__ == "__main__":
    main()