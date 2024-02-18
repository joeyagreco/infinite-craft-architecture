import os

from dotenv import load_dotenv


class EnvironmentReader:
    @classmethod
    def get(cls, name: str) -> str:
        load_dotenv()
        return os.getenv(name)
