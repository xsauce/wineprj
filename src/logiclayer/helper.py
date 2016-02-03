from models.CommonModel import m2d
from functools import wraps
__author__ = 'samgu'


def return_json(f):
    @wraps(f)
    def _func(*args, **kwargs):
        a = f(*args, **kwargs)
        return m2d(a)

    return _func
