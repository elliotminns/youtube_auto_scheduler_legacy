from video import Video
from queue_manager import upload_queue, save_queue

def add_video_to_queue():
    file_path = input("Enter the video file path: ")
    title = input("Enter the video title: ")
    tags = input("Enter the video tags (comma-separated): ").split(',')
    description = input("Enter the video description: ")

    video = Video(file_path, title, tags, description)
    upload_queue.put(video)
    save_queue()
    print(f"Video '{title}' added to the upload queue.")

def cli_menu():
    while True:
        print("\nOptions:")
        print("1. Add video to queue")
        print("2. Start scheduler")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_video_to_queue()
        elif choice == '2':
            from schedule import start_scheduler
            print("Starting scheduler...")
            start_scheduler()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
