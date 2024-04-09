from .config import Config
from requests import get


def get_image_from_text(text):
    config = Config()
    base_url = config.get("SERPAPT_BASE_URL")
    api_key = config.get("SERPAPT_API_SECRET")
    response = get(f"{base_url}/search?q={text}&tbm=isch&ijn=0&api_key={api_key}")
    return response.json()
