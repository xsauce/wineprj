import os
import settings

__author__ = 'sam'
import logging


def get_logger(log_name=''):
    logger = logging.getLogger(log_name)
    logger.setLevel(getattr(logging, settings.LOG_CONF['level']))
    fh = logging.FileHandler(os.path.join(settings.LOG_CONF['dir'], log_name + '.log'))
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

