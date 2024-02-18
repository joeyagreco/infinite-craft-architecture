import logging
import sys
from logging import LogRecord

from .CustomFormatter import CustomFormatter


class CustomLogRecord(LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.levelno == CustomFormatter.IMPORTANT_INFO_LEVEL_NUM:
            self.levelname = "IMPORTANT"


class CustomLogger:
    @staticmethod
    def get_logger() -> logging.Logger:
        log_level = logging.INFO
        logging.setLogRecordFactory(CustomLogRecord)

        logger = logging.getLogger("root")
        logger.setLevel(log_level)

        # Attach custom log methods
        setattr(
            logger,
            "important",
            lambda msg, *args, **kws: logger.log(
                CustomFormatter.IMPORTANT_INFO_LEVEL_NUM, msg, *args, **kws
            ),
        )

        logging.addLevelName(CustomFormatter.IMPORTANT_INFO_LEVEL_NUM, "IMPORTANT_INFO")

        if not logger.hasHandlers():
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(log_level)

            formatter = CustomFormatter(
                format_str="%(asctime)-8s %(levelname)-8s %(message)s",
                time_format_str="%Y-%m-%d %H:%M:%S",
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @staticmethod
    def finalize_loggers() -> None:
        """
        discord loggers are noisy, set them to info always.
        When dealing with noisy loggers, see all the ones using this code:
        all_loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]

        for logger in all_loggers:
            print(f"Logger Name: {logger.name}, Level: {logging.getLevelName(logger.level)}")
        exit()
        """
        discord_logger = logging.getLogger("discord")
        discord_logger.setLevel(logging.INFO)
