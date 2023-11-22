import logging
from os import path, mkdir
from datetime import datetime
from xdg_base_dirs import xdg_data_home


def setup_logging(loglevel):
    # Create directory for storing app info in running machine's application data files directory 
    # as per XDG Base Directory specs (https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
    app_data_dir = xdg_data_home()
    rupantar_data_dir = path.join(app_data_dir, "rupantar")
    rupantar_logs_dir = path.join(rupantar_data_dir, "logs")

    # print(f"Application data files in this machine stored in: {str(app_data_dir)}")

    if not path.exists(rupantar_data_dir):
            try:
                mkdir(rupantar_data_dir)
                # Also create a logs/ subdirectory in this location
                if not path.exists(rupantar_logs_dir):
                    try:
                        mkdir(rupantar_logs_dir)
                    except OSError as err:
                        print(f'Error creating rupantar logs directory: {err}')
            
            except OSError as err:
                print(f'Error creating rupantar local data directory: {err}')

    # Configure logging
    # https://sematext.com/blog/python-logging/#basic-logging-configuration
    log_format_string_default = "%(asctime)s | [%(levelname)s] @ %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) => %(message)s"
    # logging.basicConfig(level=loglevel, format=log_formatter) # init root logger
    logger = logging.getLogger()  # root logger
    logger.setLevel(loglevel)

    # Set handler for destination of logs, default to sys.stderr
    # Log destination = console
    logs_console_handler = logging.StreamHandler()
    logs_console_handler.setLevel(loglevel)
    # logger.addHandler(logs_console_handler)

    # Log destination = file
    log_filename = "rupantar-" + datetime.now().strftime("%H-%M-%S_%p") + ".log"
    #log_filename = f"rupantar-{datetime.datetime.now():%H-%M-%S_%p}.log"
    log_filepath = path.join(rupantar_logs_dir, log_filename)
    logs_file_handler = logging.FileHandler(filename=log_filepath)
    # Create formatter object
    file_handler_format = logging.Formatter(log_format_string_default)
    logs_file_handler.setFormatter(file_handler_format)
    logs_file_handler.setLevel(loglevel)
    # Assign handler to root logger
    logger.addHandler(logs_file_handler)
