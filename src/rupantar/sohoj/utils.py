from time import perf_counter
from logging import getLogger
from ipaddress import ip_address
from typing import Union
from pathlib import Path
from watchfiles import watch
from datetime import datetime

logger = getLogger()


def resolve_path(*args: str | Path) -> Path | FileNotFoundError:
    """Resolve the (absolute) path to a file or directory.

    Accepts either a single argument or a tuple of arguments (multiple 'paths').

    Note:
        Path to a File or Directory
        Exception notes reference: https://docs.python.org/3/tutorial/errors.html#enriching-exceptions-with-notes
        and https://peps.python.org/pep-0678/
        Pathlib in general: https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve

    Args:
        path (Path): Path to check for existence.

    Returns:
        Path: The resolved Path to the file or directory.

    Raises:
        FileNotFoundError: File/Directory not found.
    """
    try:
        # If args = single element
        if len(args) == 1:
            return Path(args[0]).resolve(strict=True)
        # Otherwise, treat it as a tuple eg: ('path', 'to', 'dest')
        else:
            return Path(*args).resolve(strict=True)

    except FileNotFoundError as err:
        logger.exception(f"{str(args)} does not exist")
        err.add_note(f"Unable to resolve: {str(args)}")
        raise


def get_func_exec_time(function):
    """Simple decorator function to get a function's execution time, start to finish.

    Args:
        function (callable): The function to be timed.

    Returns:
        Callable: The decorated function.
    """

    def wrap(*args, **kwargs):
        """Wrapper function to time function execution.

        Note:
            The `perf_counter()` function is used for timing, as it measures the actual time taken using the highest resolution timer possible on the system.
            i.e. the most accurate clock on the running platform.

        Args:
            *args: Variable length argument list for the decorated function.
            **kwargs: Arbitrary keyword arguments for the decorated function.

        Returns:
            Any: Same as the return value of the actual (decorated) function.
        """
        start_time = perf_counter()
        og_func_return = function(*args, **kwargs)
        # print(
        #     f"{function.__name__} was completed in: {perf_counter() - start_time} seconds"
        # )
        # end_time = perf_counter()
        logger.debug(
            f"{function.__name__} was completed in: {perf_counter() - start_time} seconds"
        )
        return og_func_return

    return wrap


def validate_network_address(interface_address: str) -> bool:
    """Validate a given network address to check if it is a valid IP address.

    Link-local and multicast addresses are considered to be invalid.

    Note:
        link-local addresses = reserved range of 169.254.1.0 to 169.254.254.255, as per the IETF.
        multicast addresses = reserved range of 224.0.0.0 to 239.255.255.255, as per the IANA

    Args:
      interface_address: Network address to validate

    Returns:
        bool: True if the given network address is a valid, non-link-local, non-multicast IP address. False otherwise.

    """
    try:
        ip = ip_address(interface_address)
        if ip.is_link_local or ip.is_multicast:
            return False
        return True
    except ValueError:
        return False


def get_current_time() -> str:
    """Get the current local time.

    Formatted as Year-Month-Day Hour:Min:Second

    Returns:
        str: String containing the datetime object
    """
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string


def watch_dir(
    monitored_dir: Union[Path, str], project_folder: str, config_file_name: str
) -> None:
    """Monitor the provided directory and print/log information about changes, if any.

    Types of change = For any file/dir: Create new, Delete old, and Modify old.
    Directories watched recursively, so also informs of changes in sub-directories and not just the top-level parent directory.

    Note:
        Reference: https://watchfiles.helpmanual.io/api/watch/#watchfiles.watch

    Args:
        monitored_dir (Path or str): Directory to be watched for changes.

    """
    print(f"Listening for changes in: {monitored_dir}")
    for changes in watch(monitored_dir, raise_interrupt=False):
        # FileChange = Tuple[Change, str]; 'changes' = FileChange
        logger.debug("Change detected.")
        # Re-build project
        # build_project(project_folder, config_file_name)
        # As multiple sets of FileChanges can be returned, iterate through 'em
        for each_change in changes:
            _, change_location = each_change
            logger.debug(f"Full change: {each_change}")
            print(f"Change detected at: {get_current_time()}")
            print(f"File(s) changed: {change_location}")


def watch_dir_v2(changes):
    """Print/log information based on file/directory changes.

    Currently used as a callback for watchfiles.run_process()

    Note:
        https://watchfiles.helpmanual.io/api/run_process/#watchfiles.run_process
        https://watchfiles.helpmanual.io/api/watch/#watchfiles.main.FileChange

    Args:
        changes (FileChange)
    """
    for each_change in changes:
        _, change_location = each_change
        logger.debug(f"Full change: {each_change}")
        print(f"Change detected at: {get_current_time()}")
        print(f"File(s) changed: {change_location}")
        print("Re-building...\n")
