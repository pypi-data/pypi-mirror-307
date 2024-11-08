import pytest
from pyAnimals_ejh.pyAnimals_ejh import get_random_message

#test 1 makes sure the logic works gets random message from the list of messsages only
def test_get_random_message_validMessage():
    testMessages=["hi1","hi2","hi3"]
    messsageOutput=get_random_message(testMessages)
    assert messsageOutput in testMessages

#test 2 makes sure there is an error when there is an empty list
def test_get_random_message_emptyArg():
    with pytest.raises(IndexError):
        get_random_message([])
    

#test 3 makes sure only one message is printed
def test_get_random_message_oneMessageOnly():
    testMessages=["hi1","hi2","hi3"]
    messsageOutput=get_random_message(testMessages)
    assert messsageOutput in testMessages
