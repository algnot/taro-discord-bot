from .base import Base


class Inventory(Base):
    user_id: int = 0

    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__()

    def add_item_to_inventory(self, item_name: str, quantity: int):
        self.logger.info(f"Trying to create or update inventory {self.user_id}:{item_name}..")

        self.execute("""
            INSERT INTO inventory (user_id, item_name, quantity)
            VALUES (:user_id, :item_name, :quantity)
            ON CONFLICT (user_id, item_name) DO UPDATE SET
                quantity = inventory.quantity + EXCLUDED.quantity
        """, {
            "user_id": self.user_id,
            "item_name": item_name,
            "quantity": quantity
        })

        self.logger.info(f"Create or update inventory {self.user_id}:{item_name} done")
