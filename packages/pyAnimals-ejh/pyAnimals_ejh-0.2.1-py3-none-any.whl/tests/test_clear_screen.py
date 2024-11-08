# source for patch/mock_system: https://docs.python.org/3/library/unittest.mock.html

import pytest
import os
from unittest.mock import patch
from pyAnimals_ejh.pyAnimals_ejh import clearScreen

# test #1: check clearScreen() for Windows
@patch("os.system")
@patch("os.name", "nt")
def test_clear_screen_windows(mock_system):
    clearScreen()
    mock_system.assert_called_once_with('cls')

# test #2: check clearScreen() for non-Windows
@patch("os.system")
@patch("os.name", "posix")
def test_clear_screen_unix(mock_system):
    clearScreen()
    mock_system.assert_called_once_with('clear')

# test #3: check that clearScreen() is only called once
@patch("os.system")
def test_clear_screen_call_count(mock_system):
    clearScreen()
    mock_system.assert_called_once()