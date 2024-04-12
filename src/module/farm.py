from .base import Base


class Farm(Base):

    def __init__(self):
        super().__init__()

    def create_farm_of_user(self, user_id: int):
        self.logger.info(f"Trying to create farm of user {user_id}..")
        self.execute("""
            INSERT INTO farm (user_id)
            VALUES (:user_id)
        """, {
            "user_id": user_id
        })
        self.logger.info(f"Create farm of user {user_id} done")
