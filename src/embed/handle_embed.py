import discord
from .shop_menu import ShopMenuEmbed, ShopMenuView, ShopModal
from .farm_menu import FarmMenuEmbed, FarmMenuView, FarmManagerEmbed, FarmManagerView


async def handle_interaction(interaction: discord.Interaction, action: str):
    if action == "shop":
        embed = ShopMenuEmbed(interaction=interaction)
        view = ShopMenuView(message_id=interaction.message.id, all_item=embed.all_item, user_id=interaction.user.id)

        await interaction.message.edit(embed=embed, view=view, content="")

    elif action == "home":
        embed = FarmMenuEmbed(interaction=interaction)
        view = FarmMenuView(message_id=interaction.message.id, user_id=interaction.user.id)

        await interaction.message.edit(embed=embed, view=view, content="")

    elif action == "buy":
        await interaction.response.send_modal(
            ShopModal(interaction=interaction, message_id=interaction.message.id)
        )

    elif action == "farm":
        embed = FarmManagerEmbed(interaction=interaction)
        view = FarmManagerView(message_id=interaction.message.id, user_id=interaction.user.id,
                               index=embed.farm_index, all_farm=embed.all_farm)

        await interaction.message.edit(embed=embed, view=view, content="")
