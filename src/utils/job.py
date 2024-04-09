from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.logger import Logger
from flask import Flask

logger = Logger()


def jobs(scheduler: BackgroundScheduler = None, cron="* * * * *", controller: Flask = None, *args, **kwargs):
    minute, hour, day, month, year = cron.split()

    def decorator(func):
        if scheduler:
            logger.info(f"initial job '{func.__name__}' with '{cron}'")
            scheduler.add_job(func, "cron", minute=minute, hour=hour, day=day,
                              month=month, year=year, *args, **kwargs)

        if controller:
            logger.info(f"initial route job '/job/{func.__name__}'")
            route_function_name = f"{func.__name__}_route"

            @controller.route(f"/job/{func.__name__}", methods=['GET'], endpoint=route_function_name)
            def call_runner():
                return_value = func()
                if isinstance(return_value, bool):
                    if return_value:
                        return {
                            "status": "ok"
                        }
                    return {
                        "status": "error"
                    }
                return return_value

        return func

    return decorator
