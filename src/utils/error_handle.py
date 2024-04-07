from .logger import Logger
from .config import Config
import traceback

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