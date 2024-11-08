import argparse
import sys
from pint import UnitRegistry
from collections import defaultdict

ureg = UnitRegistry()
ureg.formatter.default_format = '.3f'


def print_units():
    ureg = UnitRegistry()
    # Dictionary to hold units by category
    categories = defaultdict(list)

    # Group units by their dimensionality
    for unit in ureg._units:
        try:
            unit_obj = ureg[unit]
            dimension = str(unit_obj.dimensionality)  # Get the dimension as a string
            categories[dimension].append(unit)  # Append the unit to the appropriate category
        except:
            pass

    relevant_cats = ['[length]', '[mass]', '[time]', '[temperature]']
    # Display the units by category
    print("Units by Category:\n")
    for category, units in sorted(categories.items()):
        if category in relevant_cats:
            print(f"{category}:")
            for unit in sorted(units):
                print(f"  - {unit} ({ureg[unit]})")
            print()  # Newline for better readability

def compare(num1, num2, unit1, unit2):
    """
    Compares two quantities and returns an integer denoting if first value is greater than/equal to/smaller than the second value

    Args:
        num1 (int): First value
        num2 (int): Second value
        unit1 (str): Unit of first value
        unit2 (str): Unit of second value

    Returns:
        int: 1 if first value is greater than second, 0 if equal, and -1 if first smaller than second.
    """
    try:
        unit1_registry = ureg.parse_expression(unit1)
        unit2_registry = ureg.parse_expression(unit2)
    except Exception as e:
        print(f'Error parsing unit(s): {e}', file=sys.stderr)
        raise SystemExit(1)
    if not unit1_registry.is_compatible_with(unit2_registry):   # if the 2 units being compared aren't compatible (e.g. lbs with km)
        print(f"Invalid comparison {unit1_registry.units} with {unit2_registry.units}", file=sys.stderr)
        raise SystemExit(2)
    quant1 = convert(num1, unit1, unit1)
    quant2 = convert(num2, unit2, unit1)
    if quant1 > quant2:
        return 1
    elif quant1 == quant2:
        return 0
    else: # if quant2 is greater than quant1
        return -1
    

def convert(num1, from_unit, to_unit):
    try:
        from_registry = ureg.parse_expression(from_unit)
        to_registry = ureg.parse_expression(to_unit)
    except Exception as e:
        print(f'Error parsing unit(s): {e}', file=sys.stderr)
        raise SystemExit(1)
    if not from_registry.is_compatible_with(to_registry):
        print(f"Invalid conversion {from_registry.units} to {to_registry.units}", file=sys.stderr)
        raise SystemExit(2)

    Q_ = ureg.Quantity
    quant = Q_(num1, from_registry)
    quant = quant.to(to_registry)
    return float(quant.magnitude)

# parses the arguments of the command
def parse_main_args(args):
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="operation", required=True)

    # Parser to accept help command
    help_parser = subparsers.add_parser("help", help="Show verbose help instructions")
    help_units_parser = help_parser.add_subparsers(dest="help_subcommand")
    units_parser = help_units_parser.add_parser("units", help="Display all units")

    # Write the flags for the compare function
    compare_parser = subparsers.add_parser("compare", help="Compare two values by units")
    # Take arguments for 2 numbers and 2 units
    compare_parser.add_argument(
        'num1',  
        type=float, 
        metavar="num1",
        help="Value of first unit to compare",
    )
    compare_parser.add_argument(
        'num2', 
        type=float, 
        metavar="num2",
        help="Value of second unit to compare",
    )
    compare_parser.add_argument(
        'unit1',
        metavar="unit1",
        help="Unit of first number (run `help` to see units)",
    )
    compare_parser.add_argument(
        'unit2',
        metavar="unit2",
        help="Unit of second number (run `help` to see units)",
    )

    # Writing flags for the convert function
    convert_parser = subparsers.add_parser("convert", help="Convert a value to another unit")
    # Takes in one number and a from_unit and to_unit
    convert_parser.add_argument(
        'num1',
        type=float,
        help="Value of unit to convert",
    )
    convert_parser.add_argument(
        'from_unit',
        metavar='from_unit',
        help="Unit given input value",
    )
    convert_parser.add_argument(
        'to_unit',
        metavar='to_unit',
        help="Unit of desired output value",
    )

    args = parser.parse_args(args)

    return args
