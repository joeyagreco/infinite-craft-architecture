import time
from logging import Logger

from model.abstract.Alivable import Alivable


class AliveService:
    def __init__(self, *, logger: Logger, alivables: list[Alivable]):
        self.__logger = logger
        self.__alivables = alivables

    def wait_for_all_alive(self) -> None:
        alive = set()
        while len(alive) < len(self.__alivables):
            for index, alivable in enumerate(self.__alivables):
                if index not in alive and alivable.alive():
                    alive.add(index)
                    self.__logger.info(f"SERVICE {alivable.name().upper()} ONLINE")

            time.sleep(0.5)
