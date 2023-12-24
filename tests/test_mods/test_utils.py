from pathlib import Path
import re
import time
from datetime import datetime
from rupantar.sohoj.utils import (
    resolve_path,
    validate_network_address,
    get_current_time,
    get_func_exec_time,
)
import pytest


class TestUtils:
    # resolve_path()

    def test_resolve_path_good_path_single_arg(self, setup_test_directory):
        good_path = Path("existing", "directory")
        good_path.mkdir(parents=True)
        input_fp_str = "existing/directory"
        assert resolve_path(input_fp_str, strict=True) == good_path.resolve()

    def test_resolve_path_good_path_multiple_args(self, setup_test_directory):
        good_path = Path("i", "do", "exist")
        good_path.mkdir(parents=True)
        assert resolve_path("i", "do", "exist", strict=True) == good_path.resolve()

    def test_resolve_path_bad_path_single_arg(self, setup_test_directory):
        bad_path = Path("i", "do", "not", "exist")
        # Also works with a regular str instead of a Path
        with pytest.raises(FileNotFoundError):
            _ = resolve_path(bad_path, strict=True)

    def test_resolve_path_bad_path_multiple_args(self, setup_test_directory):
        with pytest.raises(FileNotFoundError):
            _ = resolve_path("totally", "real", "path", "trust", "me!", strict=True)

    # validate_network_address()

    def test_validate_network_address_invalid_linklocal_min(self, setup_test_directory):
        invalid_ip_linklocal = "169.254.1.0"
        assert (
            validate_network_address(invalid_ip_linklocal) is False
        ), f"{invalid_ip_linklocal} is a link-local address, not valid"

    def test_validate_network_address_invalid_linklocal_max(self, setup_test_directory):
        invalid_ip_linklocal = "169.254.254.255"
        assert (
            validate_network_address(invalid_ip_linklocal) is False
        ), f"{invalid_ip_linklocal} is a link-local address, not valid"

    def test_validate_network_address_invalid_multicast_min(self, setup_test_directory):
        invalid_ip_multicast = "224.0.0.0"
        assert (
            validate_network_address(invalid_ip_multicast) is False
        ), f"{invalid_ip_multicast} is a multicast address, not valid"

    def test_validate_network_address_invalid_multicast_max(self, setup_test_directory):
        invalid_ip_multicast = "239.255.255.255"
        assert (
            validate_network_address(invalid_ip_multicast) is False
        ), f"{invalid_ip_multicast} is a multicast address, not valid"

    def test_validate_network_address_invalid_notipatall(self, setup_test_directory):
        invalid_ip = "https://lobste.rs"
        assert (
            validate_network_address(invalid_ip) is False
        ), f"{invalid_ip} is not a valid IP address"

    def test_validate_network_address_valid_loopback(self, setup_test_directory):
        valid_ip = "127.0.0.1"
        assert (
            validate_network_address(valid_ip) is True
        ), f"{valid_ip} is a valid IP address"

    def test_validate_network_address_valid_ip(self, setup_test_directory):
        valid_ip = "9.255.255.255"
        assert (
            validate_network_address(valid_ip) is True
        ), f"{valid_ip} is a valid IP address"

    # get_current_time()

    def test_get_current_time_format(self, setup_test_directory):
        current_time = get_current_time()
        expected_fmt = "%Y-%m-%d %H:%M:%S"
        # i.e. === YYYY-MM-DD HH:MM:SS ===
        assert re.match(
            r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", current_time
        ), f"Expected format of time to be: {expected_fmt}"

    def test_get_current_time(self, setup_test_directory):
        current_time = get_current_time()
        now = datetime.now()
        expected_time = now.strftime("%Y-%m-%d %H:%M:%S")
        assert current_time == expected_time, f"Expected time: {expected_time}"

    def test_get_current_time_multiple_calls(self, setup_test_directory):
        time_a = get_current_time()
        time.sleep(1)
        time_b = get_current_time()
        assert time_a != time_b, "Expected different time values on separate calls"

    # get_func_exec_time()

    @pytest.mark.skip(reason="incomplete")
    def test_func_exec_time_get_func_exec_time(self, setup_test_directory, mocker):
        @get_func_exec_time
        def just_sleep():
            time.sleep(1)

        # TODO
