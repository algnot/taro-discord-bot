from .base import Base


class Seed(Base):
    name: str = ""

    def __init__(self, name: str = ""):
        self.name = name
        super().__init__()

    def create_or_update_seed_by_name(self, name: str, emoji: str, harvest_time_interval: int, drop_item_name: str,
                                      drop_item_quantity: int = 1, max_harvest_count: int = 1):
        self.name = name
        self.logger.info(f"Trying to create or update seed name {name}..")
        self.execute("""
            INSERT INTO seed (name, emoji, harvest_time_interval, drop_item_name, drop_item_quantity, max_harvest_count)
            VALUES (:name, :emoji, :harvest_time_interval, :drop_item_name, :drop_item_quantity, :max_harvest_count)
            ON CONFLICT (name) DO UPDATE SET
                emoji = EXCLUDED.emoji,
                harvest_time_interval = EXCLUDED.harvest_time_interval,
                drop_item_name = EXCLUDED.drop_item_name,
                drop_item_quantity = EXCLUDED.drop_item_quantity,
                max_harvest_count = EXCLUDED.max_harvest_count
        """, {
            "name": name,
            "emoji": emoji,
            "harvest_time_interval": harvest_time_interval,
            "drop_item_name": drop_item_name,
            "drop_item_quantity": drop_item_quantity,
            "max_harvest_count": max_harvest_count
        })
        self.logger.info(f"Create or update seed name {name} done")
