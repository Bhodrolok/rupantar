from typing import Sequence
from watchfiles import run_process, DefaultFilter
from logging import getLogger
from pathlib import Path
from rupantar.sohoj.server import start_server
from rupantar.sohoj.utils import watch_dir_v2, resolve_path
from rupantar.sohoj.configger import Config

logger = getLogger()


class OutputDirFilter(DefaultFilter):
    """watchfiles.DefaultFilter-inherited class to define a custom filter (an optional arg to watchfiles.watch).

    Sets up exclusion from monitoring of changes, by defining the full names of directories to be ignored.

    Note:
        Prevents an infinite loop of rebuilding on changes & reserving of files as the being-built output directory will perma trigger a change.

    Args:
        exclude_dirs (Sequence of str): Full name of directories to be ignored. Defaults to ["public"] as that is the default name of the output directory containing the generated files to be served.

    """

    def __init__(self, *, exclude_dirs: Sequence[str] = None) -> None:
        if exclude_dirs is None:
            exclude_dirs = ["public"]

        super().__init__(ignore_dirs=exclude_dirs)


def start_watchful_server(
    project_folder: str,
    config_file_name: str,
    port: int,
    interface_address: str,
    open_url: bool,
) -> None:
    """Start a HTTP web server to serve generated files of a rupantar project, re-builds and then re-serves on changes to the project.

    Ideal for testing the site locally on any machine without pressing Ctrl + F5 on browser on every change.
    Here's how it currently 'flows':
        1. The start_server() is invoked by run_process() # Runs a process
        2. This consequently also calls build_project() and generates a output directory, within the monitored directory, containing the built site.
        3. The HTTP web server is started
        4. Monitor provided directory for changes
        5. If a change is detected, process from 1. is restarted
        6. Consequently 2. - 3. is repeated, with the new changes reflected in a new browser tab.
        7. Repeat until a KeyboardInterrupt is received # Ctrl + C

    Note:
        Reference for watchfile's run_process: https://watchfiles.helpmanual.io/api/run_process/#watchfiles.run_process
        This does NOT hot-reload changes on the same browser tab that is open.
        That would require some client-side .JS code for communicating with this web server.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' and 'notes' directories are located.
        config_file_name (str): The name of the configuration file. Defaults to config.yml if not explicitly provided.
        port (int): The port number to use for the web server. If the port is None or in the range 0-1024, a random port in the range 49152-65535 is used as default.
        interface_address (str): The network address to use for the web server. If the address is not valid, '127.0.0.1' i.e. localhost is used as default.
        open_url (bool): If True, opens the serving URL in a new tab of the default browser. Defaults to False.

    Raises:
        Exception: If any error starting the web server (or while serving the files...).

    """
    try:
        config_file = "config.yml" if (config_file_name is None) else config_file_name
        project_folder_path = resolve_path(project_folder, strict=True)
        config_file_path = resolve_path(project_folder_path, config_file, strict=True)
        # Instantiate Config object for reading and loading config data values
        config = Config(config_file_path)
        # Ignore changes in the output directory where rendered pages will be located
        exclude_dir = Path(project_folder_path, config.home_path)

        print(
            f"Listening for changes in: {project_folder_path} except in the: {exclude_dir.name} directory"
        )

        run_process(
            project_folder,
            target=start_server,
            args=(project_folder, config_file_name, port, interface_address, open_url),
            callback=watch_dir_v2,
            watch_filter=OutputDirFilter(exclude_dirs=[config.home_path]),
        )
    except Exception as err:
        logger.exception(f"Error: {err}")


# # Entry point
# if __name__ == "__main__":
#     print("Direct modular execution!")
