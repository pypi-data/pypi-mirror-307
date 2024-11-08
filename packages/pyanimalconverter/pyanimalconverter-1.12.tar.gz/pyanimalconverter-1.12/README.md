# Pyanimalconverter Package

![Tests](https://github.com/software-students-fall2024/3-python-package-kapow/actions/workflows/build.yaml/badge.svg)

## Description
Our package, pyanimalconverter, helps you to fullfill all of your unit conversion needs in convenient and enjoyable ways. You can simply get the conversions, compare two quantities in different units, or even find the minimum or maximum of a list. In addition, you can even choose to perform these conversions and comparisons in a conversation with some animal friends.

### Example

[Link to example program in repository.](https://github.com/software-students-fall2024/3-python-package-kapow/blob/main/example.py)

### Link to PyPI

Link here coming soon

## Instructions for Importing

To import, please install the package with `pip install pyanimalconverter`. Then you can include `import pyanimalconverter` at the top of your code to use. 

## Instructions for Setting Up

To set up the package for contribution, the virtual environment can be set up by simply using `pipenv` with the dependencies listed in the Pipfile. Then, to build, you can use `py -m build` with the file pyproject.toml in the directory.

## Teammates

- David Jimenez, [Github](https://github.com/drj8812)
- Sean Lee, [Github](https://github.com/jseanlee)
- Madison Phung, [Github](https://github.com/mkphung29)
- Stephen Spencer-Wong, [Github](https://github.com/StephenS2021)
- William Xie, [Github](https://github.com/seeyeh)

## How to Use 

There are three ways to use the package: through the command line, via importing, and in conversation with animals. Before proceeding with either of these, please install the package with `pip install pyanimalconverter` as noted above.

### Importing

One way to use the package is by importing it, simply including `import pyanimalconverter` at the top of your code as mentioned above. From there can you call methods from `pyanimalconverter.convert`, `pyanimalconverter.conversation`, and `pyanimalconverter.minmax`. If you know you only want to use a certain function (like convert for example), you can use `import pyanimalcoverter.convert as convert`, then simply call `convert.convert()` with required parameters.

### Conversation

Another way in which the application can be used is in conversation with a frog friend, who can help you convert as well as compare two quantities. To enter the conversation, simply include `import pyanimalcoverter.conversation as conversation` and call `conversation.askAnimal()` to start an interactive conversation with your frog friend. There, you will be asked whether you want to convert or compare as well the specifics of the operation, and your frog friend will give you the results. You can continue this conversation as long as you like.

### Command Line

You can also use pyanimalconverter on the command line if you want to quickly use the convert or compare functions. To use convert you can call: `pyanimalconverter convert num from_unit to_unit` or more concretely: `pyanimalconverter convert 1 ft in` which will print out 12.

To use compare you can call: `pyanimalconverter compare num1 num2 unit1 unit2`.
