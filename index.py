import discord
import threading
import os
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.error_handle import handle_command_error, handle_on_bot_error
from src.utils.discord import send_message_to_channel_by_guild_and_channel_id, add_role_to_user
from src.messages.message_handle import handle_message
from src.controllers.init_controller import init_controller
from src.jobs.init_runner import init_runner
from src.module.users import User

config = Config()
logger = Logger()
service_name = config.get("SERVICE_NAME", "taro-discord-bot")
        
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)

bot_ready_event = threading.Event()

tree.on_error = handle_command_error
bot.on_error = handle_on_bot_error

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
    async def on_member_join(member: discord.Member):
        discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
        discord_channel_id = int(config.get("DISCORD_CHANNEL_WELCOME"))
        discord_role_user = int(config.get("DISCORD_ROLE_USER"))
        user = User()
        user.create_or_update_by_id(id=member.id, username=member.name, display_name=member.display_name,
                                    display_avatar=member.display_avatar.url, is_bot=member.bot,
                                    created_at=member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                    joined_at=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        send_message_to_channel_by_guild_and_channel_id(bot=bot, guild_id=discord_guild_id, channel_id=discord_channel_id,
                                                        message=f"Welcome <@{member.id}> to `u sick achoo` server!  🥳 🎉",
                                                        image=member.display_avatar.url)
        await add_role_to_user(member=member, role_id=discord_role_user)

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
    elif service_name == "taro-discord-runner":
        bot_ready_event.wait()
        init_runner(bot)
