import logging
logging.basicConfig(filename="logs.log", level="INFO", format="%(filename)s-%(module)s-"
                                                              "%(levelname)s -LINE:%(lineno)d -"
                                                              "%(funcName)s - %(message)s - %(asctime)s")

logger = logging.getLogger()
def log_func(func):
    def wrapper(*args):
        try:
            logger.info(f"In function:{func.__name__}")
            result = func(*args)
            logger.info(f"Successfully finished function")
            return result
        except Exception as ex:
            logger.error(f"Arguments: {args}\nError:{ex}")
            return -1

    return wrapper
