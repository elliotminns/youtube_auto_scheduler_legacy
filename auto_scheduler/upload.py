import os
import time

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload

from authenticate import credential_check
from file_select import file_selector
from select_snippet import upload_random_video

scopes = "https://www.googleapis.com/auth/youtube.upload"

def upload_short(youtube):

    title, tags = upload_random_video()

    description = title

    while True:
        try:
            request = youtube.videos().insert(
                part='snippet',
                body={
                    "snippet": {
                        "title": title,
                        "tags": tags,
                        "description": description
                    }
                },
                media_body=MediaFileUpload(file_selector())
            )
            response = request.execute()
            print(response)
            break # If no error, break the loop
        except HttpError as e:
            if e.resp.status == 500:
                print('HTTP 500 error, retrying...')
                time.sleep(10) # Wait for 10 seconds before retrying
            else:
                raise # If it's a different error, re-raise it#

if __name__ == "__main__":
    youtube = credential_check()
    upload_short(youtube)