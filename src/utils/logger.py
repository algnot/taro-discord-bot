from requests import post
from .config import Config
import datetime
import traceback


class Logger:
    
    def info(self, message):
        config = Config()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[info] topic=\"[{config.get('ENV')}] Info Message\" message=\"{message}\" date=\"{now}\"")
    
    def warning(self, message):    
        self.send_message_to_webhook("Warning Message", message, "warning")
        
    def error(self, message):
        message = f"{message}\n```{traceback.format_exc()}```"
        self.send_message_to_webhook("Error Message", message, "error")

    def get_webhook(self, level):
        config = Config()
        webhook_mapped = {
            "warning": config.get("DISCORD_USICK_ALERT_WEBHOOK_URL"),
            "info": config.get("DISCORD_USICK_ALERT_WEBHOOK_URL"),
            "error": config.get("DISCORD_USICK_ALERT_WEBHOOK_URL"),
        }

        try:
            return webhook_mapped[level]
        except Exception:
            return Exception(f"Webhook not found for level {level}")

    def send_message_to_webhook(self, topic, message, level):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        config = Config()
        
        try:
            post(url=self.get_webhook(level), json={
                "embeds": [
                    {
                        "title": f"[{config.get('ENV')}] {topic}",
                        "description": message,
                        "color": self.get_color(level),
                    },
                ],
            })
            print(f"[{level}] topic=\"{topic}\" message=\"{message}\" date=\"{now}\"")
        except Exception:
            print(f"[{level}] topic=\"{topic}\" message=\"{message}\" date=\"{now}\"")

    def get_color(self, level):
        color_mapped = {
            "warning": 15105570,
            "info": 3447003,
            "error": 15158332
        }

        try:
            return color_mapped[level]
        except Exception:
            return Exception(f"Color not found for level {level}")
