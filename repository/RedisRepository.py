from logging import Logger
from typing import Optional

from redis import Redis, from_url

from model.abstract.Alivable import Alivable


class RedisRepository(Alivable):
    def __init__(self, *, connection_string: str, socket_timeout: int, logger: Logger):
        self.__logger = logger
        self.__connection_string = connection_string
        self.__client: Redis = from_url(self.__connection_string, socket_timeout=socket_timeout)

    def alive(self) -> bool:
        try:
            self.__client.ping()
        except Exception as e:
            self.__logger.error(e)
            return False
        return True

    def name(self) -> str:
        return "redis repository"

    def clear_cache(self) -> None:
        self.__client.flushall()

    def key_exists(self, key: str) -> bool:
        return self.__client.exists(key) == 1

    def get(self, key: str) -> Optional[str]:
        value = None
        byte_value = self.__client.get(key)
        if byte_value is not None:
            value = byte_value.decode("utf-8")
        return value

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        try:
            self.__client.setex(key, ttl_seconds, value)
        except Exception as e:
            self.__logger.error(f"Failed to set key-value pair with TTL: {e}")
