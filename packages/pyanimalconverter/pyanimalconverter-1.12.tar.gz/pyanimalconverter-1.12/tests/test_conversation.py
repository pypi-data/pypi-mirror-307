import pytest, sys
from pyanimalconverter.conversation import *
from io import StringIO 

##custom fixture for input files
#@pytest.fixture
#def getInput():
#    file = open("convInput.txt")
#    return file.read()

#def test_unit_error(capfd, getInput):
#    sys.stdin = getInput
#    with pytest.raises(SystemExit):
#        askAnimal()
#    result = capfd.readouterr()
#    assert result == "Unit is not valid!\n"

def test_talk():
    # test the talk function for correct implementation

    result = talk("Hello!", "Hi!")

    assert "Hello!" in result # check if hello is included
    assert "Hi!" not in result # ensure left text bubble is not in result
    assert "_" in result  # check if speech bubble lines are included

def test_navigate_exit(capfd):
    # test the program exits normally when given DONE input
    sys.stdin = StringIO("DONE\n") # simulate user input with done and newline(enter)

    askAnimal()
    result = capfd.readouterr().out
    assert "Ok, bye. Ribbit." in result
    