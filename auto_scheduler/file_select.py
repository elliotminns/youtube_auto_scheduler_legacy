import os
import shutil
import random

def file_selector():
   parent_folder = 'C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content'
   sorted_folder = os.path.join(parent_folder, 'sorted_content')
   used_folder = os.path.join(parent_folder, 'used_content')

   # Get a list of all video files in the sorted_content folder
   videos = os.listdir(sorted_folder)

   # Randomly select a video
   video = random.choice(videos)

   # Construct the full paths for the source and destination
   source = os.path.join(sorted_folder, video)
   destination = os.path.join(used_folder, video)

   # Move the video file from the sorted_content folder to the used_content folder
   shutil.move(source, destination)

   # Return the path of the moved video
   return destination, video

