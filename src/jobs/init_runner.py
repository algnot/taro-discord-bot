import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from .spotify_job import init_spotify_job
from ..utils.config import Config


def init_runner(bot: discord.Client):
    config = Config()
    app = Flask(__name__)

    scheduler = BackgroundScheduler()
    scheduler.start()

    init_spotify_job(scheduler=scheduler, bot=bot, app=app)

    @app.route('/', methods=['GET'])
    def index():
        return {
            "jobs": {
                "random_spotify_song_and_send_to_channel": "สุ่มเพลงใน Spotify"
            }
        }

    app.run(host="0.0.0.0", port=config.get("HTTP_PORT", "3000"))
