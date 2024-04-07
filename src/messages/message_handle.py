import discord
from ..utils.config import Config
from .ping_message import on_ping_message


async def handle_message(message: discord.Message):
    config = Config()
    if message.author.bot:
        return
    
    user = message.author
    
    admin_list = str(config.get("TARO_DISCORD_ADMIN", "")).split(",")
    is_admin = str(user.id) in admin_list
    
    content = message.content.lower()
    content_splited = message.content.split(" ")
    
    if is_admin:
        await message.add_reaction("🐶")
        
    if content == "ping":
        await on_ping_message(message, is_admin)
