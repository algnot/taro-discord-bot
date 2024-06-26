import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from .spotify_job import init_spotify_job
from .random_food_job import init_random_food_job
from ..utils.config import Config
from .migrate_database_job import init_migrate_database_job
from .static import JOBS


def init_runner(bot: discord.Client):
    config = Config()
    app = Flask(__name__)

    scheduler = BackgroundScheduler()
    scheduler.start()

    init_spotify_job(scheduler=scheduler, bot=bot, app=app)
    init_random_food_job(scheduler=scheduler, bot=bot, app=app)
    init_migrate_database_job(scheduler=scheduler, bot=bot, app=app)

    @app.route('/', methods=['GET'])
    def index():
        return "Taro Runner is running :)"

    @app.route('/jobs', methods=['GET'])
    def get_all_jobs():
        return {
            "jobs": JOBS
        }

    app.run(host="0.0.0.0", port=config.get("HTTP_PORT", "3000"))
