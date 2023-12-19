import pytest
from os import getcwd, chdir
from shutil import rmtree

# Ref: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
@pytest.fixture
def setup_test_directory(tmp_path):
    """Fixture to set up a temporary directory for testing."""
    print("\nSetting up test resources...")
    og_dir = getcwd()
    chdir(tmp_path)
    print(f"Current testing directory: {getcwd()}")
    yield
    print("\nTearing down test resources...")
    chdir(og_dir)
    rmtree(tmp_path)
    print("Finish tearing down test resources")
