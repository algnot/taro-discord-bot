import discord
import asyncio


async def send_message_to_channel(channel, message):
    await channel.send(message)


def send_message_to_channel_by_guild_and_channel_id(bot: discord.Client, guild_id, channel_id, message):
    guild = bot.get_guild(guild_id)
    channel = guild.get_channel(channel_id)

    asyncio.run_coroutine_threadsafe(send_message_to_channel(channel, message), bot.loop)
