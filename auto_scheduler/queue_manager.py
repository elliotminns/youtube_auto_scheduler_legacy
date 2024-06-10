import os
import json
from queue import Queue
from video import Video

upload_queue = Queue()

def save_queue():
    queue_list = []
    while not upload_queue.empty():
        queue_list.append(upload_queue.get().to_dict())

    for item in queue_list:
        upload_queue.put(Video.from_dict(item))

    with open('queue.json', 'w') as f:
        json.dump(queue_list, f)

def load_queue():
    if os.path.exists('queue.json'):
        with open('queue.json', 'r') as f:
            queue_list = json.load(f)
            for item in queue_list:
                upload_queue.put(Video.from_dict(item))

def delete_video(index):
    queue_list = []
    while not upload_queue.empty():
        queue_list.append(upload_queue.get())

    if 0 <= index < len(queue_list):
        deleted_item = queue_list.pop(index)
        print(f"Deleted item: {deleted_item.title}")
    else:
        print("Invalid index.")

    for item in queue_list:
        upload_queue.put(item)
    
    save_queue()


#need to make it so listbox updates when video is added to queue