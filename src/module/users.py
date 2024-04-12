from .base import Base
from .farm import Farm


class User(Base):
    id: int = ""

    def __init__(self, id: int = None):
        self.id = id
        super().__init__()

    def get_user_info(self):
        user_data = self.execute("""
            SELECT * FROM public.users WHERE id = :id
        """, {
            "id": self.id
        })

        user_farm = self.execute("""
            SELECT * FROM public.farm WHERE user_id = :id
        """, {
            "id": self.id
        })

        user_inventory = self.execute("""
            SELECT * FROM public.inventory WHERE user_id = :id
        """, {
            "id": self.id
        })

        if len(user_data) > 0:
            user_data[0]["user_farm"] = user_farm
            user_data[0]["user_inventory"] = user_inventory
            return user_data[0]

        return {}

    def create_or_update_by_id(self, id: int, username: str, display_name: str, display_avatar: str,
                               is_bot: bool, created_at: str, joined_at: str):
        self.id = id
        self.logger.info(f"Trying to create or update user id {id}..")
        self.execute("""
            INSERT INTO users (id, username, display_avatar, display_name, is_bot, created_at, joined_at)
            VALUES (:id, :username, :display_avatar, :display_name, :is_bot, :created_at, :joined_at)
            ON CONFLICT (id) DO UPDATE SET
                username = EXCLUDED.username,
                display_avatar = EXCLUDED.display_avatar,
                display_name = EXCLUDED.display_name
        """, {
            "id": id,
            "username": username,
            "display_avatar": display_avatar,
            "display_name": display_name,
            "is_bot": is_bot,
            "created_at": created_at,
            "joined_at": joined_at
        })

        user = self.get_user_info()

        if len(user.get("user_farm", [])) == 0:
            farm = Farm()
            farm.create_farm_of_user(user_id=id)

        self.logger.info(f"Create or update user id {id} done")
