from dotenv import load_dotenv
import os


class Config:

    def __init__(self):
        load_dotenv()

    def get(self, name: str, defualtVakue=""):
        try:
            if name in os.environ:
                return os.environ[name]

            return defualtVakue
        except Exception:
            return defualtVakue
