import os
import time
import shutil

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload

from google.cloud import error_reporting

from file_select import file_selector
from select_snippet import upload_random_video

scopes = "https://www.googleapis.com/auth/youtube.upload"

def upload_short(youtube):

    title, tags = upload_random_video()

    description = title

    file_location, video = file_selector()

    source = os.path.join('C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content\\used_content', video)
    destination = os.path.join('C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content\\sorted_content', video)

    while True:
        client = error_reporting.Client(project='youtube-auto-scheduler')
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
                media_body=MediaFileUpload(file_location)
            )
            response = request.execute()
            print(response)
            break # If no error, break the loop
        except HttpError as e:
            if e.resp.status == 500:
                print('HTTP 500 error, retrying...')
                client.report_exception()
                shutil.move(source, destination)
                time.sleep(10) # Wait for 10 seconds before retrying
            elif e.resp.status == 400:
                print('HTTP 400 error, retrying...')
                client.report_exception()
                shutil.move(source, destination)
                time.sleep(10) # Wait for 10 seconds before retrying
            else:
                print('Unforseen Error')
                client.report_exception()
                shutil.move(source, destination)
                raise # If it's a different error, re-raise it#