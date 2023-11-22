import os
import time
import shutil

from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload

from google.cloud import error_reporting

from authenticate import credential_check
from file_select import file_selector
from select_snippet import upload_random_video

scopes = "https://www.googleapis.com/auth/youtube.upload"

def upload_short(youtube):

    title, tags = upload_random_video()

    description = title

    e500 = 10
    e400 = 600

    while True:
        try:
            file_location, video = file_selector()
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
            if e.resp.status >= 500:
                print(f'{e.resp.status} Server Error, retrying in 10 seconds...')
                HTTP_error(video, e500)
                
            elif e.resp.status >= 400 & e.resp.status <= 499:
                print(f'{e.resp.status} Client Error, retrying in 10 minutes...')
                HTTP_error(video, e400)

            elif e.resp.status >= 300 & e.resp.status <= 399:
                print(f'{e.resp.status} Redirect Response, retrying in 10 seconds...')
                HTTP_error(video, e500)

            else:
                print('Unforseen Error')
                HTTP_error(video, e500)
                break

def HTTP_error(video, delay):
    
    client = error_reporting.Client(project='youtube-auto-scheduler')
    client.report_exception()

    source = os.path.join('C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content\\used_content', video)
    destination = os.path.join('C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content\\sorted_content', video)
    shutil.move(source, destination)
    time.sleep(delay)

youtube_obj = credential_check()
upload_short(youtube_obj)