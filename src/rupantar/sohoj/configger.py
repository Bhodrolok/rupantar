from sys import version_info

# Python 3.11 and above ships with a TOML library out-of-the-box, use tomli (https://github.com/hukkin/tomli) otherwise
if version_info <= (3, 10):
    import tomli as tomllib
else:
    import tomllib
from typing import Union
from yaml import safe_load
from pathlib import Path
from logging import getLogger


logger = getLogger()


class Config:
    """Class to represent a literal Configuration object. Makes loading and managing configuration data, from TOML or YAML files, easier.

    Object instantiation accomplished by the __init__ method.

    Args:
      config_file_path(str or Path): Relative path to the configuration file. Accepted file formats are TOML(.toml/.tml) and YAML(.yaml/.yml).

    Raises:
      OSError: If any error opening or reading the configuration file.

    """

    def __init__(self, config_file_path: Union[Path, str]) -> None:
        config_file_extension = Path(config_file_path).resolve().suffix
        global config
        # YAML handling
        if config_file_extension in {".yaml", ".yml"}:
            try:
                with open(config_file_path, "r") as yaml_file:
                    config = safe_load(yaml_file)
                logger.info(f"Loaded configuration data from: {config_file_path}")
            except OSError as err:
                logger.exception(
                    f"Error reading and loading config data from {config_file_path}: {err}"
                )

        # TOML handling
        elif config_file_extension in {".toml", ".tml"}:
            try:
                # https://github.com/hukkin/tomli#parse-a-toml-file
                with open(config_file_path, "rb") as toml_file:
                    config = tomllib.load(toml_file)
                logger.info(f"Loaded configuration data from: {config_file_path}")
            except OSError as err:
                logger.exception(
                    f"Error reading and loading config data from {config_file_path}: {err}"
                )

        # Only TOML/YAML file formats supported
        else:
            logger.warning(f"Config file format: {config_file_extension} NOT supported")

        # Dynamically set attributes to the instance for each key-value pair in the config file
        if config:
            for key, val in config.items():
                setattr(self, key, val)
                logger.debug("Setting attribute '%s' as: %s", key, val)
        else:
            logger.warning("Empty or invalid configuration. No attributes were set.")
