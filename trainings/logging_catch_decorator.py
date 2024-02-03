import logging
from datetime import datetime
from functools import wraps


logger = logging.getLogger()


def catch_and_log():
    def wrapper(f):
        @wraps(f)
        def inner(*a, **kw):
            try:
                return f(*a, **kw)
            except Exception as e:
                f_name = f.__qualname__
                logger.error(f'Error at "{f_name}": {str(e)}')
                logger.error('Calling signature with passed parameters:')
                logger.error(f'{f_name}(')
                
                for arg in a:
                    logger.error(f'    {arg},')
                
                for arg, value in kw.items():
                    logger.error(f'    {arg}={str(value)},')
                
                logger.error(')')
                
                if a:
                    logger.error(f'args: {a}')
                if kw:
                    logger.error(f'kwargs:')
                    for arg, value in kw.items():
                        logger.error(f'{arg}: {value}')
        return inner
    return wrapper

class Test:
    @staticmethod
    @catch_and_log()
    def test(a, b, *, c=None, d=3):
        x = 1 / 0


Test.test(5, 'sef', c=type, d=datetime.now())
