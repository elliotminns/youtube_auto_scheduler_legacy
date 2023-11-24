# This script schedules the 'Upload.py' script to start at specified times.

from apscheduler.schedulers.blocking import BlockingScheduler
from upload import upload_short
from authenticate import credential_check

def job():
    youtube_object = credential_check()
    upload_short(youtube_object)

# Create a scheduler
scheduler = BlockingScheduler()

# Monday
scheduler.add_job(job, 'cron', day_of_week='mon', hour=18)
scheduler.add_job(job, 'cron', day_of_week='mon', hour=19)
scheduler.add_job(job, 'cron', day_of_week='mon', hour=20)
scheduler.add_job(job, 'cron', day_of_week='mon', hour=21)

# Tueday
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


# Start the scheduler
scheduler.start()