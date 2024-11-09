import logging
from functools import cached_property


class LoggerMixin:  # pylint: disable=too-few-public-methods
    @cached_property
    def logger(self) -> logging.Logger:
        name = ".".join([self.__class__.__module__, self.__class__.__name__])
        return logging.getLogger(name)
