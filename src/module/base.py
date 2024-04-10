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
            with self.client.begin():
                res = self.connect.execute(text(query), args[0])
                self.connect.commit()
            results = []

            if not res or not res.returns_rows:
                return []

            for row in res:
                result = {}
                for key in row.keys():
                    result[key] = row[key]
                results.append(result)
            return results
        except Exception as error:
            self.connect.rollback()
            self.logger.info(f"Con not execute '{query}' database will rollback with error {error}")
            return []

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if not key.startswith("_")}
