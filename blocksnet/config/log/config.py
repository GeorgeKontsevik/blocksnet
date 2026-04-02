import sys
from tqdm import tqdm
from loguru import logger
from iduedu import config as iduedu_config

LOGGER_LEVELS = {"TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"}
LOGGER_FORMAT = "<green>{time:DD MMM HH:mm}</green> | <level>{level}</level> | <level>{message}</level>"

tqdm.pandas()


class LogConfig:
    def __init__(
        self,
        logger_level="INFO",
        disable_tqdm=False,
    ):
        self.disable_tqdm = disable_tqdm
        self.logger_level = logger_level
        logger.remove()
        logger.add(sys.stderr, level=logger_level, format=LOGGER_FORMAT, colorize=True)

    def set_logger_level(self, level: str):
        if not level in LOGGER_LEVELS:
            raise ValueError(f"Logger should be in {LOGGER_LEVELS}")
        logger.remove()
        self.logger_level = level
        logger.add(sys.stderr, level=level, format=LOGGER_FORMAT, colorize=True)

    def set_disable_tqdm(self, disable: bool):
        self.disable_tqdm = disable
        iduedu_config.set_enable_tqdm(not disable)

    def get_tqdm_kwargs(self, *, leave: bool = False):
        return {
            "disable": self.disable_tqdm or (not sys.stderr.isatty()),
            "leave": leave,
            "ascii": True,
            "dynamic_ncols": True,
            "mininterval": 0.5,
        }


log_config = LogConfig()
