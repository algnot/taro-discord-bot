from .logger import Logger
from .config import Config

logger = Logger()
config = Config()

service_name = config.get("SERVICE_NAME", "taro-discord-bot")


async def handle_command_error(interection, error):
    if service_name != "taro-discord-bot":
        return
    await interection.followup.send("❌ ไม่สามารถใช้คำสั่งได้ โปรดลองใหม่อีกครั้ง", ephemeral=True)
    logger.error(f"[Discord Command] Can not use command with `{error}`")


async def handle_on_bot_error(event, *args, **kwargs):
    if service_name != "taro-discord-bot":
        return
    logger.error(f"[Discord Bot] {event} with error")


def handle_job_error(func):
    def runner(*args, **kwargs):
        try:
            logger.warning(f"Starting job `{func.__name__}`")
            return_value = func(*args, **kwargs)
            if config.get("ENV", "dev") == "production":
                logger.warning(f"Run job: `{func.__name__}` successfully")
            else:
                logger.info(f"Run job: `{func.__name__}` successfully")
            return return_value
        except Exception as e:
            logger.error(f"Error when running task: `{func.__name__}` with error {e}`")
            raise e
    runner.__name__ = func.__name__
    return runner
