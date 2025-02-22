class EZQError(Exception):
    pass


class EZQEndError(EZQError):
    pass


class EZQInterruptError(EZQError):
    pass


class NonExistingEventError(EZQError):
    pass
