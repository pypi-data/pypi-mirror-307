import logging
from typing import Optional


class Logger:
    def __init__(
        self,
        logger_name: str,
        log_file_path: Optional[str] = None,
        log_level=logging.INFO,
    ):
        self.__logger = logging.getLogger(logger_name)
        self.__logger.setLevel(log_level)

        self.__logger.handlers = []
        formatter = logging.Formatter(
            "[%(asctime)s] - [%(filename)s file line:%(lineno)d] - %(levelname)s: %(message)s"
        )

        if log_file_path is not None:
            file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
            file_handler.setFormatter(formatter)
            self.__logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.__logger.addHandler(console_handler)

    def get_logger(self) -> logging.Logger:
        return self.__logger
