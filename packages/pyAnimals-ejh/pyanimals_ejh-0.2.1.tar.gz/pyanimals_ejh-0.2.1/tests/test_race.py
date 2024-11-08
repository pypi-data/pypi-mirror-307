import pytest
from pyAnimals_ejh.pyAnimals_ejh import _get_animal_emoji, _update_position, _get_race_result, race

# tests for package function race
class TestRaceFunctions:
    # _get_animal_emoji #1: test that _get_animal_emoji() correctly handles invalid animal
    def test_emoji_invalid(self):
        actual = _get_animal_emoji("turtle")
        assert actual == "", "Expected _get_animal_emoji() to return an empty string on invalid animal"

    # _get_animal_emoji #2: test that _get_animal_emoji() returns string of length 1 for valid animal
    def test_emoji_type_len(self):
        actual = _get_animal_emoji("elephant")
        assert isinstance(actual, str) and len(actual) == 1, "Expected _get_animal_emoji() to return a string of length 1"
    
    # _get_animal_emoji #3: test that _get_animal_emoji() returns correct emoji
    def test_emoji_animal(self):
        expected_emojis = {
            "cat": "🐈",
            "bunny": "🐰",
            "elephant": "🐘",
            "rabbit": "🐇"
        }
        for animal, expected_emoji in expected_emojis.items():
            actual = _get_animal_emoji(animal)
            assert actual == expected_emoji, f"Expected emoji returned by _get_animal_emoji() to be {expected_emoji}. Instead, it returned '{actual}'"
    
    # _update_position #1: test that _update_position() returns an integer
    def test_position_type(self):
        actual = _update_position(0, 20)
        assert isinstance(actual, int), "Expected _update_position() to return an integer"
    
    # _update_position #2: test that _update_position() returns a value +1 or +2 from initial position
    def test_position_updated(self):
        init_pos = 5
        track_length = 20

        actual = _update_position(init_pos, track_length)
        assert init_pos + 1 <= actual <= init_pos + 2, f"Expected position returned by _update_position() to be +1 or +2 from initial position {init_pos}. Instead, it returned '{actual}'"

    # _update_position #3: test that _update_position() doesn't return value greater than track length
    def test_position_capped(self):
        actual = _update_position(20, 20)
        assert actual <= 20, f"Expected position returned by _update_position() to be less than or equal to track_length 20. Instead, it returned '{actual}'"
    
    # _get_race_result #1: test that _get_race_result() correctly shows animal as winner
    def test_result_animal_winner(self):
        animal = "elephant"
        player_pos = 18
        animal_pos = 20

        actual = _get_race_result(player_pos, animal_pos, animal)
        assert actual == f"{animal.title()} is the winner. Better luck next time 😅", f"Expected winner to be {animal}. Instead, it returned '{actual}'"

    # _get_race_result #2: test that _get_race_result() correctly shows player as winner
    def test_result_player_winner(self):
        animal = "elephant"
        player_pos = 20
        animal_pos = 18
        
        actual = _get_race_result(player_pos, animal_pos, animal)
        assert actual == "Congratulations! You are the winner 🏆", f"Expected winner to be player. Instead, it returned '{actual}'"

    # _get_race_result #3: test that _get_race_result() correctly shows tie
    def test_result_tie(self):
        animal = "elephant"
        player_pos = 20
        animal_pos = 20

        actual = _get_race_result(player_pos, animal_pos, animal)
        assert actual == "It's a tie!", f"Expected result to be a tie. Instead, it returned '{actual}'"

    # race #1: test that race() correctly handles invalid animal
    def test_race_invalid(self):
        actual = race("turtle")
        assert actual == "invalid animal", "Expected race() to return 'invalid animal' on invalid animal"

    # race #2: test that race() returns a list of length 2
    def test_race_positions(self):
        actual = race("elephant")
        assert isinstance(actual, list) and len(actual) == 2, "Expected race() to return a list of length 2"

    # race #3: test that at least one racer reaches the end of track by
    # the end of race()
    def test_race_completed(self):
        player_pos, animal_pos = race("elephant")
        assert player_pos == 20 or animal_pos == 20, f"Expected at least one racer to reach the end of track, position 20. However, by the end of race, the player was at '{player_pos}' and the animal was at '{animal_pos}'"
