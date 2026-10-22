"""
Provides memory management support.

---
## Module `cleaning`
The class `Cleaner` flags the global references to erase them when commanded.
References can be chosen to be excluded or included again in the process.
## Module `pointers`
A safe implementation of pointers for Python. Written in pure Python, this module includes two things:
### 1. Class `Pointer`
Creates a `Pointer` instance. These pointers point to a reference, not to an object in memory.
It is also able to point to every reference pointing to its value, as if it was pointing to the object's memory address.
If value for the reference(s) is changed, so is the pointer's value and *viceversa* (only if a reference is specified).
### 2. Decorator `pointerize`
Allows a function to receive `Pointer` objects instead of the normally expected values.
"""
# Imports
from .cleaning import Cleaner
from .pointers import Pointer,pointerize

# Declare `__all__`
__all__=["Cleaner","Pointer","pointerize"]