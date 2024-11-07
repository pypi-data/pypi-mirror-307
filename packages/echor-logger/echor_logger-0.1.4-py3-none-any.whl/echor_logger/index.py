from .logError import log_error
from .logSuccess import log_success, log_warn


class EchorLogger:
    def info(self, *args, **kwargs):
        log_success(*args, **kwargs)

    def warn(self, *args, **kwargs):
        log_warn(*args, **kwargs)

    def error(self, *args, **kwargs):
        log_error(*args, **kwargs)


echorLogger = EchorLogger()
