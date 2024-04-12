import discord
from ..utils.config import Config
from ..embed.farm_menu import FarmMenuEmbed, FarmMenuView
from ..embed.handle_embed import handle_interaction


def handle(bot: discord.Client, tree: discord.app_commands.CommandTree):
    name = "play"
    description = "Play the taro farm"

    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))

    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer()

        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")

        message = await interaction.followup.send("⌛ Game UI is creating...")

        embed = FarmMenuEmbed(interaction=interaction, message_id=message.id)
        view = FarmMenuView(message_id=message.id, user_id=interaction.user.id)

        await message.edit(embed=embed, view=view, content="")

    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            await interaction.response.defer()
            custom_id = interaction.data["custom_id"]
            action, message_id, user_id = custom_id.split("-")

            if int(user_id) != interaction.user.id:
                await interaction.followup.send("❌ นี่ไม่ใช่ฟาร์มของคุณ พิมพ์ `/play` เพื่อดูฟาร์มของคุณ", ephemeral=True)

            await interaction.message.edit(content="⌛ Game UI is loading..")
            await handle_interaction(interaction=interaction, action=action)
