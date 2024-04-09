import discord
import asyncio


async def send_message_to_channel(channel, message, image=""):
    await channel.send(content=message)

    if image:
        await channel.send(content=image)


def send_message_to_channel_by_guild_and_channel_id(bot: discord.Client, guild_id, channel_id, message, image=""):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    asyncio.run_coroutine_threadsafe(send_message_to_channel(channel, message, image), bot.loop)
