from flask import Flask
from ..utils.config import Config
from ..utils.discord import send_message_to_user_by_user_id
import discord

app = Flask(__name__)
config = Config()


def init_bank_controller(app: Flask, bot: discord.Client):
    class BankEmbed(discord.Embed):
        def __init__(self):
            super().__init__(type="article", color=5763719)
            tongla_user_id = int(config.get("DISCORD_TONGLA_USER_ID"))
            user = bot.get_user(tongla_user_id)

            self.set_author(name=f"HBD bank! 🥳 🎉 ✨",
                            icon_url=user.display_avatar.url)

            self.add_field(name=".\n",
                           value="Happy Birthday to my awesome friend Bank! 🎉 🎂\nWishing you a day filled with laughter, love, and all the good things life has to offer. May this year bring you endless joy, success, and unforgettable memories. You bring so much brightness and positivity into the world with your infectious energy and genuine kindness. Cheers to another fantastic year ahead! Let's celebrate and make this day one to remember. Sending lots of love and best wishes your way on your special day! 🎈 🎁 🎊")

            self.set_image(url="https://firebasestorage.googleapis.com/v0/b/my-website-backend-21e79.appspot.com/o/Wrapped%2FyCpEu5at9dV2WLTSTFXi%2FmainImage%2FkiRQc5sM3iTKhZQ5G8RO-IMG_0184.jpg?alt=media&token=e7f098e3-3a3c-4c07-a57c-f8f1d0d3850c")

    @app.route("/hbd-bank", methods=["GET"])
    def send_message_to_bank():
        bank_user_id = int(config.get("DISCORD_BANK_USER_ID"))
        tongla_user_id = int(config.get("DISCORD_TONGLA_USER_ID"))

        bank_embed = BankEmbed()

        send_message_to_user_by_user_id(bot=bot, user_id=bank_user_id,
                                        context={
                                           "embed": bank_embed
                                        })

        send_message_to_user_by_user_id(bot=bot, user_id=tongla_user_id,
                                        context={
                                            "content": "แบ้งกดแล้วว"
                                        })

        return {
            "go_to": "https://discord.com/channels/@me/1194285897475166348"
        }
