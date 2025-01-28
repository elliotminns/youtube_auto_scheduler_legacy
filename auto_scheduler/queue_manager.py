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

def view_queue():
    if upload_queue.empty():
        print("Queue is empty.")
    else:
        print("Current Queue:")
        for index, item in enumerate(upload_queue.queue, 1):
            print(f"{index}. {item.title}")

def delete_from_queue(index):
    if not 1 <= index <= upload_queue.qsize():
        print("Invalid index.")
        return

    temp_queue = Queue()
    deleted_item = None

    # Iterate through the queue and skip the item at the specified index
    for i in range(1, upload_queue.qsize() + 1):
        item = upload_queue.get()
        if i == index:
            deleted_item = item  # Save the item to be deleted
        else:
            temp_queue.put(item)  # Add all other items back to a temporary queue

    # Replace the original queue with the updated one
    while not temp_queue.empty():
        upload_queue.put(temp_queue.get())

    if deleted_item:
        print(f"Deleted item: {deleted_item.title}")