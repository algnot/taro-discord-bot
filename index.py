import discord
import threading
import os
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.error_handle import handle_command_error, handle_on_bot_error

config = Config()
logger = Logger()
        
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)

tree.on_error = handle_command_error
bot.on_error = handle_on_bot_error

for file in os.listdir("./src/commands"):
    if file.endswith(".py") and file != "__init__.py":
        file_name = file.split(".")[0]
        handle = getattr(__import__(f"src.commands.{file_name}", fromlist=["handle"]), "handle")
        handle(bot, tree)

@bot.event
async def on_ready():
    guilds = bot.guilds
    logger.warning(f"[Discord] Bot is ready on `{config.get('ENV')}` environment!")
    for guild in guilds:
        await tree.sync(guild=discord.Object(id=guild.id))
        
def run_discord_bot():
    bot.run(config.get("TARO_DISCORD_TOKEN"))

if __name__ == "__main__":
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.start()
    discord_thread.join()
