from rupantar.sohoj.builder import build_project, md_to_str, parse_md
from rupantar.sohoj.creator import create_project
import os
import pytest


class TestBuilder:
    # @pytest.mark.skip(reason="Not complete")
    def test_builder_nonexistent_rupantar_project_folder(self, tmp_path):
        os.chdir(tmp_path)
        nonexistent_dir = "abcd"
        with pytest.raises(FileNotFoundError, match="find given rupantar"):
            build_project(nonexistent_dir, None)

    def test_builder_nonexistent_config_file(self, tmp_path):
        os.chdir(tmp_path)
        create_project("yo", [None, None, None])
        nonexistent_config_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError, match="find given config"):
            build_project("yo", nonexistent_config_file)

    def test_builder_nonexistent_config_file_2(self, tmp_path):
        os.chdir(tmp_path)
        create_project("yoyo", [None, None, None])
        false_config_file = "xyz"
        # with pytest.raises(FileNotFoundError) as exc_info:
        with pytest.raises(FileNotFoundError, match="not find given config"):
            build_project("yoyo", false_config_file)

        # assert exc_info.type is FileNotFoundError
        # assert exc_info.value.args[0] == "Could not find given config file."

    def test_md_to_str_nonexistent_markdown_file(self, tmp_path):
        os.chdir(tmp_path)
        nonexistent_markdown_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError) as exc_info:
            md_to_str(nonexistent_markdown_file)

        assert exc_info.type is FileNotFoundError
        assert exc_info.value.args[0] == f"File not found: {nonexistent_markdown_file}"

    def test_parse_md_nonexistent_markdown_file(self, tmp_path):
        os.chdir(tmp_path)
        nonexistent_markdown_file = "abcd.gibberishformat"
        with pytest.raises(FileNotFoundError) as exc_info:
            parse_md(nonexistent_markdown_file)

        assert exc_info.type is FileNotFoundError
        assert exc_info.value.args[0] == f"File not found: {nonexistent_markdown_file}"
