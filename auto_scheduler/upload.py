import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload

from authenticate import credential_check

#scopes = ["https://www.googleapis.com/auth/youtube.upload"] - Upload Scope
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def upload_short(youtube):

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode="GB"
    )
    response = request.execute()
    print(response)

if __name__ == "__main__":
    youtube = credential_check()
    upload_short(youtube)