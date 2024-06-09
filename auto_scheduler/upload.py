import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from authenticate import credential_check

def upload_video(video_path, title, tags, description):
    try:
        credentials = credential_check()
        print(credentials)
        youtube = build('youtube', 'v3', credentials=credentials)
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '22',  # Category for "People & Blogs"
            },
            'status': {
                'privacyStatus': 'public',
            }
        }
        media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file
        )
        response = request.execute()
        logging.info(f"Video uploaded: {response['id']}")
        return True
    except HttpError as e:
        logging.error(f"An error occurred: {e}")
        return False
