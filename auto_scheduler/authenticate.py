import os  # Import os module for operating system functionalities
import google_auth_oauthlib.flow  # Import flow module from google_auth_oauthlib package
import googleapiclient.discovery  # Import discovery module from googleapiclient package
import json  # Import json module for JSON data manipulation
from google.oauth2.credentials import Credentials  # Import Credentials class from google.oauth2.credentials package
from google.auth.transport.requests import Request  # Import Request class from google.auth.transport.requests package
from googleapiclient.http import MediaFileUpload  # Import MediaFileUpload class from googleapiclient.http package

scopes = "https://www.googleapis.com/auth/youtube.upload"  # Define OAuth scopes required for YouTube API access

api_service_name = "youtube"  # Define the API service name
api_version = "v3"  # Define the API version
client_secrets_file = "auto_scheduler/resources/credentials.json"  # Path to the client secrets file containing OAuth 2.0 information

# Function to check if credentials are authorized
def is_authorized(credentials):
    return credentials and not credentials.expired

# Function to authorize access to YouTube API
def authorize():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Set environment variable for insecure transport
    
    # Start the OAuth 2.0 Authorization Flow
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()  # Run local server to handle OAuth redirect
    
    save_credentials(credentials)  # Save the obtained credentials
    
    # Build the YouTube API client with the obtained credentials
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    print('New Credentials')  # Print confirmation message
    return youtube  # Return the YouTube API client

# Function to refresh expired credentials
def refresh(credentials):
    if credentials and credentials.refresh_token:
        credentials.refresh(Request())  # Refresh the credentials
        save_credentials(credentials)  # Save the refreshed credentials
        print('Credentials Refreshed')  # Print confirmation message
        return credentials  # Return the refreshed credentials
    else:
        return None  # Return None if no credentials or refresh token is found

# Function to save credentials to a file
def save_credentials(credentials):
    with open('auto_scheduler/resources/token.json', 'w') as token_file:
        token_file.write(credentials.to_json())  # Write credentials to JSON file

# Function to check if credentials are available and authorized
def credential_check():
    try:
        with open('auto_scheduler/resources/token.json', 'r') as token_file:
            credentials_data = json.load(token_file)  # Load credentials data from file
        credentials = Credentials.from_authorized_user_info(credentials_data)  # Create credentials from loaded data
        print('Credentials Found')  # Print confirmation message
    except FileNotFoundError:
        credentials = None  # Set credentials to None if file is not found
        print('Credentials not Found')  # Print message if file is not found
    
    if is_authorized(credentials):  # Check if credentials are authorized
        print('Still Authorized')  # Print confirmation message
        
        # Build the YouTube API client with the obtained credentials
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube  # Return the YouTube API client
    else:
        refreshed_credentials = refresh(credentials)  # Refresh credentials if expired
        if refreshed_credentials and is_authorized(refreshed_credentials):
            # Build the YouTube API client with the refreshed credentials
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)

            return youtube  # Return the YouTube API client
        else:
            print('Credentials Expired')  # Print message if credentials are expired
            authorize()  # Authorize access to YouTube API
