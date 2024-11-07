import logging
import os

def getLogger(config):
    switcher = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
        "fatal": logging.FATAL
    }
    logger = logging.getLogger("gemnify_logger")
    logger.setLevel(switcher.get(config.logger_level.lower(), "info"))

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if config.logger_file_path:
            file_handler = logging.FileHandler(os.path.join(config.logger_file_path, "gemnify.log"))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger