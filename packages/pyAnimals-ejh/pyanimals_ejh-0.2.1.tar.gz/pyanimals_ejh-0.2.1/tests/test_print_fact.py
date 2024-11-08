import pytest
import random
from pyAnimals_ejh.pyAnimals_ejh import print_fact
# Test 1: Ensures print_fact returns a fact from the list for a valid animal
def test_print_fact_valid_animal(capsys):
    test_animal = "cat"
    valid_facts = [
        "Did you know domestic cats can run up to 30 mph in short bursts?",
        "Did you know a group of cats is called a clowder?",
        "Did you know cats sleep for about 13-16 hours a day?"
    ]
    print_fact(test_animal)
    captured = capsys.readouterr()
    fact_output = captured.out.replace("Random Fact: ", "").strip()
    assert fact_output in valid_facts

# Test 2: Ensures print_fact is only printing one fact
def test_print_fact_one_fact_only(capsys):
    test_animal = "elephant"
    print_fact(test_animal)
    captured = capsys.readouterr()
    assert captured.out.count("Random Fact:") == 1

# Test 3: Ensure thats the print fact raises a value error and prints out error message for invalid animnal
def test_print_fact_invalid_animal():
    with pytest.raises(ValueError, match="No facts available for 'penguin'"):
        print_fact("penguin") 

