from .logger import Logger
from .config import Config
import traceback

logger = Logger()
config = Config()

async def handle_command_error(interection, error):
    await interection.followup.send("❌ ไม่สามารถใช้คำสั่งได้ โปรดลองใหม่อีกครั้ง", ephemeral=True)
    logger.error(f"[Discord Command] Can not use command with `{error}`")

async def handle_on_bot_error(event):
    logger.error(f"[Discord Bot] {event} with error")