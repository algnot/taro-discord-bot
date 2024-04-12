import discord
from ..utils.config import Config
from ..module.users import User


def handle(bot: discord.Client, tree: discord.app_commands.CommandTree):
    name = "me"
    description = "ดูข้อมูลของฉัน"

    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))

    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer()

        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")

        interaction_user = interaction.user

        user = User(id=interaction_user.id)
        user_info = user.get_user_info()

        embed = discord.Embed(type="article", color=0xff8c00)
        embed.set_author(name=f"ข้อมูลของ {user_info.get('username', interaction_user.name)}\n",
                         icon_url=user_info.get("display_avatar", interaction_user.display_avatar.url))
        embed.set_image(url=user_info.get("display_avatar", interaction_user.display_avatar.url))

        embed.add_field(name="🗒️  ข้อมูลทั่วไป\n",
                        value=f"_\n\nชื่อเล่น: `{user_info.get('display_name', interaction_user.display_name)}`\n" +
                              f"สร้างบัญชีเมื่อ: `{user_info.get('created_at', interaction_user.created_at).strftime('%d/%m/%Y')}`\n" +
                              f"เข้า server เมื่อ: `{user_info.get('joined_at', interaction_user.joined_at).strftime('%d/%m/%Y')}`\n",
                        inline=True)
        embed.add_field(name="👾  ไอเท็ม\n",
                        value=f"_\n\n🪙 `{user_info.get('taro_coin', 0):,}` taro coin\n" +
                              f"🌲 `{len(user_info.get('user_farm', []))}` total farm\n",
                        inline=True)

        await interaction.followup.send(embed=embed)
