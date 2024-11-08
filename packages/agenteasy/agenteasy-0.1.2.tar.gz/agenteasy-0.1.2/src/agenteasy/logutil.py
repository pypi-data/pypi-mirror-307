import logging
from .config import settings


# class SpecificLoggerFilter(logging.Filter):
#     def __init__(self, logger_name):
#         self.logger_name = logger_name

#     def filter(self, record):
#         return record.name == self.logger_name


logger_name = "agentlog"
# handler = logging.StreamHandler()
# handler.addFilter(SpecificLoggerFilter(logger_name))
FORMAT = "%(levelname)-5s:  [%(asctime)s] %(name)s (%(filename)s - %(funcName)s - %(lineno)d) - %(message)s"
level = logging.DEBUG if settings.DEBUG else logging.WARNING
logging.basicConfig(
    format=FORMAT,
    encoding="utf-8",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=level,
)
logger = logging.getLogger(logger_name)

