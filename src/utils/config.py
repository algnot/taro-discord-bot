from dotenv import load_dotenv
from requests import get
import os


class Config:

    def __init__(self):
        self.unleash_endpoint = os.environ["UNLEASH_ENDPOINT"]
        self.unleash_api_key = os.environ["UNLEASH_API_KEY"]
        load_dotenv()

    def get(self, name: str, default_value=""):
        try:
            url = f"{self.unleash_endpoint}/api/admin/projects/default/features/{name}/environments/development/variants"
            api_key = self.unleash_api_key

            res = get(url=url, headers={
                "Authorization": api_key,
                "Content-Type": "application/json"
            })

            if res.status_code != 200:
                if name in os.environ:
                    return os.environ[name]
                return default_value

            return res.json().get("variants", [{}])[0].get("payload", {}).get("value", "")

        except Exception:
            try:
                if name in os.environ:
                    return os.environ[name]
                return default_value
            except Exception:
                return default_value
