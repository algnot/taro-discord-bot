import discord
from ..module.users import User
from ..module.item import Item
import asyncio


class ShopMenuEmbed(discord.Embed):
    def __init__(self, interaction:discord.Interaction):
        interaction_user = interaction.user

        user = User(id=interaction_user.id)
        user_info = user.get_user_info()

        super().__init__(type="article", color=5763719)

        self.set_author(name=f"ฟาร์มของ {user_info.get('username', interaction_user.name)}\n",
                        icon_url=user_info.get("display_avatar", interaction_user.display_avatar.url))

        item = Item()
        all_item_can_buy = item.get_all_item_can_buy()
        message_item = ""

        for item_can_buy in all_item_can_buy:
            emoji = item_can_buy.get("emoji", "")
            name = " ".join(item_can_buy.get("name", "").split("_"))
            token = " ".join(item_can_buy.get("buy_token", "").split("_"))
            price = item_can_buy.get("buy_amount", "")
            type = item_can_buy.get("type", "ชิ้น")
            message_item += f"{emoji} `{name}` ราคา `{price}` {token}/{type}"

        self.add_field(name="👾  ไอเท็มของฉัน\n",
                        value=f"_\n\n🪙 `{user_info.get('taro_coin', 0):,}` taro coin\n" +
                              f"🌲 `{len(user_info.get('user_farm', []))}` total farm\n\n.",
                        inline=False)

        self.add_field(name="\n☘️ ไอเท็มในร้าน\n",
                       value=f"_\n\n{message_item}",
                       inline=False)

        view = ShopMenuView(message_id=interaction.message.id, user_id=interaction_user.id, all_item=all_item_can_buy)
        asyncio.run_coroutine_threadsafe(self.edit_view(view, interaction), interaction.client.loop)

    async def edit_view(self, view, interaction):
        await interaction.message.edit(view=view)


class ShopMenuView(discord.ui.View):
    def __init__(self, message_id: int, user_id: int, all_item: list):
        super().__init__(timeout=None)

        for item in all_item:
            emoji = item.get("emoji", " ")
            name = " ".join(item.get("name", "").split("_"))
            self.add_item(discord.ui.Button(label=f"{emoji} {name}",
                                            style=discord.ButtonStyle.blurple,
                                            custom_id=f"buy-{message_id}-{user_id}-{item.get('name', '')}",
                                            row=0))

        self.add_item(discord.ui.Button(label="Menu",
                                        style=discord.ButtonStyle.gray,
                                        custom_id=f"home-{message_id}-{user_id}",
                                        row=0))
