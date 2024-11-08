import pytest
from pyanimalconverter.convert import compare


def test_compare_identical_units():
    # Test with identical values and units
    result = compare(100, 100, "kg", "kg")
    assert result == 0

def test_compare_different_units():
    # Test with different but compatible units
    result = compare(1, 1, "kg", "lb") # 1kg should be approx 2.20462 lb
    assert result == 1

def test_compare_incompatible_units():
    # Test with incompatible units, expecting an error
    with pytest.raises(SystemExit): 
        compare(1, 1, "m", "s")




