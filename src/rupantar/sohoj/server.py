from http.server import SimpleHTTPRequestHandler
from socket import SOL_SOCKET, SO_REUSEADDR
from socketserver import TCPServer
from functools import partial
from pathlib import Path
from random import randint
from logging import getLogger
import webbrowser as wb

from rupantar.sohoj.configger import Config
from rupantar.sohoj.utils import validate_network_address

logger = getLogger()


def start_server(
    project_folder: str,
    config_file_name: str,
    port: int,
    interface_address: str,
    openURL=False,
) -> None:
    """Start a basic HTTP server to serve the static files of a existing rupantar project.

    Ideal for testing the pages locally on any machine.
    Change the current working directory to the given project folder, reads and loads the configuration data,
    and start the HTTP server at the given network address and port.

    Args:
        project_folder (str): The path to the rupantar project folder where the 'content' and 'notes' directories are located.
        config_file_name (str): The name of the configuration file. Defaults to config.yml if not explicitly provided.
        port (int): The port number to use for the server. If the port is None or in the range 0-1024, a random port in the range 49152-65535 is used as default.
        interface_address (str): The network address to use for the server. If the address is not valid, '127.0.0.1' i.e. localhost is used as default.

    Raises:
        Exception: If any error starting the HTTP server or while serving the files.

    """
    try:
        config_file = "config.yml" if (config_file_name is None) else config_file_name
        # Ephemeral/dynamic/private ports, think good for temporary stuff
        PORT = (
            randint(49152, 65535)
            if ((port is None) or ((port in range(0, 1024))))
            else port
        )
        logger.info("Using port: %s", PORT)
        HOST = (
            interface_address
            if (validate_network_address(interface_address))
            else "127.0.0.1"
        )
        serving_url = f"http://{HOST}:{PORT}"
        logger.info("Using network address: %s", HOST)
        logger.info(f"Web server address: {serving_url}")

        project_folder_path = Path(project_folder).resolve()
        logger.info(f"Rupantar project directory location: {project_folder_path}")
        # Location of tconfig file, assumed to be in abovementioned project folder
        config_file_path = Path(project_folder_path, config_file).resolve()
        logger.info(f"Config file location: {config_file_path}")
        # Instantiate Config object for reading and loading config data values
        config = Config(config_file_path)

        # Define the dir which contains the (built) static sites, and serve out of that instead of the cwd
        serving_dir = Path(project_folder_path, config.home_path)
        logger.info(f"Serving out of directory:  {serving_dir}")

        try:
            handler = partial(SimpleHTTPRequestHandler, directory=serving_dir)
            with TCPServer((HOST, PORT), handler) as httpd:
                # Allow immediate socket re-use
                httpd.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
                print(f"Web server available at: {serving_url}")
                # If ran with `-O/--open`, open the URL in a new tab of the default browser
                # https://docs.python.org/3/library/webbrowser.html#webbrowser.open_new_tab
                if openURL:
                    browser = wb.get()
                    logger.debug(f"Using system default web browser: {str(browser)}")
                    browser.open_new_tab(serving_url)
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server...")
            httpd.server_close()
        except Exception as err:
            logger.exception("Error while serving the server: %s", str(err))

    except Exception as err:
        logger.exception("Error starting server: %s", str(err))
