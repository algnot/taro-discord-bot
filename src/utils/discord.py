import discord
import asyncio
from .logger import Logger

logger = Logger()


async def send_message_to_channel(channel, message, image=""):
    await channel.send(content=message)

    if image:
        await channel.send(content=image)


async def add_role_to_user(member: discord.Member, role_id: int):
    role = member.guild.get_role(role_id)
    await member.add_roles(role)
    logger.warning(f"Add role `{role.name}` to <@{member.id}>")


def send_message_to_channel_by_guild_and_channel_id(bot: discord.Client, guild_id, channel_id, message, image=""):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    asyncio.run_coroutine_threadsafe(send_message_to_channel(channel, message, image), bot.loop)
