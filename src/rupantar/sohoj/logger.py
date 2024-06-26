"""This module is for setting up logging throughout the rupantar app.

The main function in this module is `setup_logging`, which sets up the logging configuration for the application.
It uses two helper functions: `create_logs_directory` and `setup_logging_dir` to setup the logging directory.
It creates a directory for storing application logs, configures the logging level, and sets up handlers for logging
to both the console and/or a log file on the disk.
The log file is created in the app data directory with the platform name as well as the application run-time timestamp in the filename.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from rupantar.sohoj.utils import resolve_path
from logging import StreamHandler, getLogger, FileHandler, Formatter
import sys
from pathlib import Path
from datetime import datetime
from xdg_base_dirs import xdg_data_home
import sysconfig

def create_logs_directory(path: Path) -> None:
    """Create a directory for storing application run-time logs if it does not exist.

    Args:
        path (Path): The path to the directory to be created.

    Raises:
        OSError: If any error creating the directory.
    """
    if not path.exists():
        try:
            path.mkdir()
        except OSError as err:
            print(f"Error creating logs directory at {path}.\n{err}")
            raise


def setup_logging_dir(
    app_name: str, app_data_dir: str, logs_dir_name: str = "logs"
) -> Path:
    """Setup the app data and logs directories.

    Create the directory for storing app info in running machine's application data/AppData directory

    Args:
        app_name (str): The name of the application. Used for naming the logs directory.
        app_data_dir (str): The path to the application data directory.
        logs_dir_name (str, optional): The name of the logs directory. Sub-directory within the application data directory. Defaults to "logs".

    Returns:
        Path: The absolute path to the created logs directory.
    """

    app_data_dir = resolve_path(app_data_dir, app_name)
    logs_dir = resolve_path(app_data_dir, logs_dir_name)

    create_logs_directory(app_data_dir)
    create_logs_directory(logs_dir)

    return logs_dir


def setup_logging(
        logger_name: str = None, 
        log_level: int = 20, 
        log_to_console: bool = False) -> None:
    """Set up logging configuration for rupantar, app-wide.

    Create a centralized directory for storing application logs, where will this be created in the machine running rupantar?
    Why in the XDG_DATA_HOME directory of course! According to the XDG Base Directory specification, this is the place where
    "user-specific data files should be stored". Seems apt for storing run-time logs.
    Reference: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

    Also configure the logging level and set up handlers for logging to both the console and/or a log file.
    The log files generated will have the platform name along with a timestamp in their filenames.

    Note:
        log_level can be passed when running the script with the -l or --log flag, this is of course entirely optional
        https://docs.python.org/3/library/logging.html#logging-levels
        Level name - Logging level mapping: {'CRITICAL': 50, 'CRITICAL': 50, 'ERROR': 40, 'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}

    Args:
        logger_name (str): The name of the Python module that creates the logger instance to include in the timestamp
        log_level (int): The logging level to set for the application. This should be one of the
        levels specified in the logging module, e.g., logging.INFO, logging.DEBUG, etc.
        Defaults to 20 i.e. INFO level.
        log_to_console (bool): Whether or not to also print out the log messages to the console (stdout) on top of saving to disk.

    Raises:
        OSError: If any error creating the directories or the log file.

    """
    time_stamp = datetime.now().strftime("%X").replace(":", "_")
    rupantar_logs_dir = setup_logging_dir("rupantar", xdg_data_home())

    # Configure logging
    # https://sematext.com/blog/python-logging/#basic-logging-configuration
    # Init the root logger instance
    root_logger = getLogger()
    root_logger.setLevel(log_level)

    # Log message format string
    log_msg_fmt = "[%(levelname).1s]/%(asctime)s.%(msecs).03d -- {%(filename)s} | %(funcName)s at line %(lineno)d => %(message)s"

    # Log destination = console
    if log_to_console:
        logs_console_handler = StreamHandler(sys.stdout)
        logs_console_handler.setFormatter(fmt=Formatter(fmt=log_msg_fmt, datefmt='%m%d %H:%M:%S'))
        logs_console_handler.setLevel(log_level)
        root_logger.addHandler(logs_console_handler)

    # Log destination = (disk log) file
    # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    # Eg: rupantar-win-amd64-10_51_10.log
    log_filename = f"{logger_name}-{sysconfig.get_platform()}-{time_stamp}.log"
    log_filepath = resolve_path(rupantar_logs_dir, log_filename)
    logs_file_handler = FileHandler(filename=log_filepath, mode="a")

    # Create formatter objects
    file_handler_format = Formatter(fmt=log_msg_fmt, datefmt="%d-%b-%Y %H:%M:%S")
    logs_file_handler.setFormatter(file_handler_format)
    # Set level for the file handler to be always debug-level
    logs_file_handler.setLevel(10)

    # Assign the defined handler(s) to the root logger
    root_logger.addHandler(logs_file_handler)
