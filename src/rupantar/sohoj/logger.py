import logging
from os import path, mkdir
from datetime import datetime

def setup_logging(loglevel):
    log_format_string_default = "%(asctime)s | [%(levelname)s] @ %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) => %(message)s"
    # https://sematext.com/blog/python-logging/#basic-logging-configuration
    # Root logger
    logger = logging.getLogger()
    logger.setLevel(loglevel)

    if not path.exists('logs'):
        try:
            mkdir('logs')
        except OSError as err:
            logging.exception("%s", err)

    # Set log destination as file in the 'logs' directory
    log_filename = 'rupantar-' + datetime.now().strftime("%H-%M-%S_%p") + '.log'
    log_filepath = 'logs/' + log_filename
    logs_file_handler = logging.FileHandler(filename=log_filepath)
    # Create formatter object
    file_handler_format = logging.Formatter(log_format_string_default)
    logs_file_handler.setFormatter(file_handler_format)
    logs_file_handler.setLevel(loglevel)
    # Assign handler to the root logger
    logger.addHandler(logs_file_handler)
