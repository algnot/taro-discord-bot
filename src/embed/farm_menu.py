import discord
from ..module.users import User
from ..module.item import Item


class FarmMenuEmbed(discord.Embed):
    def __init__(self, interaction):
        interaction_user = interaction.user

        user = User(id=interaction_user.id)
        user_info = user.get_user_info()

        super().__init__(type="article", color=5763719)

        self.set_author(name=f"ฟาร์มของ {user_info.get('username', interaction_user.name)}\n",
                        icon_url=user_info.get("display_avatar", interaction_user.display_avatar.url))

        inventory_message = ""
        for item in user_info.get("user_inventory", []):
            quantity = item.get("quantity", 0)

            if quantity > 0:
                item_model = Item()
                item_info = item_model.get_item_info_by_item_name(name=item.get("item_name", ""))
                emoji = item_info.get("emoji", "-")
                item_name = " ".join(item.get("item_name", "").split("_"))
                inventory_message += f"{emoji} `{quantity}` {item_name}\n"

        self.add_field(name="🗒️  ไอเท็ม\n",
                       value=f"_\n\n🪙 `{user_info.get('taro_coin', 0):,}` taro coin\n" +
                             f"🌲 `{len(user_info.get('user_farm', []))}` total farm\n",
                       inline=True)

        self.add_field(name="📦 Farm Inventory\n",
                       value=f"_\n\n{inventory_message}",
                       inline=True)


class FarmMenuView(discord.ui.View):
    def __init__(self, message_id: int, user_id: int):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(label="Farm",
                                        style=discord.ButtonStyle.blurple,
                                        custom_id=f"farm-{message_id}-{user_id}-0",
                                        row=0))

        self.add_item(discord.ui.Button(label="Shop",
                                        style=discord.ButtonStyle.blurple,
                                        custom_id=f"shop-{message_id}-{user_id}",
                                        row=0))


class FarmManagerEmbed(discord.Embed):
    farm_index: int = 0
    user_farm: list = []
    farm_info: dict = {}

    def __init__(self, interaction):
        interaction_user = interaction.user

        user = User(id=interaction_user.id)
        user_info = user.get_user_info()

        self.farm_index = int(interaction.data["custom_id"].split("-")[3])
        self.all_farm = user_info.get("user_farm", [])

        super().__init__(type="article", color=5763719)

        self.farm_info = self.all_farm[self.farm_index]

        self.set_author(name=f"ฟาร์มของ {user_info.get('username', interaction_user.name)}\n",
                        icon_url=user_info.get("display_avatar", interaction_user.display_avatar.url))

        information_message = ""

        self.add_field(name=f"\n🌄 ข้อมูลฟาร์ม หมายเลข `{self.farm_index + 1}`\n",
                       value=f"_\n\n☘️ เลเวล: `{self.farm_info.get('level', 1)}`\n" +
                             f"🌾 เมล็ด: `{' '.join(str(self.farm_info.get('seed_name', '-')).split('_'))}`\n" +
                             f"🌾 จำนวนเมล็ด: `{self.farm_info.get('seed_count', 0)}/{self.farm_info.get('max_seed_count', 0)}`\n" +
                             f"⌛ เก็บเกี่ยวครั้งต่อไป: `{self.farm_info.get('harvest_time', '-')}`\n" +
                             f"✨ เก็บเกี่ยวได้อีก: `{self.farm_info.get('harvest_count', 0)}` ครั้ง\n"
                             f"========================================\n{information_message}",
                       inline=False)


class FarmManagerView(discord.ui.View):
    def __init__(self, message_id: int, user_id: int, all_farm: list, index: int = 0):
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(label="◀️",
                                        style=discord.ButtonStyle.blurple,
                                        custom_id=f"farm-{message_id}-{user_id}-{index - 1}",
                                        disabled=index == 0,
                                        row=0))

        self.add_item(discord.ui.Button(label="▶️",
                                        style=discord.ButtonStyle.blurple,
                                        custom_id=f"farm-{message_id}-{user_id}-{index + 1}",
                                        disabled=index > len(all_farm),
                                        row=0))

        self.add_item(discord.ui.Button(label="Menu",
                                        style=discord.ButtonStyle.gray,
                                        custom_id=f"home-{message_id}-{user_id}",
                                        row=0))
