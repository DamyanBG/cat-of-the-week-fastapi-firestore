from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from cron_tasks.won_job import win_job


def create_scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(id="win_job_01", func=win_job, trigger="interval", seconds=10)
    return scheduler
