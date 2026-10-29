#*===============================================================================================================================
#* LEGEND
#*-------------------------------------------------------------------------------------------------------------------------------
#! Missing
#& Missing unimportant
#? Question
#* Section
#^ Important
# Normal comment
#// Alternative or deprecated code
#*===============================================================================================================================

#* IMPORTS
# Import `TypeVar` and `Generic`
from typing import TypeVar,Generic
# Import `Generator` from `collections.abc` module
from collections.abc import Generator
# Import `currentframe` from `inspect` package
from inspect import currentframe
# Import `AttrAccessManager` from the `descriptors` module
from ._descriptors import AttrAccessManager

#* TYPING
# Define type with `TypeVar`
PT=TypeVar("PT")

#* MAIN CLASS
# Define the class `Pointer` with generic type
class Pointer(Generic[PT]):
    """
    Implements pointers in Python for both mutable (though unneded) and non-mutable objects.
    These pointers are completely safe and do not work internally as C's pointers, they are just an imitation of their behaviour.
    
    When a Pointer instance is created, though it stores a value, it "points" to an specific reference, not the value in a memory address.
    This way, all references pointing to the same non-mutable object don't change when the pointer is updated, avoiding a potential mess.
    
    It is possible to point to every reference linked to the value, but the pointer's value will not be updated when one or more references change.
    Instead, those references will be untargeted.
    Once the number of targeted references drops to `0`, the value is deleted and the pointer raises an error when called.
    
    Non-mutable objects still change their memory addresses when re-referenced,
    but the reference and the value stored in the pointer are forced to share memory address.
    
    Value and memory address updates are not made in real-time, but the properties update the non-matching values:
    * **Getter**: it updates its own value to the variable's one (if a single reference is targeted).
    * **Setter**: it updates the value of the variable(s) to its own.
    * **Deleter**: it deletes the original variable.
    ---
    
    Attributes
    ----------
    value : `Any`, Obfuscated descriptor
        Object to point to.
    attr : `str`|`None`, Obfuscated descriptor
        Name of class or instance attribute. Only if `value` is a class or instance.
    name : `str`|`tuple[str]`, Obfuscated descriptor
        Name of the variable to which the pointer is pointing.
        Could be a tuple of names.
    vars_dict : `dict[str,Any]`, Obfuscated descriptor
        Variables' dictionary.
        Set to `inspect.currentframe().f_back.f_locals` by default.
    
    Methods
    -------
        **point_to**
            Changes the variable or attribute the pointer is pointed to.
        **get_refs**
            Returns all the references pointing to the pointer's value.
        **select_ref**
            Switches to a reference through an index instead of the reference's name.
        **switch_ref**
            Allows to switch between the references pointing to the pointer's value.
        **switch_frame**
            Allows to switch between the global and local frames.
    
    Properties
    ----------
        **value**
            Points to `value` (or `value.attr`).
            Called through `<instance@Pointer>.value`.
            All three possible objects (getter, setter and deleter) have been defined.
        **reference**
            Pointed reference.
            Called through `<instance@Pointer>.reference`.
            **Only getter** defined.
        **attr**
            Name of the attribute of the pointed class instance.
            Called through `<instance@Pointer>.attr`.
            **Only getter** defined.
    ---
    ## Currently supported
    Both global and local variables can be pointed at.
    
    Non-referenced literals are **not** supported.
    """
    #* SLOTS
    # Declare empty slots so the attributes are controlled
    __slots__=()
    
    #* DESCRIPTORS
    # Declare the descriptor obfuscated attributes so they can only be accessed through the instances' methods
    __attr=AttrAccessManager() # Targeted attribute
    __name=AttrAccessManager() # Targeted reference
    __value=AttrAccessManager() # Targeted value
    __vars_dict=AttrAccessManager() # Variables' dictionary
    
    #* METHODS
    # __init__
    def __init__(self,value=None,reference:str|None=None,*,attr:str|None=None):
        """
        Arguments
        ---------
        value : `Any`|`None`, Optional
            Object to point to.
            If you want to point to an attribute, pass to this argument the class or instance without the attribute name.
            If no reference is given, the pointer targets all the value's references.
            Note that the pointer points to the references of the object that shares the given value's identity, not content.
        reference : `str`|`None`, Optional
            Name linked to the value to point to.
            Useful in case there are multiple references pointing to the same object.
            Reference must be linked to the given value's identity, if a value was given.
            If no reference is given, all value's references will be targeted.
            If no value is given, the reference will be used to locate the target object.
        attr : `str`|`None`, Optional
            Name of the class or instance attribute to which the pointer will point to.
            Leave empty if the objective is to point to the instance itself instead of a single attribute.
        
        Raises
        ------
        NameError
            If the object doesn't exist or reference is not defined.
        ValueError
            If the reference's value doesn't match the given value.
            Also if no argument is given.
        AttributeError
            If the targeted attribute doesn't belong to the targeted object.
        """
        # Store hidden attributes `__attr` and `__vars_dict`
        self.__attr=attr # Class or instance attribute to point to
        self.__vars_dict=vars_dict=currentframe().f_back.f_locals # Variables' dictionary
        
        # If no value or reference is given
        if not value and not reference:
            # Raise a `ValueError`
            raise ValueError("Either a value or a reference is needed")
        # Else, if a reference is given
        elif value and reference:
            # If the reference is in the variables' frame and points to the given value
            if reference in vars_dict and vars_dict[reference] is value:
                # Store the reference in `name` local variable
                name=reference
            # Else, if the reference isn't in the variables' frame
            elif reference not in vars_dict:
                # Raise a `NameError`
                raise NameError(f"Name \"{reference}\" is not defined")
            # Else, if the reference doesn't point to the given value
            elif vars_dict[reference] is not value:
                # Raise a `ValueError`
                raise ValueError(f"Name \"{reference}\" doesn't point to given value {value} ({value.__class__.__name__})")
        # Else, if only a reference is given
        elif reference:
            # If the given reference is in the variables' dictionary
            if reference in vars_dict:
                # Store the reference into local variable `name`
                name=reference
                # Store the value the reference is pointing to in argument `value`
                value=vars_dict[reference]
            # Else
            else:
                # Raise a `NameError`
                raise NameError(f"Name \"{reference}\" is not defined")
        # Else (only value)
        else:
            # If the given value is between the variables' dictionary's values
            if value in vars_dict.values():
                # Get every reference to the given value
                name=tuple(key for key,v in vars_dict.items() if v is value)
            # Else
            else:
                # Raise a `NameError`
                raise NameError(f"No reference is pointing to given value {value} ({value.__class__.__name__})")
            
        # Set argument `value` as the pointer's value
        self.__value=value
        # Store the reference in the hidden attribute `__name`
        self.__name=name
        
        # If there is a class' or instance's attribute to point to but it doesn't belong to the given value
        if attr and attr not in dir(value):
            # Raise an `AttributeError`
            raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
    
    # Point to another object
    def point_to(self,value=None,reference:str|None=None,*,attr:str|None=None):
        """
        Reuses the `Pointer` object and makes it to point to a new object.
        
        Arguments
        ---------
        value : `Any`|`None`, Optional
            Value to point to.
            If wanted to point to an attribute, introduce just the class or instance without the attribute.
        reference : `str`|`None`, Optional
            Reference pointing to the desired value.
            Reference must be linked to the given value's identity.
            If no reference is given, all value's references will be targeted.
            If no value is given, the reference will be used to locate the target object.
        attr : `str`|`None`, Optional
            Name of the class or instance attribute from the targeted object for the pointer to point to.
            Leave empty if pointing to the object is desired instead of a single attribute.
        
        Raises
        ------
        NameError
            If the object or targeted reference exists no more.
        ValueError
            If the reference's value doesn't match the pointer's value.
            Also if no argument is given.
        AttributeError
            If the targeted attribute doesn't belong to the targeted instance.
        """
        # If no reference or value is given
        if not value and not reference:
            # If an instance's attribute name is given
            if attr:
                # If the attribute belongs to the pointer's value
                if attr in dir(self.value):
                    # Store the attribute name into its corresponding hidden attribute
                    self.__attr=attr
                # Else
                else:
                    # Raise an `AttributeError`
                    raise AttributeError(f"\"{attr}\" isn't an attribute of the name \"{self.__name}\" with value {self.__value} ({self.__value.__class__.__name__})")
            # Else
            else:
                # Raise a `ValueError`
                raise ValueError("No argument was given")
        # Else, if both reference and value are given
        elif reference and value:
            # If the reference is in the variables' frame and it points to the given value
            if reference in self.__vars_dict and self.__vars_dict[reference] is value:
                # Store both into their corresponding hidden attributes
                self.__name,self.__value=reference,value
                # If an attribute name is given
                if attr:
                    # If the attribute belongs to the given value
                    if attr in dir(self.__value):
                        # Store attribute name into its corresponding hidden attribute
                        self.__attr=attr
                    # Else
                    else:
                        # Raise an `AttributeError`
                        raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
            # Else, if the reference isn't in the variables' frame
            elif reference not in self.__vars_dict:
                # Raise a `NameError`
                raise NameError(f"Name \"{reference}\" is not defined")
            # Else, if the reference doesn't point to the given value
            elif self.__vars_dict[reference] is not value:
                # Raise a `ValueError`
                raise ValueError(f"Name \"{reference}\" doesn't point to given value {value} ({value.__class__.__name__})")
        # Else, if only a reference is given
        elif reference:
            # If the reference is in the variables' frame
            if reference in self.__vars_dict:
                # Store the reference and the value it is pointing to into their corresponding hidden attributes
                self.__name,self.__value=reference,self.__vars_dict[reference]
                # If an instance's attribute name is given
                if attr:
                    # If the attribute belongs to the new value
                    if attr in dir(self.__value):
                        # Store the attribute name into its corresponding hidden attribute
                        self.__attr=attr
                    # Else
                    else:
                        # Raise an `AttributeError`
                        raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
            # Else
            else:
                # Raise a `NameError`
                raise NameError(f"Name \"{reference}\" is not defined")
        # Else (only value)
        else:
            # If the given value is between the variables' frame's values
            if value in self.__vars_dict.values():
                # Loop for the variables' frame
                self.__name,self.__value=tuple(key for key,v in self.__vars_dict.items() if v is value),value
                # If an instance's attribute name is given
                if attr:
                    # If the attribute belongs to the new value
                    if attr in dir(self.__value):
                        # Store the attribute name into its corresponding hidden attribute
                        self.__attr=attr
                    # Else
                    else:
                        # Raise an `AttributeError`
                        raise AttributeError(f"\"{attr}\" is not an attribute of {self.__value.__class__.__name__} {self.__value}")
            # Else
            else:
                # Raise a `NameError`
                raise NameError(f"No reference is pointing to given value {value} ({value.__class__.__name__})")
    
    # Get references
    def get_refs(self,*,lazy:bool=False)->tuple[str]|Generator[str]:
        """
        Gets all the references pointing to the current value of the `Pointer` object.
        
        Arguments
        ---------
        lazy : `bool`, Optional
            A lazy (generator) object is returned instead of a tuple.
            The lazy object is generated from a copy of the variables' dictionary at the moment
            the method is called to prevent errors.
        
        Returns
        -------
        tuple[str]|Generator[str]
            References pointing to current pointer's value.
        """
        # If the stored reference is a string
        if isinstance(self.__name,str):
            # Execute `value` property getter to update pointer's value
            self.value
        # Obtain all the references as a lazy object (generator)
        references=(key for key,value in self.__vars_dict.copy().items() if value is self.__value)
        # Return all the references pointing to the pointer's value either as a lazy object or as a tuple
        return references if lazy else tuple(references)
    
    # Select reference by index
    def select_ref(self,index:int=0,/,*,random:bool=False,fast:bool=False):
        """
        Selects a reference from the ones linked to the pointer's value using the provided index.
        
        In case there are too many variables in the corresponding dictionary, a fast method is available.
        The fast method loops through the lazy `get_refs` method's resultant object until the desired reference is found
        instead of looping through the whole variables' dictionary, which is what the normal `get_refs` method does,
        and indexing the resulting tuple.
        
        Fast method is only needed in case of massive amounts of variables.
        Performance difference is minimal for any other case.
        Fast method is only available for positive indexes.
        
        Arguments
        ---------
        index : `int`, Optional
            Position index for the references' tuple.
            The reference stored in the provided position is set as the only targeted reference.
            Defaults to the first position (`0`).
        random : `bool`, Optional
            Whether to select a random reference from the available ones (`True`) or not (`False`).
            Defaults to `False`.
            `random` argument ignores any other argument.
        fast : `bool`, Optional
            Whether to use the fast method to select the reference (`True`) or not (`False`).
            Defaults to `False`.
        
        Returns
        -------
        Pointer
            The `Pointer` object is returned.
        
        Raises
        ------
        IndexError
            When given index is out of range.
        """
        # If a random reference is required
        if random:
            # Import the `choice` function from `random` package
            from random import choice
            # Switch to a random reference
            self.switch_ref(choice(self.get_refs()))
        # Else
        else:
            # Try
            try:
                # If the given index is not negative
                if fast and index>=0:
                    # Store a lazy object of references
                    references=self.get_refs(lazy=True)
                    # Loop number up to the given index
                    for i in range(index):
                        # Call the next value of the generator
                        next(references)
                    # Switch to the next value of the generator (desired reference)
                    self.switch_ref(next(references))
                # Else
                else:
                    # Switch reference
                    self.switch_ref(self.get_refs()[index])
            # If an `IndexError` or a `StopIteration` are raised
            except IndexError,StopIteration:
                # Raise an `IndexError`
                raise IndexError("Provided index is out of range")
        # Return the `Pointer` object
        return self
    
    # Switch reference
    def switch_ref(self,reference:str|None=None):
        """
        Switches between references pointing to the same current value of the `Pointer` object.
        
        Arguments
        ---------
        reference : `str`|`None`, Optional
            Reference, pointing to the current pointer's value, to switch the pointer to.
            If empty, the `Pointer` object targets every reference pointing to its current value,
            as if it were actually pointing to the value's memory address.
        
        Returns
        -------
        Pointer
            The `Pointer` object is returned.
        
        Raises
        ------
        NameError
            If the object or targeted reference exists no more.
        ValueError
            If the reference's value doesn't match the pointer's value.
        """
        # If no reference is given
        if not reference:
            # Get all references pointing to the current value
            reference=self.get_refs()
            # If no reference was found
            if len(reference)==0:
                # Delete the pointer's current value
                del self.__value
                # If an attribute name was given
                if self.__attr:
                    # Delete it
                    del self.__attr
                # Raise a `NameError`
                raise NameError("The variable has already been deleted, so the pointer no longer has access to it.")
        # Else, if the given reference is in the variables' frame but it doesn't point to current the pointer's value
        elif reference in self.__vars_dict and self.__vars_dict[reference] is not self.value:
            # Raise a `ValueError`
            raise ValueError(f"Name \"{reference}\" doesn't point to pointer's value {self.__value} ({self.__value.__class__.__name__})")
        # Else, if the given reference is not in the variables' frame
        elif reference not in self.__vars_dict:
            # Raise a `NameError`
            raise NameError(f"Name \"{reference}\" is not defined")
        # Store the reference into its corresponding hidden attribute
        self.__name=reference
        # Return the `Pointer` object
        return self
    
    # Switch frame
    def switch_frame(self):
        """
        Switches the variables' frame from current local to global and vice versa.
        
        Returns
        -------
        Pointer
            The `Pointer` object is returned.
        """
        # Get the frame of origin
        frame=currentframe().f_back
        # Set `_var_dict` hidden attribute to the global or the current local frame
        self.__vars_dict=frame.f_globals if frame.f_globals!=self.__vars_dict else frame.f_locals
        # Return the `Pointer` object
        return self
    
    #* PROPERTIES
    # Value
    @property
    # Getter
    def value(self):
        """
        Gets, sets or deletes the pointer's value.
        It also affects the original object(s) if needed.
        If an attribute name was originally given, the attribute value is affected instead of the given instance.
        
        If pointing to all references, they get updated.
        
        Arguments
        ---------
        value : `Any`|`None`
            New value to set the pointer to.
        
        Returns
        -------
        Any
            Object or attribute value the pointer is pointing to.
            It is returned as-is, instead of a copy, so it can be manipulated through its own methods.
        
        Raises
        ------
        NameError
            If the object or targeted reference exists no more.
        AttributeError
            If the targeted attribute doesn't belong to the targeted instance.
        """
        # If an instance's attribute name is stored
        if self.attr:
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Pass
                pass
            # Else, if the stored reference is not in the variables' frame
            elif self.reference not in self.__vars_dict:
                # Delete the pointer's value and the stored attribute name
                del self.__value,self.__attr
                # Raise a `NameError`
                raise NameError("The given instance has already been deleted, so the pointer no longer has access to it.")
            # Else, if the reference isn't pointing to the pointer's value
            elif self.__vars_dict[self.reference] is not self.__value:
                # Update pointer's value
                self.__value=self.__vars_dict[self.reference]
            
            # If the stored attribute name doesn't belong to the pointer's value
            if self.attr not in dir(self.__value):
                # Raise an `AttributeError`
                raise AttributeError(f"The attribute \"{self.attr}\" has already been deleted, so the pointer no longer has access to it.")
            # Return the instance attribute's value
            return getattr(self.__value,self.attr)
        # Else
        else:
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Pass
                pass
            # Else, if the stored reference is not in the variables' frame
            elif self.reference not in self.__vars_dict:
                # Delete the pointer's hidden attribute `__value`
                del self.__value
                # Raise a `NameError`
                raise NameError("The variable has already been deleted, so the pointer no longer has access to it.")
            # Else, if the original value differs from the stored one (because it was changed)
            elif self.__value is not self.__vars_dict[self.reference]:
                # Update the pointer's value
                self.__value=self.__vars_dict[self.reference]
            # Return the pointer's value
            return self.__value
    # Setter
    @value.setter
    def value(self,value):
        # If an attribute name is stored
        if self.attr:
            # Set the instance's attribute to the new value
            setattr(self.__value,self.attr,value)
        # Else
        else:
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Loop for references
                for ref in self.__name:
                    # Set all the targeted references to the new value
                    self.__vars_dict[ref]=value
            # Else, if the new pointer's value differs from the original variable
            elif value is not self.__vars_dict[self.reference]:
                # Update the original variable setting it to the new value
                self.__vars_dict[self.reference]=value
            # Set the pointer's value to the new value
            self.__value=value
    # Deleter
    @value.deleter
    def value(self):
        # If an attribute name is stored
        if self.attr:
            # Delete the attribute from the stored instance
            delattr(self.__value,self.attr)
        # Else
        else:
            # Delete the `__value` pointer's hidden attribute
            del self.__value
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Loop for references
                for ref in self.__name:
                    # Delete current reference from the variables' dictionary
                    del self.__vars_dict[ref]
            # Else
            else:
                # Delete the corresponding variable
                del self.__vars_dict[self.reference]
    
    # Reference
    @property
    # Getter
    def reference(self)->str|tuple[str]:
        """
        Gets the reference or references the pointer is pointing to.
        
        Returns
        -------
        str|tuple[str]
            Reference pointing to the `Pointer` instance.
        
        Raises
        ------
        NameError
            Raised if object was already deleted or the targeted reference exists no more.
        """
        # If a tuple is stored
        if isinstance(self.__name,tuple):
            # Get all the references
            self.__name=self.get_refs()
            # If no reference was found
            if len(self.__name)==0:
                # Delete the pointer's value
                del self.__value
                # If an attribute name was given
                if self.attr:
                    # Delete `__attr` hidden attribute
                    del self.__attr
                # Raise a `NameError`
                raise NameError("The object has already been deleted, so the pointer no longer has access to it.")
        # Return the stored reference(s)
        return self.__name
    #^ No setter
    #^ No deleter
    
    # Attribute
    @property
    def attr(self)->str|None:
        """
        Gets the name of the attribute the pointer is pointing to, if it was given.
        
        Returns
        -------
        str|None
            Name of instance or class attribute the pointer is pointing to.
        """
        # Return the stored attribute name
        return self.__attr
    #^ No setter
    #^ No deleter
    
    #* INDEXATION
    # Getter
    def __getitem__(self,index):
        return self.value[index]
    # Setter
    def __setitem__(self,index,value):
        self.value[index]=value
    # Deleter
    def __delitem__(self,index):
        del self.value[index]
    
    #* ARITHMETIC OPERATIONS
    # Addition
    def __add__(self,value):
        return self.value+value
    
    # Difference
    def __sub__(self,value):
        return self.value-value
    
    # Multiplication
    def __mul__(self,value):
        return self.value*value
    
    # Fraction
    def __truediv__(self,value):
        return self.value/value
    
    # Integer division
    def __floordiv__(self,value):
        return self.value//value
    
    # Module
    def __mod__(self,value):
        return self.value%value
    
    # Power
    def __pow__(self,value):
        return self.value**value
    
    #* REFLEXED ARITHMETIC METHODS
    # Addition
    def __radd__(self,value):
        return value+self.value
    
    # Difference
    def __rsub__(self,value):
        return value-self.value
    
    # Multiplication
    def __rmul__(self,value):
        return value*self.value
    
    # Fraction
    def __rtruediv__(self,value):
        return value/self.value
    
    # Integer division
    def __rfloordiv__(self,value):
        return value//self.value
    
    # Module
    def __rmod__(self,value):
        return value%self.value
    
    # Power
    def __rpow__(self,value):
        return value**self.value
    
    #* IN-PLACE ARITHMETIC METHODS
    # Addition
    def __iadd__(self,value):
        self.value+=value
        return self
    
    # Difference
    def __isub__(self,value):
        self.value-=value
        return self
    
    # Multiplication
    def __imul__(self,value):
        self.value*=value
        return self
    
    # Fraction
    def __itruediv__(self,value):
        self.value/=value
        return self
    
    # Integer division
    def __ifloordiv__(self,value):
        self.value//=value
        return self
    
    # Module
    def __imod__(self,value):
        self.value%=value
        return self
    
    def __ipow__(self,value):
        self.value**=value
        return self
    
    #* COMPARATIVE METHODS
    # Equality
    def __eq__(self,value):
        return self.value==value.value if isinstance(value,Pointer) else self.value==value
    
    # Inequality
    def __ne__(self,value):
        return self.value!=value.value if isinstance(value,Pointer) else self.value!=value
    
    # Lower than
    def __lt__(self,value):
        return self.value<value.value if isinstance(value,Pointer) else self.value<value
    
    # Lower or equal
    def __le__(self,value):
        return self.value<=value.value if isinstance(value,Pointer) else self.value<=value
    
    # Greater than
    def __gt__(self,value):
        return self.value>value.value if isinstance(value,Pointer) else self.value>value
    
    # Greater or equal
    def __ge__(self,value):
        return self.value>=value.value if isinstance(value,Pointer) else self.value>=value
    
    #* UNARY METHODS
    # Negative
    def __neg__(self):
        return -self.value
    
    # Positive
    def __pos__(self):
        return +self.value
    
    # Absolute value
    def __abs__(self):
        return abs(self.value)
    
    #* LENGTH
    # Length
    def __len__(self):
        return len(self.value)
    
    #* TRANSFORMATION METHODS
    # __int__
    def __int__(self):
        return int(self.value)
    
    # __float__
    def __float__(self):
        return float(self.value)
    
    # __index__
    def __index__(self):
        return self.value
    
    #* SCREEN
    # Representation
    def __repr__(self):
        return f"{self.__class__.__name__}({self.value},{self.reference if isinstance(self.reference,str) else None},attr={self.attr})"
    
    # HTML representation
    def _repr_html_(self):
        return f"""\
<table>
    <thead>
        <tr>
            <th style="text-align: center;">{self.reference}</th>
        </tr>
    </thead>
    <tr>
        <td style="text-align: center;">{self.value}</td>
    </tr>
</table>\
"""
    
    # Printing
    def __str__(self):
        return str(self.value)