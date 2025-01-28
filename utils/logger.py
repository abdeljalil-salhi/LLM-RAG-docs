from logging import Logger, getLogger, StreamHandler, INFO

from colorlog import ColoredFormatter


def create_logger() -> Logger:
    logger = getLogger("logger")
    color_handler = StreamHandler()
    color_formatter = ColoredFormatter(
        "%(log_color)s[%(asctime)s][%(filename)s:%(lineno)d]  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    color_handler.setFormatter(color_formatter)
    logger.addHandler(color_handler)
    logger.propagate = False
    logger.setLevel(INFO)
    return logger


logger = create_logger()
