import discord
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from ..utils.job import jobs
from ..utils.config import Config
from ..utils.logger import Logger
from ..utils.error_handle import handle_job_error
from ..module.base import Base
from sqlalchemy import MetaData, Table, Column, Text, text


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
        Table("users", metadata, Column("id", Text, primary_key=True))
        metadata.create_all(engine)

        logger.info("Migrating users table..")
        create_column(base.connect, "users", "username", "TEXT")
        create_column(base.connect, "users", "display_avatar", "TEXT")
        create_column(base.connect, "users", "display_name", "TEXT")
        create_column(base.connect, "users", "is_bot", "BOOLEAN")
        create_column(base.connect, "users", "created_at", "TIMESTAMP")
        create_column(base.connect, "users", "joined_at", "TIMESTAMP")
        logger.info(f"Migrate users table done")

        return True

    def create_column(engine, table, column_name, type):
        try:
            logger.info(text(f"ALTER TABLE {table} ADD COLUMN {column_name} {type};"))
            return engine.execute(text(f"ALTER TABLE {table} ADD COLUMN {column_name} {type}; COMMIT;"))
        except Exception as e:
            return False
