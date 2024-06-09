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
    scheduler.add_job(job, 'cron', day_of_week='mon', hour=18)
    scheduler.add_job(job, 'cron', day_of_week='mon', hour=19)
    scheduler.add_job(job, 'cron', day_of_week='mon', hour=20)
    scheduler.add_job(job, 'cron', day_of_week='mon', hour=21)

    # Tuesday
    scheduler.add_job(job, 'cron', day_of_week='tue', hour=18)
    scheduler.add_job(job, 'cron', day_of_week='tue', hour=19)
    scheduler.add_job(job, 'cron', day_of_week='tue', hour=20)
    scheduler.add_job(job, 'cron', day_of_week='tue', hour=21)
    scheduler.add_job(job, 'cron', day_of_week='tue', hour=22)

    # Wednesday
    scheduler.add_job(job, 'cron', day_of_week='wed', hour=18)
    scheduler.add_job(job, 'cron', day_of_week='wed', hour=19)
    scheduler.add_job(job, 'cron', day_of_week='wed', hour=20)
    scheduler.add_job(job, 'cron', day_of_week='wed', hour=21)
    scheduler.add_job(job, 'cron', day_of_week='wed', hour=22)

    # Thursday
    scheduler.add_job(job, 'cron', day_of_week='thu', hour=18)
    scheduler.add_job(job, 'cron', day_of_week='thu', hour=19)
    scheduler.add_job(job, 'cron', day_of_week='thu', hour=20)
    scheduler.add_job(job, 'cron', day_of_week='thu', hour=21)

    # Friday
    scheduler.add_job(job, 'cron', day_of_week='fri', hour=16)
    scheduler.add_job(job, 'cron', day_of_week='fri', hour=17)
    scheduler.add_job(job, 'cron', day_of_week='fri', hour=18)
    scheduler.add_job(job, 'cron', day_of_week='fri', hour=19)
    scheduler.add_job(job, 'cron', day_of_week='fri', hour=20)

    # Saturday
    scheduler.add_job(job, 'cron', day_of_week='sat', hour=15)
    scheduler.add_job(job, 'cron', day_of_week='sat', hour=16)
    scheduler.add_job(job, 'cron', day_of_week='sat', hour=17)
    scheduler.add_job(job, 'cron', day_of_week='sat', hour=18)

    # Sunday
    scheduler.add_job(job, 'cron', day_of_week='sun', hour=12)
    scheduler.add_job(job, 'cron', day_of_week='sun', hour=13)
    scheduler.add_job(job, 'cron', day_of_week='sun', hour=14)
    scheduler.add_job(job, 'cron', day_of_week='sun', hour=15)
    scheduler.add_job(job, 'cron', day_of_week='sun', hour=21, minute=23)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
