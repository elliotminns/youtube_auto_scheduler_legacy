import os
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload

from authenticate import credential_check

#scopes = ["https://www.googleapis.com/auth/youtube.upload"] - Upload Scope
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

output_file = 'tags.txt'

def get_tags(youtube):

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="GB"
    )
    response = request.execute()
    extract_and_append_tags(response)

def extract_and_append_tags(data):
    try:
        # Extract tags from each video item
        all_tags = []
        for item in data.get('items', []):
            video_tags = item.get('snippet', {}).get('tags', [])
            all_tags.extend(video_tags)

        # Append tags to the existing file or create a new one if it doesn't exist
        with open(output_file, 'a') as file:
            for tag in all_tags:
                file.write(tag + '\n')
        
        print(f"Tags successfully extracted and appended to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    youtube = credential_check()
    get_tags(youtube)