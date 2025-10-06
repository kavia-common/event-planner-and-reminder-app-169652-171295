from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)
_scheduler: Optional[BackgroundScheduler] = None


# PUBLIC_INTERFACE
def start_scheduler() -> BackgroundScheduler:
    """Start an in-process APScheduler for periodic notification tasks."""
    global _scheduler
    if _scheduler and _scheduler.running:
        return _scheduler

    scheduler = BackgroundScheduler(timezone="UTC")
    # Example heartbeat job; replace with real reminder dispatchers
    scheduler.add_job(_heartbeat_job, IntervalTrigger(minutes=5), id="heartbeat", replace_existing=True)
    scheduler.start()
    _scheduler = scheduler
    logger.info("BackgroundScheduler started with jobs: %s", [job.id for job in scheduler.get_jobs()])
    return scheduler


def _heartbeat_job():
    logger.debug("Notifications scheduler heartbeat at %s", datetime.utcnow().isoformat())
