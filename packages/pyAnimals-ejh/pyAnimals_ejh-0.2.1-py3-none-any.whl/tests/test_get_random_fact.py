import pytest
import random
from pyAnimals_ejh.pyAnimals_ejh import get_random_fact
# Test 1: Ensures that the random fact returned is for the specific input animal from the list of facts
def test_get_random_fact_validAnimal():
    testAnimal = "cat"
    testFacts = [
        "Did you know domestic cats can run up to 30 mph in short bursts?",
        "Did you know a group of cats is called a clowder?",
        "Did you know cats sleep for about 13-16 hours a day?"
    ]
    factOutput = get_random_fact(testAnimal)
    assert factOutput in testFacts

# Test 2: Invalid animal raises value error
def test_get_random_fact_invalidAnimal():
    with pytest.raises(ValueError, match = "No facts available for 'dolphin'"):
        get_random_fact("dolphin")

# Test 3: No input raises raises value error
def test_get_random_fact_noAnimal():
    with pytest.raises(ValueError, match = "No facts available for ''"):
        get_random_fact("")  # No input

# Test 4: Ensures only one fact is returned
def test_get_random_fact_one_fact():
    test_animal = "elephant"
    fact_output = get_random_fact(test_animal)
    assert isinstance(fact_output, str)