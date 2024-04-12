from .base import Base


class Item(Base):
    name: str = ""

    def __init__(self, name: str = ""):
        self.name = name
        super().__init__()

    def create_or_update_item_by_name(self, name: str, type: str, emoji: str, sell_token: str, sell_amount: int,
                                      buy_token: str, buy_amount: int, can_sell: bool = False, can_buy: bool = False):
        self.name = name
        self.logger.info(f"Trying to create or update item name {name}..")
        self.execute("""
            INSERT INTO item (name, type, emoji, sell_token, sell_amount, buy_token, buy_amount, can_sell, can_buy)
            VALUES (:name, :type, :emoji, :sell_token, :sell_amount, :buy_token, :buy_amount, :can_sell, :can_buy)
            ON CONFLICT (name) DO UPDATE SET
                type = EXCLUDED.type,
                emoji = EXCLUDED.emoji,
                sell_token = EXCLUDED.sell_token,
                sell_amount = EXCLUDED.sell_amount,
                buy_token = EXCLUDED.buy_token,
                buy_amount = EXCLUDED.buy_amount,
                can_sell = EXCLUDED.can_sell,
                can_buy = EXCLUDED.can_buy
        """, {
            "name": name,
            "type": type,
            "emoji": emoji,
            "sell_token": sell_token,
            "sell_amount": sell_amount,
            "buy_token": buy_token,
            "buy_amount": buy_amount,
            "can_sell": can_sell,
            "can_buy": can_buy
        })
        self.logger.info(f"Create or update item name {name} done")

    def get_all_item_can_buy(self):
        result = self.execute("""
            SELECT * FROM item WHERE can_buy
        """)

        return result

    def get_item_info_by_item_name(self, name: str):
        result = self.execute("""
            SELECT * FROM item WHERE name = :name
        """, {
            "name": name
        })

        if len(result) > 0:
            return result[0]

        return {}
