import logging

logger = logging.getLogger(__name__)


class EZQError(Exception):
    pass


class EZQEndError(EZQError):
    pass


class EZQInterruptError(EZQError):
    pass
