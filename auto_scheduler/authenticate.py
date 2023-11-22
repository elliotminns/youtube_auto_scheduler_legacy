import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import json
from google.oauth2.credentials import Credentials  # Import Credentials class
from google.auth.transport.requests import Request  # Import Request class

from googleapiclient.http import MediaFileUpload

scopes = "https://www.googleapis.com/auth/youtube.upload"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "resources/credentials.json"

def is_authorized(credentials):
    return credentials and not credentials.expired

def authorize():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    
    save_credentials(credentials)
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    print ('New Credentials')
    return(youtube)

def refresh(credentials):
    if credentials and credentials.refresh_token:
        credentials.refresh(Request())
        save_credentials(credentials)
        print('Credentials Refreshed')
        return credentials
    else:
        return None
    
def save_credentials(credentials):
    with open('resources/token.json', 'w') as token_file:
        token_file.write(credentials.to_json())

def credential_check():
    try:
        with open('resources/token.json', 'r') as token_file:
            credentials_data = json.load(token_file)
        credentials = Credentials.from_authorized_user_info(credentials_data)
        print ('Credentials Found')
    except FileNotFoundError:
        credentials = None
        print ('Credentials not Found')
    
    if is_authorized(credentials):
        print('Still Authorized')

        youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

        return(youtube)
    else:
        refreshed_credentials = refresh(credentials)
        if refreshed_credentials and is_authorized(refreshed_credentials):

            youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

            return(youtube)
        else:
            print('Credentials Expired')
            authorize()