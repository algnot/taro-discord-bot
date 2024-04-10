from sqlalchemy import create_engine
from ..utils.config import Config
from ..utils.logger import Logger
from sqlalchemy import text


class Base:
    client = None
    connect = None
    config = None
    logger = None

    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.client = create_engine(url=self.config.get("POSTGRES_URL"))
        self.connect = self.client.connect()

    def __enter__(self):
        self.client = create_engine(url=self.config.get("POSTGRES_URL"))
        self.connect = self.client.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.close()
        self.client.dispose()
        return self

    def execute(self, query, *args, **kwargs):
        try:
            with self.client.begin() as conn:
                res = conn.execute(text(query), *args)
                results = []

                if not res or not res.returns_rows:
                    return []

                for row in res:
                    results.append(row._mapping)
                return results
        except Exception as error:
            self.logger.info(f"Con not execute '{query}' database will rollback with error {error}")
            return []
