import os
import shutil

# Path to the main folder containing subfolders
main_folder = "C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content"

# Path to the new folder where all videos will be moved
destination_folder = "C:\\Users\\bluch\\Desktop\\youtube auto scheduler\\youtube_auto_scheduler\\video_content\\sorted_content"

# Iterate through each subfolder (Bulk 1 to Bulk 10)
for i in range(1, 11):
    subfolder_path = os.path.join(main_folder, f"(Bulk {i}) Add a heading")

    # Iterate through files (videos) in each subfolder
    for j in range(1, 26):
        video_source = os.path.join(subfolder_path, f"{j}.mp4")
        video_destination = os.path.join(destination_folder, f"{(i-1) * 25 + j}.mp4")

        # Move and rename the video files to the destination folder
        shutil.move(video_source, video_destination)

print("Videos moved and renamed successfully.")