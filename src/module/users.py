from .base import Base
from .farm import Farm
from .item import Item


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

    def buy_item(self, item_name: str, quantity: int):
        item = Item()
        item_info = item.get_item_info_by_item_name(name=item_name)

        token = item_info.get("buy_token", "taro_coin")
        total_price = item_info.get("buy_amount", 0) * quantity

        user_token = self.execute(f"""
            SELECT {token} FROM users WHERE id = :user_id
        """, {
            "user_id": self.id
        })

        if len(user_token) == 0:
            raise UserWarning("❌ พบข้อผิดพลาดบางอย่างกรูณาลองอีกครั้ง")

        if user_token[0].get(token) < total_price:
            raise UserWarning(f"❌ จำนวน `{' '.join(token.split('_'))}` ไม่พอสำหรับการสั่งซื้อ "
                              f"(ต้องการ `{total_price:,}` มีอยู่ `{user_token[0].get(token):,}`)")

        from .vault import Vault
        from .inventory import Inventory
        taro_discord_id = int(self.config.get("TARO_DISCORD_USER_ID", 1154093547931312289))
        vault = Vault()
        inventory = Inventory(user_id=self.id)
        transaction_id = vault.create_transaction(from_id=self.id, to_id=taro_discord_id, token_name=token, amount=total_price)
        inventory.add_item_to_inventory(item_name=item_info.get("name", "Unknown"), quantity=quantity)

        return transaction_id, item_info.get("emoji", "☘️")
