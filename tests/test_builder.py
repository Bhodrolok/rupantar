from rupantar.sohoj.builder import build_project, md_to_str, parse_md
from rupantar.sohoj.creator import create_project
from os import chdir, getcwd
from shutil import rmtree
import pytest


class TestBuilder:
    @pytest.fixture
    def setup_directory(self, tmp_path):
        print("\nSetting up test resources...")
        # Fix for PermissionError: [WinError 32] The process cannot access the file because it is being used by another process
        og_dir = getcwd()
        chdir(tmp_path)
        print(f"Currently the testing directory is: {getcwd()}")
        yield
        print("\nTearing down test resources...")
        chdir(og_dir)
        rmtree(tmp_path)

    # @pytest.mark.skip(reason="Not complete")

    def test_build_project_nonexistent_rupantar_project_folder(self, setup_directory):
        nonexistent_dir = "abcd"
        with pytest.raises(FileNotFoundError, match="find given rupantar"):
            build_project(nonexistent_dir, None)

    def test_build_project_nonexistent_config_file(self, setup_directory):
        create_project("yo", [None, None, None])
        nonexistent_config_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="find given config"):
            build_project("yo", nonexistent_config_file)

    def test_md_to_str_nonexistent_markdown_file(self, setup_directory):
        nonexistent_markdown_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="File not found"):
            md_to_str(nonexistent_markdown_file)

    def test_parse_md_nonexistent_markdown_file(self, setup_directory):
        nonexistent_markdown_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="File not found"):
            parse_md(nonexistent_markdown_file)
