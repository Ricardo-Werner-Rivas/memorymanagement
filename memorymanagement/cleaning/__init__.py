"""
Implements the class `Cleaner` to keep track of the references and erase them easily.
## Overview
Initialize a `Cleaner` object:
```
# Default arguments' values
cleaner=Cleaner(
    not_delete:list[str]=list(vars(modules["main"])), # List of global variables at that moment (modules comes from sys library)
    excluded:list[str]=[], # Empty list to be modified later if you need
    flagged:list[str]=[] # List of references to undo
)
```
Now `cleaner` has the following attributes:
```
cleaner._not_delete=list(vars(modules["main"])) # At initialization moment
cleaner._excluded=[] # Wasn't asked to exclude any reference.
cleaner._flagged=[] # Wasn't asked to include any reference.
```
To automatically include all the new references, use the `.update()` method:
```
x=10
y="Hello world"
z=f"Hello Python for time number {x}"
# Default arguments' values
cleaner.update(
    exclude:str|list[str]|tuple[str]|None=None, # Excludes flagged or yet not created references from the process
    include:str|list[str]|tuple[str]|None=None # Includes references into the process
)
print(cleaner)
```
The cell above prints the following (via `__str__` method):
```
Flagged: ["x","y","z"]

Excluded: []

Not delete: <list(vars(modules["main"]))> # Unchanged since initialization
```
To delete these variables from memory, use the `clean()` method:
```
# Cleans memory
cleaner.clean()

# Print again the `Cleaner` instance
print(cleaner)
```
The output will now be:
```
Flagged: []

Excluded: []

Not delete: <list(vars(modules["main"]))> # Unchanged since initialization
```
And if we print the global variables:
```
print(list(globals()))
```
The output will be:
```
["Cleaner","cleaner"]
```
"""
# Imports
from .core import Cleaner