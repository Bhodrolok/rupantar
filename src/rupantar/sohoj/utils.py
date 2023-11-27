from time import perf_counter
from logging import getLogger

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
