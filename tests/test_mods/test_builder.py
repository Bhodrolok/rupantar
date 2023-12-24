from rupantar.sohoj.builder import build_project, md_to_str, parse_md
from rupantar.sohoj.creator import create_project
import pytest


class TestBuilder:
    @pytest.mark.skip(reason="Not complete")
    def test_build_project_nonexistent_rupantar_project_folder(
        self, setup_test_directory
    ):
        nonexistent_dir = "abcd"
        with pytest.raises(FileNotFoundError, match="find given rupantar"):
            build_project(nonexistent_dir, None)

    @pytest.mark.skip(reason="Not complete")
    def test_build_project_nonexistent_config_file(self, setup_test_directory):
        create_project("yo", [None, None, None])
        nonexistent_config_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="find given config"):
            build_project("yo", nonexistent_config_file)

    @pytest.mark.skip(reason="Not complete")
    def test_md_to_str_nonexistent_markdown_file(self, setup_test_directory):
        nonexistent_markdown_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="File not found"):
            md_to_str(nonexistent_markdown_file)

    @pytest.mark.skip(reason="Not complete")
    def test_parse_md_nonexistent_markdown_file(self, setup_test_directory):
        nonexistent_markdown_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="File not found"):
            parse_md(nonexistent_markdown_file)
