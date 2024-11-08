import pytest
from pyAnimals_ejh.pyAnimals_ejh import randMessage
from unittest.mock import patch

#test 1 make sure a random message printed is for the correct animal
@pytest.mark.parametrize("animal, expected", [
    ("cat", ["Meow Meow", "Hiss, Hiss", "Purr Purr", "I am hungry for fish!"]),
    ("bunny", ["Hop Hop", "Munch Munch", "I am Hungry for Hay"]),
    ("elephant", ["Trumpet Trumpet", "Snort Snort", "Theres Dust in my trunk.", "I am Hungry for Grass.", "Lets go in the Water", "Rumble Rumble"]),
    ("dog", ["Woof Woof", "I am hungry for socks!", "I am hungry for chicken!", "Lets play fetch!"]),
    ("rabbit", ["Hop Hop", "Nibble Nibble", "I am hungry for carrots!"])
])
def test_randMessage_MessageCheck(animal, expected, capfd):
    randMessage(animal)
    output = capfd.readouterr().out.strip()  
    print(f"Output for {animal}: {output}")  
    assert any(f"{animal} says: {messageChoice}"in output for messageChoice in expected)


#test 2 make sure the error message is outputted when the wrong animal is inputted 
def test_randMessageErrorMessage (capfd):
    randMessage("Panda")
    output=capfd.readouterr().out
    assert "Unknown Animal. Message can't be printed try a different animal." in output

#test 3 tests when nothign is passed into the randMessage function
def test_randMessage_noneAnimal(capfd):
    randMessage(None)  
    output = capfd.readouterr().out
    assert "Unknown Animal. Message can't be printed try a different animal." in output


