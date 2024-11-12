import os.path

import pytest

from src.skautils.exehelper import CheckExeVersion

current_folder = os.path.dirname(os.path.abspath(__file__))
LINK_TO_TOML = os.path.join(current_folder, r"toml", r"versions.toml")
INCORRECT_LINK_TO_TOML = os.path.join(current_folder, r"toml", r"version.toml")
NAME_NOT_IN_FILE = ""
NAME_IN_FILE = "test_project"
NO_NAME_IN_FILE = "not_test_project"
REAL_VERSION = "0.0.1"
TEST_MAIL = "test@datacycle.ru"
NOT_REAL_VERSION = "0.0.2"


def test_do_nothing():
    CheckExeVersion(NAME_IN_FILE, REAL_VERSION, LINK_TO_TOML, current_folder, TEST_MAIL, True)

def test_no_toml_file():
    with pytest.raises(FileNotFoundError):
        CheckExeVersion(NAME_IN_FILE, REAL_VERSION, INCORRECT_LINK_TO_TOML, current_folder, TEST_MAIL, True)

def test_wrong_version():
    with pytest.raises(RuntimeError):
        CheckExeVersion(NAME_IN_FILE, NOT_REAL_VERSION, LINK_TO_TOML, current_folder, TEST_MAIL, True)

def test_no_exe_name():
    with pytest.raises(KeyError):
        CheckExeVersion(NO_NAME_IN_FILE, REAL_VERSION, LINK_TO_TOML, current_folder, TEST_MAIL, True)

if __name__ == "__main__":
    test_no_exe_name()
