from flask import Flask
from ..utils.config import Config
from .users import init_user_controller
import discord

app = Flask(__name__)
config = Config()

def init_controller(bot:discord.Client):
    @app.route('/', methods=['GET'])
    def index():
        return "Server is running :)"
    
    init_user_controller(app, bot)
    
    app.run(host='0.0.0.0', port=config.get("HTTP_PORT", "3000"))
