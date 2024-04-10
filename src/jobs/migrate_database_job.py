import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.job import jobs
from ..utils.config import Config
from ..utils.logger import Logger
from ..utils.error_handle import handle_job_error
from ..module.base import Base
from ..module.users import User
from sqlalchemy import MetaData, Table, Column, text, BIGINT, TEXT
from requests import get


def init_migrate_database_job(scheduler: BackgroundScheduler, bot: discord.Client, app: Flask = None):
    config = Config()
    logger = Logger()

    @jobs(scheduler=scheduler, cron="0 22 * * *", controller=app)
    @handle_job_error
    def migrate_database_job():
        base = Base()
        engine = base.client
        metadata = MetaData()

        # Create All table
        Table("users", metadata, Column("id", BIGINT, primary_key=True))
        Table("vault", metadata, Column("name", TEXT, primary_key=True))
        metadata.create_all(engine)

        logger.info("Migrating users table..")
        create_column(base.connect, "users", "username", "TEXT")
        create_column(base.connect, "users", "display_avatar", "TEXT")
        create_column(base.connect, "users", "display_name", "TEXT")
        create_column(base.connect, "users", "is_bot", "BOOLEAN")
        create_column(base.connect, "users", "created_at", "TIMESTAMP")
        create_column(base.connect, "users", "joined_at", "TIMESTAMP")
        create_column(base.connect, "users", "taro_coin", "BIGINT DEFAULT 0")
        migrate_user_data()
        logger.info(f"Migrate users table done")

        logger.info("Migrating vault table..")
        create_column(base.connect, "vault", "init_value", "BIGINT DEFAULT 0")
        create_column(base.connect, "vault", "remaining_value", "BIGINT DEFAULT 0")
        create_column(base.connect, "vault", "relate_table", "TEXT")
        create_column(base.connect, "vault", "relate_column", "TEXT")
        logger.info(f"Migrate vault table done")

        return True

    def migrate_user_data():
        try:
            users = get(f"{config.get('TARO_CONTROLLER_ENDPOINT')}/users").json()

            for user_data in users.get("datas", []):
                user = User()
                user.create_or_update_by_id(id=int(user_data["user_id"]),
                                            username=str(user_data["name"]),
                                            display_avatar=str(user_data["display_avatar"]),
                                            display_name=str(user_data["display_name"]),
                                            is_bot=bool(user_data["is_bot"]),
                                            created_at=str(user_data["created_at"]),
                                            joined_at=str(user_data["joined_at"]))

        except Exception as error:
            logger.error(f"Skip 'migrate_user_data' get some error {error}")

    def create_column(engine, table, column_name, type):
        try:
            logger.info(f"ALTER TABLE {table} ADD COLUMN {column_name} {type};")
            with engine.begin():
                engine.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_name} {type};"))
        except Exception as e:
            return False
