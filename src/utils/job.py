from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.logger import Logger

logger = Logger()


def jobs(scheduler: BackgroundScheduler, cron="* * * * *", *args, **kwargs):
    minute, hour, day, month, year = cron.split()

    def decorator(func):
        logger.info(f"initial job '{func.__name__}' with '{cron}'")
        scheduler.add_job(func, "cron", minute=minute, hour=hour, day=day,
                          month=month, year=year, *args, **kwargs)
        return func

    return decorator
