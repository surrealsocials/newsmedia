# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from .utils import update  # Import your task function

scheduler = BackgroundScheduler()

# Schedule your task to run every hour
scheduler.add_job(
    update,
    trigger=IntervalTrigger(minutes=1),
    id='update',
    name='update database every hour',
    replace_existing=True,
)
print('\n############## UPDATED DB ######################\n')
scheduler.start()
