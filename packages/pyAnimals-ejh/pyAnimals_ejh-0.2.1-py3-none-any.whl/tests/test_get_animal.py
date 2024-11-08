from textwrap import dedent
import pytest
from pyAnimals_ejh.pyAnimals_ejh import get_animal

class TestGetAnimalFunction:
    # tests 1-4: check that function gets correct ASCII art for valid animals
    # test 1
    
    def test_cat_ASCII(self):
        actual = get_animal("cat")

        expected = dedent(r"""
          _
         | |__               /\__/\
         |__  |             ( o . o) 
            | |_____________ > ^ <
            |                  /
             /  ___________   /
            /_/             \_\
        """)
        
        assert actual == expected, "Test failed: cat ASCII art not returned correctly."

    # test 2
    def test_bunny_ASCII(self):
        actual = get_animal("bunny")

        expected = dedent(r"""
              () ()
             ( 0x0 )
              (   ) 
              (")(")
        """)
        
        assert actual == expected, "Test failed: bunny ASCII art not returned correctly."

    # test 3
    def test_elephant_ASCII(self):
        actual = get_animal("elephant")
        
        expected = dedent(r"""
                 ____
        ________(     \––-     ♥
     /''         \ ,_ ,   • \  _
    /  |               \___ U /
    ^   \    ______    | 
        |_,,|      |_,,|
        """)
        
        assert actual == expected, "Test failed: elephant ASCII art not returned correctly."

    # test 4
    def test_rabbit_ASCII(self):
        actual = get_animal("rabbit")
        
        expected = dedent(r"""
            ,\\
              \\\,_
               \` ,\\
          __,.-" =__)
        ."        )
     ,_/   ,    \/\_
     \_|    )_-\ \_-`
        `-----` `--`
        """)
        
        assert actual == expected, "Test failed: rabbit ASCII art not returned correctly."
    
    # test 5: check that function handles invalid animals
    def test_invalid_animal(self):
        result = get_animal("dog")
        assert result == "", "Test failed: invalid animal should return an empty string."
