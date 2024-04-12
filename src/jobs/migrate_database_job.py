import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.job import jobs
from ..utils.config import Config
from ..utils.logger import Logger
from ..utils.error_handle import handle_job_error
from ..module.base import Base
from ..module.users import User
from ..module.vault import Vault
from ..module.item import Item
from ..module.seed import Seed
from sqlalchemy import MetaData, Table, Column, text, BIGINT, TEXT
from requests import get


def init_migrate_database_job(scheduler: BackgroundScheduler, bot: discord.Client, app: Flask = None):
    config = Config()
    logger = Logger()

    @jobs(scheduler=scheduler, cron="0 22 * * *", controller=app)
    @handle_job_error
    def migrate_users_data_job():
        base = Base()
        engine = base.client
        metadata = MetaData()

        # Create user table
        Table("users", metadata, Column("id", BIGINT, primary_key=True))
        metadata.create_all(engine)

        logger.info("Migrating users table..")
        create_column(engine, "users", "username", "TEXT")
        create_column(engine, "users", "display_avatar", "TEXT")
        create_column(engine, "users", "display_name", "TEXT")
        create_column(engine, "users", "is_bot", "BOOLEAN")
        create_column(engine, "users", "created_at", "TIMESTAMP")
        create_column(engine, "users", "joined_at", "TIMESTAMP")
        create_column(engine, "users", "taro_coin", "BIGINT DEFAULT 0")
        migrate_user_data(bot=bot)
        logger.info(f"Migrate users table done")

        return True

    @jobs(scheduler=scheduler, cron="0 0 * * *", controller=app)
    @handle_job_error
    def migrate_vault_data_job():
        base = Base()
        engine = base.client
        metadata = MetaData()
        vault = Vault()
        item = Item()
        seed = Seed()

        # Create all table
        Table("vault", metadata, Column("name", TEXT, primary_key=True))
        Table("transaction", metadata, Column("id", TEXT, primary_key=True))
        Table("item", metadata, Column("name", TEXT, primary_key=True))
        Table("seed", metadata, Column("name", TEXT, primary_key=True))
        Table("farm", metadata, Column("id", BIGINT, primary_key=True, autoincrement="auto"))
        Table("inventory", metadata, Column("id", BIGINT, primary_key=True, autoincrement="auto"))
        metadata.create_all(engine)

        logger.info("Migrating transaction table..")
        create_column(engine, "transaction", "token", "TEXT")
        create_column(engine, "transaction", "from_id", "BIGINT")
        create_column(engine, "transaction", "to_id", "BIGINT")
        create_column(engine, "transaction", "amount", "BIGINT")
        create_column(engine, "transaction", "status", "TEXT")
        create_column(engine, "transaction", "date", "TIMESTAMP DEFAULT NOW()")
        logger.info(f"Migrate transaction table done")

        logger.info("Migrating vault table..")
        create_column(engine, "vault", "remaining_value", "BIGINT DEFAULT 0")
        create_column(engine, "vault", "init_value", "BIGINT DEFAULT 0")
        create_column(engine, "vault", "relate_table", "TEXT")
        create_column(engine, "vault", "relate_column", "TEXT")
        vault.create_or_update_value_vault(name="taro_coin", init_value=5000000, relate_table="users",
                                           relate_column="taro_coin")
        logger.info(f"Migrate vault table done")

        logger.info("Migrating inventory table..")
        create_column(engine, "inventory", "user_id", "BIGINT")
        create_column(engine, "inventory", "item_bane", "TEXT")
        create_column(engine, "inventory", "quantity", "BIGINT DEFAULT 0")
        logger.info(f"Migrate inventory table done")

        logger.info("Migrating item table..")
        create_column(engine, "item", "type", "TEXT")
        create_column(engine, "item", "emoji", "TEXT")
        create_column(engine, "item", "sell_token", "TEXT")
        create_column(engine, "item", "sell_amount", "BIGINT")
        create_column(engine, "item", "buy_token", "TEXT")
        create_column(engine, "item", "buy_amount", "BIGINT")
        create_column(engine, "item", "can_sell", "BOOLEAN DEFAULT FALSE")
        create_column(engine, "item", "can_buy", "BOOLEAN DEFAULT FALSE")
        item.create_or_update_item_by_name(name="bean_seed", type="seed", sell_token="-", sell_amount=0, can_sell=False,
                                           buy_token="taro_coin", buy_amount=20, can_buy=True, emoji="🫘")
        item.create_or_update_item_by_name(name="seed", type="product", sell_token="taro_coin", sell_amount=15, can_sell=True,
                                           buy_token="-", buy_amount=0, can_buy=False, emoji="🫘")
        logger.info(f"Migrate item table done")

        logger.info("Migrating seed table..")
        create_column(engine, "seed", "emoji", "TEXT")
        create_column(engine, "seed", "harvest_time_interval", "BIGINT")
        create_column(engine, "seed", "drop_item_name", "TEXT")
        create_column(engine, "seed", "drop_item_quantity", "BIGINT DEFAULT 1")
        create_column(engine, "seed", "max_harvest_count", "BIGINT DEFAULT 1")
        seed.create_or_update_seed_by_name(name="bean_seed", emoji="🫘", harvest_time_interval=(6 * 60 * 60),
                                           drop_item_name="bean", drop_item_quantity=2, max_harvest_count=3)
        logger.info(f"Migrate seed table done")

        logger.info("Migrating farm table..")
        create_column(engine, "farm", "user_id", "BIGINT")
        create_column(engine, "farm", "harvest_time", "TIMESTAMP")
        create_column(engine, "farm", "seed_name", "TEXT")
        create_column(engine, "farm", "harvest_count", "BIGINT DEFAULT 0")
        create_column(engine, "farm", "level", "BIGINT DEFAULT 1")
        create_column(engine, "farm", "is_decay", "BOOLEAN DEFAULT FALSE")
        logger.info(f"Migrate farm table done")

        return True

    def migrate_user_data(bot: discord.Client):
        try:
            users = get(f"{config.get('TARO_CONTROLLER_ENDPOINT')}/users").json()
            vault = Vault(name="taro_coin")

            for user_data in users.get("datas", []):
                user = User(id=int(user_data["user_id"]))
                user.create_or_update_by_id(id=int(user_data["user_id"]),
                                            username=str(user_data["name"]),
                                            display_avatar=str(user_data["display_avatar"]),
                                            display_name=str(user_data["display_name"]),
                                            is_bot=bool(user_data["is_bot"]),
                                            created_at=str(user_data["created_at"]),
                                            joined_at=str(user_data["joined_at"]))
                if config.get("ENV") == "production":
                    vault.create_transaction(token_name=vault.name, from_id=bot.user.id,
                                             to_id=int(user_data["user_id"]), amount=100)

        except Exception as error:
            logger.error(f"Skip 'migrate_user_data' get some error {error}")

    def create_column(engine, table, column_name, type):
        try:
            logger.info(f"ALTER TABLE {table} ADD COLUMN {column_name} {type};")
            with engine.begin() as conn:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_name} {type};"))
        except Exception as e:
            return False
