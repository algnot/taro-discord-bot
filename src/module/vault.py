from .base import Base
from .users import User
import uuid


class Vault(Base):
    name: str = ""

    def __init__(self, name=""):
        self.name = name
        super().__init__()

    def create_or_update_value_vault(self, name: str, init_value: int, relate_table: str, relate_column: str):
        self.name = name
        self.logger.info(f"Trying to create or update vault {name}..")
        self.execute(f"""
            INSERT INTO vault (name, init_value, relate_table, relate_column)
            VALUES (:name, :init_value, :relate_table, :relate_column)
            ON CONFLICT (name) DO UPDATE SET
                name = EXCLUDED.name,
                init_value = EXCLUDED.init_value,
                relate_table = EXCLUDED.relate_table,
                relate_column = EXCLUDED.relate_column,
                remaining_value = EXCLUDED.init_value - (SELECT SUM({relate_column}) FROM public.{relate_table})
        """, {
            "name": name,
            "init_value": init_value,
            "relate_table": relate_table,
            "relate_column": relate_column
        })
        self.logger.info(f"Create or update vault {name} done")

    def create_transaction(self, token_name: str, from_id: int, to_id: int, amount: int):
        transaction_id = str(uuid.uuid4())
        self.execute("""
            INSERT INTO transaction (id, token, from_id, to_id, amount, status)
            VALUES (:id, :token_name, :from_id, :to_id, :amount, :status)
        """, {
            "id": transaction_id,
            "token_name": token_name,
            "from_id": from_id,
            "to_id": to_id,
            "amount": amount,
            "status": "pending"
        })

        user = User(id=from_id)
        user_info = user.get_user_info()

        if user_info[token_name] < amount:
            self.execute("""
                UPDATE transaction
                SET status = :status
                WHERE id = :id
            """, {
                "id": transaction_id,
                "status": "failed"
            })
            self.logger.info(f"Transaction {transaction_id} failed")
            return

        self.execute(f"""
            UPDATE users
            SET {token_name} = {token_name} - :amount
            WHERE id = :from_id;
            UPDATE users
            SET {token_name} = {token_name} + :amount
            WHERE id = :to_id;
            UPDATE transaction
            SET status = :status
            WHERE id = :transaction_id;
        """, {
            "amount": amount,
            "from_id": from_id,
            "to_id": to_id,
            "status": "completed",
            "transaction_id": transaction_id
        })

        return transaction_id
