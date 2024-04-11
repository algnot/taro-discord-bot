from .base import Base


class User(Base):
    id: int = ""

    def __init__(self, id: int = None):
        self.id = id
        super().__init__()

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
        self.logger.info(f"Create or update user id {id} done")
