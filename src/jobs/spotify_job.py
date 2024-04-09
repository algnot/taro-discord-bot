import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.job import jobs
from ..utils.config import Config
from ..utils.discord import send_message_to_channel_by_guild_and_channel_id
from ..utils.spotify import Spotify
from ..utils.error_handle import handle_job_error
from random import randint


def init_spotify_job(scheduler: BackgroundScheduler, bot: discord.Client, app: Flask = None):
    config = Config()

    @jobs(scheduler=scheduler, cron="0 10,15 * * *", controller=app)
    @handle_job_error
    def random_spotify_song_and_send_to_channel():
        spotify = Spotify()
        discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
        discord_channel_id = int(config.get("DISCORD_CHANNEL_PLAY_WITH_TARO"))

        total_song = spotify.get_count_song_in_playlist()
        random_index = randint(0, total_song - 1)
        song = spotify.get_song_in_playlist_by_index(random_index)

        send_message_to_channel_by_guild_and_channel_id(bot,
                                                        discord_guild_id,
                                                        discord_channel_id,
                                                        song["external_urls"]["spotify"])
        return True
