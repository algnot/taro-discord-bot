import discord
import threading
import os
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.error_handle import handle_command_error, handle_on_bot_error
from src.messages.message_handle import handle_message
from src.controllers.init_controller import init_controller

config = Config()
logger = Logger()
service_name = config.get("SERVICE_NAME", "taro-discord-bot")
        
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)

tree.on_error = handle_command_error
bot.on_error = handle_on_bot_error

bot_ready_event = threading.Event()

if service_name == "taro-discord-bot":
    for file in os.listdir("./src/commands"):
        if file.endswith(".py") and file != "__init__.py":
            file_name = file.split(".")[0]
            handle = getattr(__import__(f"src.commands.{file_name}", fromlist=["handle"]), "handle")
            handle(bot, tree)


    @bot.event
    async def on_message(message):
        await handle_message(message)


@bot.event
async def on_ready():
    bot_ready_event.set()

    if service_name == "taro-discord-bot":
        guilds = bot.guilds
        env = config.get('ENV')
        if env == "production":
            logger.warning(f"[Discord] Bot is ready on `{config.get('ENV')}` environment!")
        else:
            logger.info(f"[Discord] Bot is ready on `{config.get('ENV')}` environment!")
        for guild in guilds:
            await tree.sync(guild=discord.Object(id=guild.id))


def run_discord_bot():
    bot.run(config.get("TARO_DISCORD_TOKEN"))


if __name__ == "__main__":
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.start()
    if service_name == "taro-discord-bot":
        discord_thread.join()
    elif service_name == "taro-discord-controller":
        bot_ready_event.wait()
        init_controller(bot)
