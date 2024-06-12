import logging
from apscheduler.schedulers.background import BackgroundScheduler
from queue_manager import upload_queue, save_queue
from upload import upload_video
import json
import os
import threading

def job(app):
    if upload_queue.empty():
        print("No Videos in Queue")
        logging.info("No videos in the queue.")
        return

    video = upload_queue.get()
    success = upload_video(video.file_path, video.title, video.tags, video.description)
    if success:
        print(f"Video '{video.title}' uploaded successfully.")
        logging.info(f"Video '{video.title}' uploaded successfully.")
        save_queue()
        # Refresh the listbox to reflect the changes
        app.refresh_listbox_threadsafe()
    else:
        print("Failed to upload video")
        logging.error(f"Failed to upload video '{video.title}'.")
        upload_queue.put(video)

def load_schedule():
    if not os.path.exists("schedule.json"):
        return {}
    with open("schedule.json", "r") as f:
        return json.load(f)

def start_scheduler(app):
    scheduler = BackgroundScheduler()
    update_scheduler(scheduler, app)  # Initial setup
    
    # Start a separate thread to periodically check for updates in the schedule
    def schedule_updater():
        while True:
            update_scheduler(scheduler, app)
            # Check every hour for updates (adjust the time interval as needed)
            threading.Event().wait(10)

    # Start the schedule updater thread
    updater_thread = threading.Thread(target=schedule_updater, daemon=True)
    updater_thread.start()
    
    scheduler.start()
    try:
        while True:
            pass  # Keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")

def update_scheduler(scheduler, app):
    scheduler.remove_all_jobs()
    schedule = load_schedule()
    for day, times in schedule.items():
        for time in times:
            hour, minute = map(int, time.split(":"))
            scheduler.add_job(job, 'cron', day_of_week=day[:3].lower(), hour=hour, minute=minute, args=[app])

if __name__ == "__main__":
    app = None  # Use this if you need to test start_scheduler without the GUI
    start_scheduler(app)
