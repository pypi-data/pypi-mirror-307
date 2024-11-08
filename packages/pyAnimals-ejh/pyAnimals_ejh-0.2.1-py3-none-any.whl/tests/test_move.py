# source for patch/mock_system: https://docs.python.org/3/library/unittest.mock.html

from unittest.mock import patch
import pytest
from pyAnimals_ejh.pyAnimals_ejh import move

# test #1: handles valid animals
@pytest.mark.parametrize("validAnimal", ["cat", "bunny", "elephant", "rabbit"])
def test_valid_animal(validAnimal):
    # check that there aren't any errors for valid animal options
    move(validAnimal)

# test #2: screen is cleared
@pytest.mark.parametrize("animal", ["cat", "bunny", "elephant", "rabbit"])
@patch("pyanimals.main.clearScreen")
def test_clear_screen(mockClearScreen, animal):
    move(animal)
    # check that clearScreen is called the expected number of times
    assert mockClearScreen.call_count == 25

# test #3: animal didn't move off screen
@pytest.mark.parametrize("animal", ["cat", "bunny", "elephant", "rabbit"])
@patch("pyanimals.main.clearScreen")
@patch("builtins.print")
def test_in_bounds(mockInBounds, mockClearScreen, animal):
    screenWidth = 80
    move(animal)
        
    for call in mockInBounds.call_args_list:
        printedText = call[0][0]
            
        if printedText.strip():
            leadingSpaces = len(printedText) - len(printedText.lstrip())
            # check that leading spaces + animal width <= screen width
            assert leadingSpaces + len(printedText.lstrip().splitlines()[0]) <= screenWidth, \
                    "Animal moved off screen"