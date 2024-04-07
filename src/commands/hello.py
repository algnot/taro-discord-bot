import discord
from ..utils.config import Config


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "ping"
    description = "ping to server"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        await interaction.followup.send(f"pong in `{config.get('ENV')}` environment!")
        