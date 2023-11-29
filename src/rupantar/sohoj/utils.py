from time import perf_counter
from logging import getLogger
from ipaddress import ip_address

logger = getLogger()


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
        logger.debug(
            f"{function.__name__} was completed in: {perf_counter() - start_time} seconds"
        )
        return og_func_return

    return wrap


def validate_network_address(interface_address: str) -> bool:
    """Validate a given network address to check if it is a valid IP address.

    Link-local and multicast addresses are considered to be invalid.

    Note:
        The link-local addresses = reserved range of 169.254.1.0 to 169.254.254.255, as per the IETF.

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
