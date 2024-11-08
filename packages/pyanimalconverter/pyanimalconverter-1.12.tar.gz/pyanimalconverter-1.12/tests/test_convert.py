import pytest
from pyanimalconverter import convert
import pint

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

def test_sanity_check():
    """
    Test debugging... making sure that we can run a simple test that always passes.
    Note the use of the example_fixture in the parameter list - any setup and teardown in that fixture will be run before and after this test function executes
    From the main project directory, run the `python3 -m pytest` command to run all tests.
    """
    expected = True  # the value we expect to be present
    actual = True  # the value we see in reality
    assert actual == expected, "Expected True to be equal to True!"

def test_another_true():
    assert True

def test_convert_diff_compatible_units():
    quantity = convert.convert(1, "km", "meter")
    assert quantity == 1000

def test_convert_incompatible_units():
    with pytest.raises(SystemExit):    # TODO: figure out how incompatible conversion error or trouble parsing error
        quantity = convert.convert(1, "km", "lb")

def test_convert_same_units():
    quantity = convert.convert(1, "km", "km")
    assert quantity == 1

