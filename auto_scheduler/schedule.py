import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from queue_manager import upload_queue, save_queue
from upload import upload_video

def job():
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
    else:
        print("Faied to upload video")
        logging.error(f"Failed to upload video '{video.title}'.")
        # Optionally re-add to queue
        upload_queue.put(video)


def start_scheduler():
    scheduler = BlockingScheduler()
    # Monday
    scheduler.add_job(job, 'cron', day_of_week='mon', hour=18, misfire_grace_time=30)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
