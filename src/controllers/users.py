from flask import Flask
from ..utils.config import Config
import discord

app = Flask(__name__)
config = Config()


def init_user_controller(app: Flask, bot: discord.Client):
    @app.route('/users', methods=['GET'])
    def get_all_user_data():
        discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
        results = []

        guilds = bot.guilds
        for guild in guilds:
            if guild.id != discord_guild_id:
                continue
            members = guild.members
            for member in members:
                result = {"user_id": member.id,
                          "name": member.name,
                          "display_name": member.display_name,
                          "display_avatar": str(member.display_avatar),
                          "created_at": member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                          "joined_at": member.joined_at.strftime("%Y-%m-%d %H:%M:%S"),
                          "is_bot": member.bot}
                results.append(result)

        return {
            "datas": results
        }
