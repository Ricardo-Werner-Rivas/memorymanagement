"""
A safe implementation of pointers written in pure Python.

It is safe beacause it doesn't imitate the internal behaviour of C pointers, as it could break the memory.
It only replicates the visible effects and behaviour of C pointers.
## Class `Pointer`
This is the core of the module. The class `Pointer` points to a specific reference (not object in memory),
which will be syncrhonized with the pointer's value since the moment of the pointer's creation.

Pointing to every reference is also possible and, then, all of them will be syncrhonized with the pointer's value.
If any reference is reassigned, it will be taken out of the references register.
When no reference remains, the pointer's value will be deleted when called and will raise an error.

The pointer's value will be syncrhonized with its linked variable when the last is changed
only if the `Pointer` object is pointing to a single value's reference.

If all references are registered, synchronization is only possible when modified the pointer's value.
## Decorator `pointerize`
This decorator makes any function able to receive `Pointer` objects instead of the originally expected.
"""
# Import from modules
from .core import Pointer # Class "Pointer"
from .decorators import pointerize # Decorator "pointerize"
__all__=["Pointer","pointerize"]