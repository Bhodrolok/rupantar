"""This module is for setting up logging throughout the rupantar app.

The main function in this module is `setup_logging`, which sets up the logging configuration for the application.
It uses two helper functions: `create_logs_directory` and `setup_logging_dir` to setup the logging directory.
It creates a directory for storing application logs, configures the logging level, and sets up handlers for logging
to both the console and/or a log file on the disk.
The log file is created in the app data directory with the platform name as well as the run-time timestamp in the filename.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""

from logging import getLogger, FileHandler, Formatter
from pathlib import Path
from datetime import datetime
from xdg_base_dirs import xdg_data_home
import sysconfig

from rupantar.sohoj.utils import resolve_path


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


def setup_logging(loglevel: int = 20) -> None:
    """Set up logging configuration for rupantar, app-wide.

    Create a centralized directory for storing application logs, where will this be created in the machine running rupantar?
    Why in the XDG_DATA_HOME directory of course! According to the XDG Base Directory specification, this is the place where
    "user-specific data files should be stored". Seems apt for storing run-time logs.
    Reference: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html

    Also configure the logging level and set up handlers for logging to both the console and/or a log file.
    The log files generated will have the platform name along with a timestamp in their filenames.
    NB: The console handler is commented out currently.

    Note:
        loglevel can be passed when running the script with the -l or --log flag, this is of course entirely optional

    Args:
        loglevel (int): The logging level to set for the application. This should be one of the
        levels specified in the logging module, e.g., logging.INFO, logging.DEBUG, etc.
        Defaults to 20 i.e. INFO level.
        https://docs.python.org/3/library/logging.html#logging-levels
        Level name - Logging level mapping: {'CRITICAL': 50, 'FATAL': 50, 'ERROR': 40, 'WARN': 30, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10, 'NOTSET': 0}

    Raises:
        OSError: If any error creating the directories or the log file.

    """
    rupantar_logs_dir = setup_logging_dir("rupantar", xdg_data_home())

    # Configure logging
    # https://sematext.com/blog/python-logging/#basic-logging-configuration
    # Init the root logger
    logger = getLogger()
    logger.setLevel(loglevel)
    log_format_string_default = "{%(filename)s} | %(asctime)s | [%(levelname)s] at %(name)s: %(funcName)s, line %(lineno)d => %(message)s"

    # Log destination = console
    # logs_console_handler = StreamHandler()
    # logs_console_handler.setFormatter(Formatter(log_format_string_default))
    # logs_console_handler.setLevel(loglevel)
    # logger.addHandler(logs_console_handler)

    # Log destination = (disk log) file
    # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    time_stamp = datetime.now().strftime("%X").replace(":", "_")
    log_filename = f"rupantar-{sysconfig.get_platform()}-{time_stamp}.log"
    log_filepath = resolve_path(rupantar_logs_dir, log_filename)
    logs_file_handler = FileHandler(filename=log_filepath, mode="a")

    # Create formatter objects
    file_handler_format = Formatter(
        fmt=log_format_string_default, datefmt="%d-%b-%Y %H:%M:%S"
    )
    logs_file_handler.setFormatter(file_handler_format)
    # Set level for file handler to be always debug-lvl
    logs_file_handler.setLevel(10)

    # Assign handler(s) to the root logger
    logger.addHandler(logs_file_handler)
