from client.OpenAiClient import OpenAiClient
from enumeration.OpenAiModel import OpenAiModel
from menu import clear_screen, padding, prompt_for_input
from repository.RedisRepository import RedisRepository
from repository.WazeRepository import WazeRepository
from service.AliveService import AliveService
from service.WazeService import WazeService
from util.ConfigReader import ConfigReader
from util.CustomLogger import CustomLogger
from util.EnvironmentReader import EnvironmentReader

if __name__ == "__main__":
    logger = CustomLogger.get_logger()
    SOCKET_TIMEOUT = ConfigReader.get("app", "DB", "REDIS_SOCKET_TIMEOUT_SECONDS", as_type=int)
    REDIS_CONNECTION_STRING = EnvironmentReader.get("REDIS_CONNECTION_STRING")
    POSTGRES_CONNECTION_STRING = EnvironmentReader.get("POSTGRES_CONNECTION_STRING")
    OPEN_AI_API_KEY = EnvironmentReader.get("OPEN_AI_API_KEY")
    redis_repository = RedisRepository(
        logger=logger, connection_string=REDIS_CONNECTION_STRING, socket_timeout=SOCKET_TIMEOUT
    )
    waze_repository = WazeRepository(connection_string=POSTGRES_CONNECTION_STRING, logger=logger)
    open_ai_client = OpenAiClient(
        logger=logger, api_key=OPEN_AI_API_KEY, chat_completion_model=OpenAiModel.GPT_3_5_TURBO
    )

    # wait for services to come online
    alive_service = AliveService(logger=logger, alivables=[redis_repository, open_ai_client])
    alive_service.wait_for_all_alive()

    waze_service = WazeService(
        logger=logger,
        redis_repository=redis_repository,
        waze_repoisitory=waze_repository,
        open_ai_client=open_ai_client,
    )

    # this keeps track of all wazes the user has unlocked
    unlocked_wazes = waze_service.get_all_starting_wazes()

    # this ensures the user only uses wazes that are unlocked
    def get_validator_func(wazes: set[str]) -> callable:
        def validator_func(user_input: str) -> bool:
            return waze_service.clean_waze(user_input) in wazes

        return validator_func

    while True:
        clear_screen()
        print("WAZES", sorted(unlocked_wazes))
        padding()
        validator_func = get_validator_func(unlocked_wazes)
        waze_1 = prompt_for_input("word 1", validator_func=validator_func)
        padding(2)
        waze_2 = prompt_for_input("word 2", validator_func=validator_func)

        combined_waze, first_discovery = waze_service.combine_wazes(waze_1, waze_2)

        if combined_waze is None:
            print("COULD NOT GET A COMBINATION")
            input()
            continue

        # "unlock" the new waze
        # we use a set here, so duplicates will never be added
        unlocked_wazes.add(waze_service.clean_waze(combined_waze))

        padding()
        print(f"RESULTING WAZE: {combined_waze}")
        if first_discovery:
            padding()
            print("FIRST DISCOVERY!")
        input()
