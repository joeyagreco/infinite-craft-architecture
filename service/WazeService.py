import os
from logging import Logger
from typing import Optional

from client.OpenAiClient import OpenAiClient
from model.Waze import Waze
from repository.RedisRepository import RedisRepository
from repository.WazeRepository import WazeRepository
from util.file import load_file_to_string


class WazeService:
    """
    WAZE = word or phrase
    """

    def __init__(
        self,
        *,
        logger: Logger,
        redis_repository: RedisRepository,
        waze_repoisitory: WazeRepository,
        open_ai_client: OpenAiClient,
    ):
        self.__logger = logger
        self.__redis_repository = redis_repository
        self.__waze_repository = waze_repoisitory
        self.__open_ai_client = open_ai_client
        self.__redis_repository.clear_cache()
        self.__ERROR_WAZE = "ERROR"
        self.__KEY_TTL_SECONDS = 1000
        self.__CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.__PROMPT_FILE_PATH = os.path.abspath(
            os.path.join(self.__CURRENT_FILE_PATH, "../data/waze_prompt.txt")
        )
        self.__STARTING_WAZES_FILE_PATH = os.path.abspath(
            os.path.join(self.__CURRENT_FILE_PATH, "../data/starting_wazes.txt")
        )
        self.__PROMPT = load_file_to_string(self.__PROMPT_FILE_PATH)
        self.__STARTING_WAZES = {
            self.clean_waze(w)
            for w in load_file_to_string(self.__STARTING_WAZES_FILE_PATH).split("\n")
        }

        self.__waze_repository.insert_wazes(
            [Waze(waze=w) for w in self.__STARTING_WAZES], do_nothing_on_conflict=True
        )

    def clean_waze(self, waze: str) -> str:
        waze = waze.lower()
        waze = waze.strip()
        waze = waze.strip("'\"")
        return waze

    def __get_key_from_wazes(self, waze_1: str, waze_2: str) -> str:
        # we need to sort these alphabetically to ensure ("a", "b") gives the same output as ("b", "a")
        return "|".join(sorted([waze_1, waze_2]))

    def __add_waze(self, waze: str) -> bool:
        """
        Adds the given waze to the long-term storage if it doesn't already exist there.
        Returns a boolean of whether this was a new waze or not.
        """
        return (
            self.__waze_repository.insert_wazes([Waze(waze=waze)], do_nothing_on_conflict=True) == 1
        )

    def get_all_starting_wazes(self) -> set[str]:
        return self.__STARTING_WAZES

    def __get_waze_from_wazes(self, waze_1: str, waze_2: str) -> str:
        """
        Takes 2 wazes and returns a waze that is the combination of them.
        If this combination already exists, will return the existing combination waze.
        Otherwise, will prompt AI for new combination waze.
        """
        # first, check if this waze already exists
        existing_waze = self.__redis_repository.get(self.__get_key_from_wazes(waze_1, waze_2))
        if existing_waze != None:
            self.__logger.info(f"found existing waze: {existing_waze}")
            return existing_waze
        # waze does not exist, get it from ai
        prompt = f"{self.__PROMPT} INPUT: '{waze_1}', '{waze_2}' OUTPUT:"
        waze = self.__open_ai_client.get_response_from_prompt(prompt)
        if waze.upper() == self.__ERROR_WAZE.upper():
            raise Exception(f"could not get waze for {waze_1} + {waze_2}")
        waze = self.clean_waze(waze)
        self.__logger.info(f"generated new waze: {waze}")
        return waze

    def combine_wazes(self, waze_1: str, waze_2: str) -> tuple[Optional[str], bool]:
        """
        Returns the combination of the given wazes.
        Returns None if the waze could not be combined.
        Returns a 2nd value that is a boolean representing if this was a first discovery or not.
        Writes the waze recipe to the redis cache.
        Writes the resulting waze if it is a first discovery.
        """
        waze_1 = self.clean_waze(waze_1)
        waze_2 = self.clean_waze(waze_2)
        key = self.__get_key_from_wazes(waze_1, waze_2)
        combined_waze = None
        first_discovery = False
        try:
            combined_waze = self.__get_waze_from_wazes(waze_1, waze_2)
        except Exception as e:
            self.__logger.warning(f"error getting waze: {e}")
            combined_waze = self.__ERROR_WAZE

        if combined_waze != self.__ERROR_WAZE and not self.__redis_repository.key_exists(key):
            self.__logger.info("CHECKING FOR FIRST DISCOVERY")
            # not an error
            # not a combination we have in our cache
            first_discovery = self.__add_waze(combined_waze)
            self.__logger.info(f"FIRST DISCOVERY = {first_discovery}")

        # add recipe to redis
        self.__logger.info(f"ADDING {key}:{combined_waze}")
        self.__redis_repository.set(key, combined_waze, self.__KEY_TTL_SECONDS)
        return (
            (combined_waze, first_discovery)
            if combined_waze != self.__ERROR_WAZE
            else (None, first_discovery)
        )
