import discord
from ..utils.config import Config
from requests import get
from enum import Enum
from ..jobs.static import JOBS


def handle(bot: discord.Client, tree: discord.app_commands.CommandTree):
    name = "job"
    description = "Run job in taro runner server (Admin Only)"

    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    job_list = JOBS

    if len(job_list) == 1:
        job_list["none"] = "none"

    jobs = Enum("Jobs", job_list)

    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    @discord.app_commands.describe(job="Job ที่ต้องการ run")
    async def call(interaction: discord.Interaction, job: jobs):
        await interaction.response.defer()

        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")

        user = interaction.user
        admin_list = str(config.get("TARO_DISCORD_ADMIN", "")).split(",")
        is_admin = str(user.id) in admin_list

        if not is_admin:
            await interaction.followup.send(f"❌ Can not use this command")
            return

        runner_endpoint = config.get("TARO_RUNNER_ENDPOINT", "taro-discord-runner:3000")
        result = get(f"{runner_endpoint}/job/{job.name}")

        await interaction.followup.send(f"Run job `{job.name}` success with response `{result.text}`")
