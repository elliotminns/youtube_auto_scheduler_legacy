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
    deleted_item = None
    for _ in range(index):
        deleted_item = upload_queue.get()
        upload_queue.put(deleted_item)
    upload_queue.get()
    print(f"Deleted item: {deleted_item.title}")

# Example usage:
# Call load_queue() to load queue from file

# Call view_queue() to view the queue

# Call delete_from_queue(index) to delete an item from the queue
