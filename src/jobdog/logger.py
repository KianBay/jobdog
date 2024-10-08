import logging

logger = logging.getLogger("jobdog")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)

def info(message: str):
    logger.info(message)

def error(message: str):
    logger.error(message)

def debug(message: str):
    logger.debug(message)

def warn(message: str):
    logger.warning(message)