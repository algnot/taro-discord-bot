import discord
from ..module.users import User
from ..module.item import Item
from discord import ui


class ShopMenuEmbed(discord.Embed):
    all_item: list = []

    def __init__(self, interaction: discord.Interaction):
        interaction_user = interaction.user

        super().__init__(type="article", color=5763719)

        self.set_author(name=f"ฟาร์มของ {interaction_user.name}\n",
                        icon_url=interaction_user.display_avatar.url)

        item = Item()
        all_item_can_buy = item.get_all_item_can_buy()
        self.all_item = all_item_can_buy
        message_item = ""

        for item_can_buy in all_item_can_buy:
            emoji = item_can_buy.get("emoji", "")
            name = " ".join(item_can_buy.get("name", "").split("_"))
            token = " ".join(item_can_buy.get("buy_token", "").split("_"))
            price = item_can_buy.get("buy_amount", 0)
            type = item_can_buy.get("type", "ชิ้น")
            message_item += f"{emoji} `{name}` ราคา `{price}` {token}/{type}"

        self.add_field(name="\n☘️ ไอเท็มในร้าน\n",
                       value=f"_\n\n{message_item}",
                       inline=False)


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


class ShopModal(discord.ui.Modal):
    quantity = ui.TextInput(label="จำนวนที่ต้องการ", default="1", placeholder="1")
    item_name: str = ""
    item_id: str = ""
    message_id: int = 0

    def __init__(self, interaction: discord.Interaction, message_id: int):
        self.message_id = message_id
        self.item_id = interaction.data["custom_id"].split("-")[3]
        self.item_name = " ".join(self.item_id.split("_"))
        super().__init__(title=f"ซื้อ {self.item_name}")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()

        message = await interaction.channel.fetch_message(self.message_id)
        message_response = await interaction.followup.send(f"⌛ กำลังซื้อ `{self.item_name}` จำนวน `{self.quantity}`",
                                                            ephemeral=True)

        try:
            quantity = int(self.quantity.value)
        except Exception:
            return await message_response.edit(content="❌ กรุณาใส่จำนวนที่ต้องการซื้อเป็นตัวเลขเท่านั้น")

        try:
            user = User(id=interaction.user.id)
            transaction_id, emoji = user.buy_item(item_name=self.item_id, quantity=quantity)
            await message_response.edit(content=f"{emoji} ซื้อ `{self.item_name}` จำนวน `{quantity:,}` สำเร็จ (transaction id: `{transaction_id}`)")
        except UserWarning as error:
            return await message_response.edit(content=error)
