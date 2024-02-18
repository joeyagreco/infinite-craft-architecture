import logging


class CustomFormatter(logging.Formatter):
    IMPORTANT_INFO_LEVEL_NUM = 21  # 1 more than info

    GREY = "\x1b[38;21m"
    BLUE = "\x1b[38;5;39m"
    YELLOW = "\x1b[38;5;226m"
    RED = "\x1b[38;5;196m"
    BOLD_RED = "\x1b[31;1m"
    GREEN = "\x1b[38;5;82m"
    RESET = "\x1b[0m"

    def __init__(self, *, format_str: str, time_format_str: str):
        super().__init__()
        self.format_str = format_str
        self.timeFormatStr = time_format_str
        self.FORMATS = {
            logging.DEBUG: self.GREY + self.format_str + self.RESET,
            logging.INFO: self.BLUE + self.format_str + self.RESET,
            self.IMPORTANT_INFO_LEVEL_NUM: self.GREEN + self.format_str + self.RESET,
            logging.WARNING: self.YELLOW + self.format_str + self.RESET,
            logging.ERROR: self.RED + self.format_str + self.RESET,
            logging.CRITICAL: self.BOLD_RED + self.format_str + self.RESET,
        }

    def format(self, record):
        log_format = self.FORMATS.get(
            record.levelno, self.BLUE + self.format_str + self.RESET
        )  # Fallback to INFO level
        formatter = logging.Formatter(log_format, self.timeFormatStr)
        return formatter.format(record)
