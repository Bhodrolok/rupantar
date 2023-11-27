"""This module is for setting up logging throughout the rupantar app.

The main function in this module is `setup_logging`, which sets up the logging configuration for the application. 
It creates a directory for storing application logs, configures the logging level, and sets up handlers for logging 
to both the console and/or a log file. The log file is created in the application's data directory with the run-time timestamp in its name.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""


# import logging
from logging import StreamHandler, getLogger, FileHandler, Formatter
from os import path, mkdir
from datetime import datetime
from xdg_base_dirs import xdg_data_home


def setup_logging(loglevel):
    """Set up logging configuration for rupantar, app-wide.

    Create a centralized directory for storing application logs, where will this be created in the machine running rupantar?
    Why in the XDG_DATA_HOME directory of course! According to the XDG Base Directory specification, this is the place where
    "user-specific data files should be stored". Seems apt for storing run-time logs.
    Reference: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    Also configure the logging level and set up handlers for logging to both the console and/or a log file.
    The console handler is commented out currently.
    The log files generated in the application's data directory will have with a timestamp in their filenames.

    Note:
        loglevel can be passed when running the script with a -l flag, this is of course entirely optional. Defaults to INFO anyways.

    Args:
        loglevel (int): The logging level to set for the application. This should be one of the
                        levels specified in the logging module, e.g., logging.INFO, logging.DEBUG, etc.

    Raises:
        OSError: If any error creating the directories or the log file.

    """
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
                    print(f"Error creating rupantar logs directory: {err}")

        except OSError as err:
            print(f"Error creating rupantar local data directory: {err}")

    # Configure logging
    # https://sematext.com/blog/python-logging/#basic-logging-configuration
    log_format_string_default = "%(asctime)s | [%(levelname)s] @ %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) => %(message)s"
    # logging.basicConfig(level=loglevel, format=log_formatter) # init root logger
    logger = getLogger()  # root logger
    logger.setLevel(loglevel)

    # Set handler for destination of logs, default to sys.stderr
    # Log destination = console
    logs_console_handler = StreamHandler()
    logs_console_handler.setLevel(loglevel)
    logs_console_handler.setFormatter(Formatter(log_format_string_default))
    # logger.addHandler(logs_console_handler)

    # Log destination = file
    log_filename = "rupantar-" + datetime.now().strftime("%H-%M-%S_%p") + ".log"
    # log_filename = f"rupantar-{datetime.datetime.now():%H-%M-%S_%p}.log"
    log_filepath = path.join(rupantar_logs_dir, log_filename)
    logs_file_handler = FileHandler(filename=log_filepath)
    # Create formatter object
    file_handler_format = Formatter(log_format_string_default)
    logs_file_handler.setFormatter(file_handler_format)
    logs_file_handler.setLevel(loglevel)
    # Assign handler to root logger
    logger.addHandler(logs_file_handler)
