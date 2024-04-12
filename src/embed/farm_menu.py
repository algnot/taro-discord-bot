import discord
from ..module.users import User
import asyncio


class FarmMenuEmbed(discord.Embed):
    def __init__(self, interaction):
        interaction_user = interaction.user

        user = User(id=interaction_user.id)
        user_info = user.get_user_info()

        super().__init__(type="article", color=5763719)

        self.set_author(name=f"ฟาร์มของ {user_info.get('username', interaction_user.name)}\n",
                        icon_url=user_info.get("display_avatar", interaction_user.display_avatar.url))

        self.add_field(name="👾  ไอเท็ม\n",
                       value=f"_\n\n🪙 `{user_info.get('taro_coin', 0):,}` taro coin\n" +
                             f"🌲 `{len(user_info.get('user_farm', []))}` total farm\n",
                       inline=True)

        self.add_field(name="📦 Farm Inventory\n",
                       value=f"_\n\n📦 `{len(user_info.get('user_inventory', []))}` total inventory\n",
                       inline=True)


class FarmMenuView(discord.ui.View):
    def __init__(self, message_id: int, user_id: int):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(label="Shop",
                                        style=discord.ButtonStyle.blurple,
                                        custom_id=f"shop-{message_id}-{user_id}",
                                        row=0))
