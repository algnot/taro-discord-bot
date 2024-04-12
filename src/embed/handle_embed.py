import discord
from .shop_menu import ShopMenuEmbed
from .farm_menu import FarmMenuEmbed


async def handle_interaction(interaction: discord.Interaction, action: str):
    if action == "shop":
        embed = ShopMenuEmbed(interaction=interaction)

        await interaction.message.edit(embed=embed, content="")

    elif action == "home":
        embed = FarmMenuEmbed(interaction=interaction)

        await interaction.message.edit(embed=embed, content="")

    return
