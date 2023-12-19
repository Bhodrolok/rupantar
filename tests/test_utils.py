from os import getcwd
from pathlib import Path
from rupantar.sohoj.utils import resolve_path
import pytest

class TestBuilder:    
    @pytest.mark.skip(reason="Not complete")
    def test_resolve_path_single_nonexistent_path(self, setup_test_directory):
        with pytest.raises(FileNotFoundError) as exc_info:
            _ = resolve_path("gibberish")

        assert exc_info.type is FileNotFoundError

    def test_resolve_path_good_path_single_arg(self, setup_test_directory):
        good_path = Path("existing", "directory")
        good_path.mkdir(parents=True)
        input_fp_str = "existing/directory"
        assert resolve_path(input_fp_str) == good_path.resolve()
    
    def test_resolve_path_good_path_multiple_args(self, setup_test_directory):
        good_path = Path("i", "do", "exist")
        good_path.mkdir(parents=True)
        assert resolve_path("i", "do", "exist") == good_path.resolve()

    def test_resolve_path_bad_path_single_arg(self, setup_test_directory):
        bad_path = Path(getcwd(), "i", "do", "not", "exist")
        assert resolve_path(bad_path) == bad_path