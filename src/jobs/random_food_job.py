import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.job import jobs
from ..utils.config import Config
from ..utils.csv import read_csv_content_to_array
from ..utils.common import get_image_from_text
from ..utils.discord import send_message_to_channel_by_guild_and_channel_id
from ..utils.error_handle import handle_job_error
from random import randint, choice
import datetime


def init_random_food_job(scheduler: BackgroundScheduler, bot: discord.Client, app: Flask = None):
    config = Config()

    @jobs(scheduler=scheduler, cron="0 9,12,17 * * *", controller=app)
    @handle_job_error
    def random_food_and_send_to_channel():
        all_food = read_csv_content_to_array("./src/data/food.csv")
        random_index = randint(0, len(all_food) - 1)
        now = datetime.datetime.now()
        prefix = ""

        result = all_food[random_index][0]
        result_image = get_image_from_text(result)
        result_image_url = ""

        if "images_results" in result_image and isinstance(result_image["images_results"], list):
            if len(result_image["images_results"]) > 0:
                image_url = choice(result_image["images_results"])
                if "original" in image_url:
                    result_image_url = image_url["original"]

        if 0 < now.hour < 10:
            prefix = f"🍔 เช้าแล้วอย่าลืมกินข้าวนะ!"
        elif 10 < now.hour < 15:
            prefix = f"🍔 เที่ยงแล้วอย่าลืมกินข้าวนะ!"
        else:
            prefix = f"🍔 เย็นแล้วอย่าลืมกินข้าวนะ!"

        discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
        discord_channel_id = int(config.get("DISCORD_CHANNEL_PLAY_WITH_TARO"))
        message = f"{prefix} คุณควรกินข้าวกับ **{result}**"
        send_message_to_channel_by_guild_and_channel_id(bot,
                                                        discord_guild_id,
                                                        discord_channel_id,
                                                        message,
                                                        result_image_url)
