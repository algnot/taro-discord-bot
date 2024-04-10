from .base import Base


class Vault(Base):

    def __init__(self):
        super().__init__()

    def create_or_update_value_vault(self, name: str, init_value: int, relate_table: str, relate_column: str):
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
