# `memorymanagement`
Provides memory management support.

The only Python implementation currently supported is the one made by the **CPython** team.
The rest remain untested.
## Modules
### `cleaning`
Provides the class `Cleaner`, which allows you to flag references stored in memory to eventually erase them.
It is also possible to modify the list of flagged references through its methods.
### `pointers`
Provides a safe implementation of pointers for Python.
#### Class `Pointer`
The pointer itself. Imitates the behaviour of C pointers. `Pointer` points to a **reference**, not to an object stored in memory.
#### Decorator `pointerize`
Allows functions to receive pointers instead of values.
## Installation
You can install the `memorymanagement` package from **PyPI** as follows:
```powershell
pip install memorymanagement
```
## How to use
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
Create, for example, these global variables:
```py
value_1=10
value_2=50
value_3=100
```
Update the list of flagged references like one of the following:
* Including all new global variables:
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
from memorymanagement import Pointer
a=10
x=Pointer(a)
print(f"a:\n{a}\n\nPointer:\n{x.value}\n\n")
a=20
print(f"a:\n{a}\n\nPointer:\n{x.value}\n\n")
a=10
x.value=20
print(f"a:\n{a}\n\nPointer:\n{x.value}")
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
from memorymanagement import pointerize
@pointerize
def myFunction(value:int):
    value=20
    return
a=10
print(f"Value: {a}")
myFunction(Pointer(a))
print(f"Value: {a}")
```
Output:
```sh
Value: 10
Value: 20

```
## Contribution
To contribute to this project fork this repository and clone your fork. Pull requests will be revised by the owner before being accepted or rejected.

There are two branches:
* **PyPI**: the main branch, for releases.
* **TestPyPI**: for pre-releases or development versions.

Pull requests from TestPyPI to PyPI will only be done by the owner when a new release is ready.

### Branch merging
To merge branches properly with PyPI branch in your cloned repository, you will need to have the `.gitattributes` file in the PyPI branch and execute the following commands, while in repo directory, in your PowerShell:
```powershell
git config merge.keepPyPIFiles.name "Keep README.md and setup.cfg from PyPI branch on merge"
git config merge.keepPyPIFiles.driver "bash -c 'cp $(git rev-parse --show-toplevel)/$3 $2'"
```
This way, `README.md` and `setup.cfg` files will not be overwritten in the PyPI branch.