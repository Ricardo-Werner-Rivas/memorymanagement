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

#^ The different types of comments require the "Colorful Comments Refreshed" extension for VSCode to be properly distinguished

#* IMPORTS
# Import "TypeVar" and "Generic"
from typing import TypeVar,Generic
# Import "currentframe" from "inspect" package
from inspect import currentframe
# Define type with TypeVar
PT=TypeVar("PT")

#* MAIN CLASS
# Define the class "Pointer" with generic type
class Pointer(Generic[PT]):
    """
    Implements pointers in Python for both mutable (though unneded) and non-mutable objects.
    These pointers are completely safe and do not work internally as C's pointers, they are just an imitation of their behaviour.
    
    When a Pointer instance is created, though it stores a value, it "points" to an specific reference, not the value in a memory adress.
    This way, all references pointing to the same non-mutable object don't change when the pointer is updated, avoiding a potential mess.
    
    Non-mutable objects still change their memory adresses when re-referenced but the reference and the value stored in the pointer are forced to share memory adress.
    
    Value and memory adress updates are not made in real-time, but the properties update the non-coincident values:
    * **Getter**: it updates its own value to the variable's one (if variable was given instead of literal).
    * **Setter**: it updates the value of the variable to its own (if variable was given instead of literal).
    * **Deleter**: it also deletes the original variable (if variable was given instead of literal).
    ---
    
    Attributes
    ----------
    value : `Any`, Hidden
        Object to point to.
    attr : `str`|`None`, Hidden
        Attribute of class instance. Only if `value` is a class instance.
    name : `str`, Hidden
        Name of the global variable to which the pointer is pointing.
        Could require an input from the user to introduce the name of the variable if more than one is found.
    vars_dict : `dict[str,Any]`, Hidden
        Dictionary of variables.
        `vars(modules["__main__"])` if pointing to a global variable and
        `inspect.currentframe().f_back.f_locals` if pointing to a local variable.
    
    Methods
    -------
        **point_to**
            Changes the variable or attribute the pointer is pointed to.
        **switch_ref**
            Allows to switch between the references pointing to the same value.
        **print_refs**
            Prints all the references pointing to the value.
    
    Properties
    ----------
        **value**
            Points to `value` (or `value.attr`).
            Called through `<instance@Pointer>.value`.
            All three possible objects (getter, setter and deleter) have been declared.
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
    
    Literals are **not** supported because of it being useless. Literals do **not** work anymore.
    The only use for introducing a literal instead of a referenced value is for the class code to bind the instance
    to an unknown reference pointing to the given value or to display all the references pointing to the given literal, through the `get_refs` or `print_refs` methods,
    if there is more than one.
    """
    #* METHODS
    # Constructor (__init__)
    def __init__(self,value=None,reference:str|None=None,*,attr:str|None=None):
        """
        Arguments
        ---------
        value : `Any`, Optional
            Object to point to. If want to point to a class instance's atribute, pass to this argument the class instance without the atribute.
        reference : `str`|`None`, Optional
            Name linked to the value to point to. Useful in case there are multiple references pointing to the same value.
        attr : `str`|`None`, Optional
            Attribute of the class instance to which you want to point. Leave empty if `value` is not a class instance.
        local : `bool`, Optional
            Indicates if the value to point to is a local variable (`True` for yes and `False` for no). `False` by default.
        """
        # Store hidden attributes "_attr" and "_vars_dict"
        self._attr=attr # Instance attribute to point to
        self._vars_dict=vars_dict=currentframe().f_back.f_locals # Variables' frame
        
        # If no value or reference is given
        if not value and not reference:
            # Raise a "ValueError"
            raise ValueError("Either a value or a reference is needed")
        # Else, if a reference is given
        elif value and reference:
            # If the reference is in the variables' frame and points to the given value
            if reference in vars_dict and vars_dict[reference] is value:
                # Store the reference in "name" local variable
                name=reference
            # Else, if the reference isn't in the variables' frame
            elif reference not in vars_dict:
                # Raise a "NameError"
                raise NameError(f"Name \"{reference}\" is not defined")
            # Else, if the reference doesn't point to the given value
            elif vars_dict[reference] is not value:
                # Raise a "ValueError"
                raise ValueError(f"Name \"{reference}\" doesn't point to given value ({value})")
        # Else, if only a reference is given
        elif reference:
            # If the given reference is in the variables' frame
            if reference in vars_dict:
                # Store the reference into local variable "name"
                name=reference
                # Store the value the reference is pointing to in argument "value"
                value=vars_dict[reference]
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"Name \"{reference}\" is not defined")
        # Else (only value)
        else:
            # If the given value is between the variables' frame values
            if value in vars_dict.values():
                # Loop for the variables' frame
                for key,v in vars_dict.items():
                    # If the current value is the given value
                    if v is value:
                        # The current key is the reference
                        name=key
                        # Break
                        break
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"No reference is pointing to given value \"{value}\" ({value.__class__.__name__})")
            
        # Set argument "value" as the pointer's value
        self._value=value
        # Store the reference in the hidden attribute "_name"
        self._name=name
        
        # If there is an instance's attribute to point to and it doesn't belong to the given value
        if attr and attr not in dir(value):
            # Raise an "AttributeError"
            raise AttributeError(f"\"{attr}\" is not an attribute of \"{value}\"")
    
    # Point to
    def point_to(self,value=None,reference:str|None=None,*,attr:str|None=None):
        """
        Changes the address which the `Pointer` object points to.
        
        Arguments
        ---------
        value : `Any`|`None`, Optional
            Value to point to. If wanted class attribute, introduce just the class object.
        reference : `str`|`None`, Optional
            Reference pointing to the desired value. If wanted class attribute, introduce the reference for the class instance.
        attr : `str`|`None`, Optional
            Attribute of the class if class object was passed through `reference` or `value`.
        """
        # If no reference or value is given
        if not value and not reference:
            # If an instance's attribute name is given
            if attr:
                # If the attribute belongs to the pointer's value
                if attr in dir(self._value):
                    # Store the attribute name into its corresponding hidden attribute
                    self._attr=attr
                # Else
                else:
                    # Raise an "AttributeError"
                    raise AttributeError(f"\"{attr}\" isn't an attribute of the variable \"{self._name}\" with value \"{self._value}\" (\"{self._value.__class__.__name__}\")")
            # Else
            else:
                # Raise a "ValueError"
                raise ValueError("No argument was given")
        # Else, if both reference and value are given
        elif reference and value:
            # If the reference is in the variables' frame and it points to the given value
            if reference in self._vars_dict and self._vars_dict[reference] is value:
                # Store both into their corresponding hidden attributes
                self._name,self._value=reference,value
                # If an attribute name is given
                if attr:
                    # If the attribute belongs to the given value
                    if attr in dir(self._value):
                        # Store attribute name into its corresponding hidden attribute
                        self._attr=attr
                    # Else
                    else:
                        # Raise an "AttributeError"
                        raise AttributeError(f"\"{attr}\" is not an attribute of \"{self._value}\"")
            # Else, if the reference isn't in the variables' frame
            elif reference not in self._vars_dict:
                # Raise a "NameError"
                raise NameError(f"Name \"{reference}\" is not defined")
            # Else, if the reference doesn't point to the given value
            elif self._vars_dict[reference] is not value:
                # Raise a "ValueError"
                raise ValueError(f"Name \"{reference}\" doesn't point to given value \"{value}\"")
        # Else, if only a reference is given
        elif reference:
            # If the reference is in the variables' frame
            if reference in self._vars_dict:
                # Store the reference and the value it is pointing to into their corresponding hidden attributes
                self._name,self._value=reference,self._vars_dict[reference]
                # If an instance's attribute name is given
                if attr:
                    # If the attribute belongs to the new value
                    if attr in dir(self._value):
                        # Store the attribute name into its corresponding hidden attribute
                        self._attr=attr
                    # Else
                    else:
                        # Raise an "AttributeError"
                        raise AttributeError(f"\"{attr}\" is not an attribute of \"{self._value}\"")
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"Name \"{reference}\" is not defined")
        # Else (only value)
        else:
            # If the given value is between the variables' frame's values
            if value in self._vars_dict:
                # Loop for the variables' frame
                for key,v in self._vars_dict.items():
                    # If the current value is the given value
                    if v is value:
                        # The current key is the reference and the given value is set as pointer's value
                        self._name,self._value=key,value
                        # Break
                        break
                # If an instance's attribute name is given
                if attr:
                    # If the attribute belongs to the new value
                    if attr in dir(self._value):
                        # Store the attribute name into its corresponding hidden attribute
                        self._attr=attr
                    # Else
                    else:
                        # Raise an "AttributeError"
                        raise AttributeError(f"\"{attr}\" is not an attribute of \"{self._value}\"")
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"No reference is pointing to given value \"{self._value}\"")
    
    # Get references
    def get_refs(self)->tuple[str]:
        """
        Gets all the references pointing to the same current value of the `Pointer` object.
        """
        # Find and return all the references pointing to the pointer's value
        return tuple(key for key,v in self._vars_dict.items() if v is self._value)
    
    #// # Print references
    #// def print_refs(self):
    #//     """
    #//     Prints all the references pointing to the same current value of the pointer.
    #//     """
    #//     # Print all the references pointing to the pointer's value
    #//     print(tuple(key for key,v in self._vars_dict.items() if v is self._value))
    
    # Switch reference
    def switch_ref(self,reference:str):
        """
        Allows to switch between references pointing to the same current value of the `Pointer` object.
        
        Arguments
        ---------
        reference : `str`
            Reference to switch the pointer to.
        """
        # If the given reference is in the variables' frame but it doesn' point to current the pointer's value
        if reference in self._vars_dict and self._vars_dict[reference] is not self.value:
            # Raise a "ValueError"
            raise ValueError(f"Name \"{reference}\" doesn't point to pointer's value \"{self.value}\"")
        # Else, if the given reference is not in the variables' frame
        elif reference not in self._vars_dict:
            # Raise a "NameError"
            raise NameError(f"Name \"{reference}\" is not defined")
        # Store the reference into its corresponding hidden attribute
        self._name=reference
    
    #* PROPERTIES
    # Value
    @property
    # Getter
    def value(self):
        # If an instance's attribute name is stored
        if self.attr:
            # If the stored reference is not in the variables' frame
            if self.reference not in self._vars_dict:
                # Delete the pointer's value and the stored attribute name
                del self._value,self.attr
                # Raise a "NameError"
                raise NameError("The class instance has already been deleted, so the pointer no longer has access to it.")
            # Else, if the stored attribute name doesn't belong to the pointer's value
            elif self.attr not in dir(self._value):
                # Raise an "AttributeError"
                raise AttributeError(f"The atribute \"{self._attr}\" has already been deleted, so the pointer no longer has access to it.")
            # Return the instance attribute's value
            return getattr(self._value,self.attr)
        # Else
        else:
            # If the stored reference is not in the variables' frame
            if self.reference not in self._vars_dict:
                # Delete the pointer's hidden attribute "_value"
                del self._value
                # Raise a "NameError"
                raise NameError("The variable has already been deleted, so the pointer no longer has access to it.")
            # If the original value differs from the stored one (because it was changed)
            if self._value is not self._vars_dict[self.reference]:
                # Update the pointer's value
                self._value=self._vars_dict[self.reference]
            # Return the pointer's value
            return self._value
    # Setter
    @value.setter
    def value(self,value):
        # If an attribute name is stored
        if self.attr:
            # Set the instance' attribute to the new value
            setattr(self._value,self.attr,value)
        # Else
        else:
            # Set the pointers value to the new value
            self._value=value
            # If the new pointer's value differs from the original variable
            if value is not self._vars_dict[self.reference]:
                # Update the original variable setting it to the new value
                self._vars_dict[self.reference]=value
    # Deleter
    @value.deleter
    def value(self):
        # If an attribute name is stored
        if self.attr:
            # Delete the attribute from the stored instance
            delattr(self._value,self.attr)
        # Else
        else:
            # Delete the "_value" pointer's hidden attribute
            del self._value
            # Delete the corresponding variable
            del self._vars_dict[self.reference]
    
    # Reference
    @property
    # Getter
    def reference(self):
        # Return the stored reference
        return self._name
    
    # Attribute
    @property
    def attr(self):
        # Return the stored attribute name
        return self._attr
    
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
        if isinstance(value,Pointer):
            return self.value+value.value
        else:
            return self.value+value
    
    # Difference
    def __sub__(self,value):
        if isinstance(value,Pointer):
            return self.value-value.value
        else:
            return self.value-value
    
    # Multiplication
    def __mul__(self,value):
        if isinstance(value,Pointer):
            return self.value*value.value
        else:
            return self.value*value
    
    # Fraction
    def __truediv__(self,value):
        if isinstance(value,Pointer):
            return self.value/value.value
        else:
            return self.value/value
    
    # Integer division
    def __floordiv__(self,value):
        if isinstance(value,Pointer):
            return self.value//value.value
        else:
            return self.value//value
    
    # Module
    def __mod__(self,value):
        if isinstance(value,Pointer):
            return self.value%value.value
        else:
            return self.value%value
    
    # Power
    def __pow__(self,value):
        if isinstance(value,Pointer):
            return self.value**value.value
        else:
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
        self.value=self.value+value
        return self
    
    # Difference
    def __isub__(self,value):
        self.value=self.value-value
        return self
    
    # Multiplication
    def __imul__(self,value):
        self.value=self.value*value
        return self
    
    # Fraction
    def __itruediv__(self,value):
        self.value=self.value/value
        return self
    
    # Integer division
    def __ifloordiv__(self,value):
        self.value=self.value//value
        return self
    
    # Module
    def __imod__(self,value):
        self.value=self.value%value
        return self
    
    def __ipow__(self,value):
        self.value=self.value**value
        return self
    
    #* COMPARATIVE METHODS
    # Equality
    def __eq__(self,value):
        if isinstance(value,Pointer):
            return self.value==value.value
        else:
            return self.value==value
    
    # Inequality
    def __ne__(self,value):
        if isinstance(value,Pointer):
            return self.value!=value.value
        else:
            return self.value!=value
    
    # Lower than
    def __lt__(self,value):
        if isinstance(value,Pointer):
            return self.value<value.value
        else:
            return self.value<value
    
    # Lower or equal
    def __le__(self,value):
        if isinstance(value,Pointer):
            return self.value<=value.value
        else:
            return self.value<=value
    
    # Greater than
    def __gt__(self,value):
        if isinstance(value,Pointer):
            return self.value>value.value
        else:
            return self.value>value
    
    # Greater or equal
    def __ge__(self,value):
        if isinstance(value,Pointer):
            return self.value>=value.value
        else:
            return self.value>=value
    
    #* UNARY METHODS
    # Negative
    def __neg__(self):
        return Pointer(-self.value)
    
    # Positive
    def __pos__(self):
        return Pointer(+self.value)
    
    # Absolute value
    def __abs__(self):
        return Pointer(abs(self.value))
    
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
        return f"{self.__class__.__name__}({self.value},{self.reference},attr={self.attr})"
    
    # HTML representation
    def _repr_html_(self):
        return f"""\
<table>
    <thead>
        <tr>
            <th style=\"text-align: center;\">{self.reference}</th>
        </tr>
    </thead>
    <tr>
        <td style=\"text-align: center;\">{self.value}</td>
    </tr>
</table>\
"""
    
    # Printing
    def __str__(self):
        return str(self.value)