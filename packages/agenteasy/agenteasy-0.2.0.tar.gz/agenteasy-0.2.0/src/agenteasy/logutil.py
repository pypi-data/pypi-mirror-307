import logging
from .config import settings

logger_name = "agentlog"
FORMAT = "%(levelname)-5s:  [%(asctime)s] %(name)s (%(filename)s - %(funcName)s - %(lineno)d) - %(message)s"
level = logging.DEBUG if settings.DEBUG else logging.WARNING
if level == logging.DEBUG:
    logging.basicConfig(
        format=FORMAT,
        encoding="utf-8",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
    )
logger = logging.getLogger(logger_name)
