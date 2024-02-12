import logging
from functools import wraps

logger = logging.getLogger(__name__)


def log_if_errors(*, reraise=True):
    def wrapper(f):
        @wraps(f)
        def inner(*a, **kw):
            try:
                return f(*a, **kw)
            except Exception as e:
                f_name = f.__qualname__
                logger.error(f'Error at "{f_name}": {str(e)}')

                if reraise:
                    raise e

        return inner

    return wrapper
