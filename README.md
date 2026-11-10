# `memorymanagement`
Provides memory management support.

The only Python implementation currently supported is the **CPython** interpreter.
The rest are untested.
## Table of Contents
* [Modules](#modules)
    * [`cleaning`](#cleaning)
    * [`pointers`](#pointers)
        * [Class `Pointer`](#class-pointer)
        * [Decorator `pointerize`](#decorator-pointerize)
* [Installation](#installation)
* [Usage](#usage)
    * [Class `Cleaner`](#class-cleaner)
    * [Class `Pointer`](#class-pointer-1)
    * [Decorator `pointerize`](#decorator-pointerize-1)
* [Contribution](#contribution)
## Modules
### `cleaning`
Provides the class `Cleaner`, which allows you to flag references stored in memory to eventually erase them.
It is also possible to modify the list of flagged references through its methods.
### `pointers`
Provides a safe implementation of pointers for Python.
#### Class `Pointer`
The pointer itself. Imitates the behaviour of C pointers.
`Pointer` points to a **reference**, or to every reference at the same time, not to an object stored in memory.
#### Decorator `pointerize`
Allows functions to receive pointers instead of values.
## Installation
You can install the development version of the `memorymanagement` package from [**TestPyPI**](https://test.pypi.org/project/memorymanagement/) as follows:
```powershell
pip install --index-url https://test.pypi.org/simple/ memorymanagement
```
For TestPyPI version, `--no-deps` option is not needed because it has no dependencies.
## Usage
### Class `Cleaner`
```py
# Imports
# Make your imports here
from memorymanagement import Cleaner # Importing class Cleaner
```
Right after imports are done, I recommend to initialize an instance of class `Cleaner`, so no arguments are needed. This is the optimal use this class was designed for.
```py
# Initialize cleaner object
cleaner=Cleaner()
```
Create, for example, these variables (can be global or local):
```py
value_1=10
value_2=50
value_3=100
```
Update the list of flagged references like one of the following:
* Including all new variables:
    ```py
    cleaner.update()
    print(cleaner.flagged)
    ```
    Output:
    ```sh
    ["value_1","value_2","value_3"]
    ```
* Excluding some variables:
    ```py
    cleaner.update(exclude="value_2")
    print(cleaner.flagged)
    ```
    Output:
    ```sh
    ["value_1","value_3"]
    ```
    ---
    ```py
    cleaner.update(exclude=["value_2","value_3"])
    print(cleaner.flagged)
    ```
    Output:
    ```sh
    ["value_1"]
    ```
* Include again some variables:

    After having excluded some variables
    ```py
    cleaner.update(exclude=["value_2","value_3"])
    ```
    You can reintroduce them
    ```py
    # Create a new variable and update
    value_4=150
    cleaner.update(exclude="value_4",include="value_2") # "include" can also be a list of strings
    print(cleaner.flagged)
    ```
    Output:
    ```sh
    ["value_1","value_2"]
    ```
You can also directly include or exclude references like so:
```py
cleaner.exclude(<name_var_1>,<name_var_2>,...)
```
```py
cleaner.include(<name_var_1>,<name_var_2>,...)
```
To flag all the excluded variables at once, you can use:
```py
cleaner.include_all(exclude=[<var_1>,<var_2>,...]) # exclude: optional keyword argument, accepts strings and iterables of strings
```
You can also exclude all the flagged variables like so:
```py
cleaner.exclude_all(include=[<var_1>,<var_2>,...]) # include: optional keyword argument, accepts strings and iterables of strings
```
And reset the cleaner's parameters like so:
```py
cleaner.purge()
```
### Class `Pointer`
Example:
```py
# Import the `Pointer` class
from memorymanagement import Pointer
# Create a pointer to a variable
p=Pointer(x:=10).select_ref() # So it points to "x" reference, instead of every reference. Also `p=Pointer(x:=10,"x")`
# Print variable and pointer's value
print(f"a:\n{x}\n\nPointer:\n{p.value}\n\n")
# Set variable to 20
x=20
# Print variable and pointer's value
print(f"a:\n{x}\n\nPointer:\n{p.value}\n\n")
# Set variable to 10
x=10
# Set pointer's value to 20
p.value=20
# Print variable and pointer's value
print(f"a:\n{x}\n\nPointer:\n{p.value}")
```
Output:
```sh
a:
10

Pointer:
10


a:
20

Pointer:
20


a:
20

Pointer:
20
```
### Decorator `pointerize`
Example:
```py
# Import pointerize decorator
from memorymanagement import pointerize
# Define and decorate `myFunction`
@pointerize
def myFunction(value:int):
    # Set the value to 20
    value=20
# Set a new variable to a value (10 in this case)
x=10
# Print variable
print(f"Value: {x}")
# Execute the function using a pointer to `x`
myFunction(Pointer(x))
# Print `x` variable
print(f"Value: {x}")
```
Output:
```sh
Value: 10
Value: 20
```
## Contribution
To contribute to this project fork this repository and clone your fork. Pull requests will be revised by the owner before being accepted or rejected.

There are two branches:
* [**PyPI**](https://github.com/Ricardo-Werner-Rivas/memorymanagement/tree/PyPI): the main branch, for releases.
* [**TestPyPI**](https://github.com/Ricardo-Werner-Rivas/memorymanagement/tree/TestPyPI): for pre-releases or development versions.

Pull requests from **TestPyPI** to **PyPI** will only be done by the owner when a new release is ready.