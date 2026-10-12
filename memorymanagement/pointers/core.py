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
    
    Non-mutable objects still change their memory adresses when re-referenced,
    but the reference and the value stored in the pointer are forced to share memory adress.
    
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
        Set to `inspect.currentframe().f_back.f_locals`.
    
    Methods
    -------
        **point_to**
            Changes the variable or attribute the pointer is pointed to.
        **get_refs**
            Returns all the references pointing to the pointer's value.
        **switch_ref**
            Allows to switch between the references pointing to the pointer's value.
    
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
    
    Literals are **not** supported because of it being useless, and they using them won't work.
    The only use for introducing a literal instead of a referenced value would be
    for the class code to display all the references pointing to the given literal,
    through the `get_refs` method, if there is more than one.
    """
    #* METHODS
    # __init__
    def __init__(self,value=None,reference:str|None=None,*,attr:str|None=None):
        """
        Arguments
        ---------
        value : `Any`|`None`, Optional
            Object to point to.
            If you want to point to an attribute, pass to this argument the class or instance without the attribute.
            If no reference is given, the pointer targets all the value's references.
            Note that the pointer points to the references of the object that shares the given value's identity, not content.
        reference : `str`|`None`, Optional
            Name linked to the value to point to.
            Useful in case there are multiple references pointing to the same object.
            Reference must be linked to the given value's identity.
            If no reference is given, all value's references will be targeted.
            If no value is given, the reference will be used to locate the target object.
        attr : `str`|`None`, Optional
            Name of the class or instance attribute to which the pointer will point to.
            Leave empty if the objective is to point to the instance itself instead of a single attribute.
        """
        # Store hidden attributes "_attr" and "_vars_dict"
        self._attr=attr # Instance attribute to point to
        self._vars_dict=vars_dict=currentframe().f_back.f_locals # Variables' dictionary
        
        # If no value or reference is given
        if not value and not reference:
            # Raise a "ValueError"
            raise ValueError("Either a value or a reference is needed")
        # Else, if a reference is given
        elif value and reference:
            #// if not isinstance(reference,str):
            #//     reference=set(reference)
            #//     if any(ref not in vars_dict for ref in reference):
            #//         raise NameError
            #//     elif any(vars_dict[ref] is not value for ref in reference):
            #//         raise ValueError
            #//     else:
            #//         name=tuple(reference)
            #// elif reference in vars_dict and vars_dict[reference] is value:
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
                raise ValueError(f"Name \"{reference}\" doesn't point to given value {value} ({value.__class__.__name__})")
        # Else, if only a reference is given
        elif reference:
            #// if not isinstance(reference,str):
            #//     reference=set(reference)
            #//     if any(ref not in vars_dict for ref in reference):
            #//         raise NameError
            #//     elif len(set(id(vars_dict[ref]) for ref in reference))>1:
            #//         raise ValueError
            #//     else:
            #//         name=tuple(reference)
            #// elif reference in vars_dict:
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
            # If the given value is between the variables' dictionary's values
            if value in vars_dict.values():
                # Get every reference to the given value
                name=tuple(key for key,v in vars_dict.items() if v is value)
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"No reference is pointing to given value {value} ({value.__class__.__name__})")
            
        # Set argument "value" as the pointer's value
        self._value=value
        # Store the reference in the hidden attribute "_name"
        self._name=name
        
        # If there is a class' or instance's attribute to point to but it doesn't belong to the given value
        if attr and attr not in dir(value):
            # Raise an "AttributeError"
            raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
    
    #// def __init__(self,value=None,reference:str|None=None,*,attr:str|None=None):
    #//     """
    #//     Arguments
    #//     ---------
    #//     value : `Any`|`None`, Optional
    #//         Object to point to. If want to point to a class instance's attribute, pass to this argument the class instance without the attribute.
    #//     reference : `str`|`None`, Optional
    #//         Name linked to the value to point to. Useful in case there are multiple references pointing to the same value.
    #//     attr : `str`|`None`, Optional
    #//         Name of the class or instance attribute to which the pointer will point to.
    #//         Leave empty if the objective is to point to the instance itself instead of a single attribute.
    #//     """
    #//     # Store hidden attributes "_attr" and "_vars_dict"
    #//     self._attr=attr # Instance attribute to point to
    #//     self._vars_dict=vars_dict=currentframe().f_back.f_locals # Variables' frame
        
    #//     # If no value or reference is given
    #//     if not value and not reference:
    #//         # Raise a "ValueError"
    #//         raise ValueError("Either a value or a reference is needed")
    #//     # Else, if a reference is given
    #//     elif value and reference:
    #//         # If the reference is in the variables' frame and points to the given value
    #//         if reference in vars_dict and vars_dict[reference] is value:
    #//             # Store the reference in "name" local variable
    #//             name=reference
    #//         # Else, if the reference isn't in the variables' frame
    #//         elif reference not in vars_dict:
    #//             # Raise a "NameError"
    #//             raise NameError(f"Name \"{reference}\" is not defined")
    #//         # Else, if the reference doesn't point to the given value
    #//         elif vars_dict[reference] is not value:
    #//             # Raise a "ValueError"
    #//             raise ValueError(f"Name \"{reference}\" doesn't point to given value {value} ({value.__class__.__name__})")
    #//     # Else, if only a reference is given
    #//     elif reference:
    #//         # If the given reference is in the variables' frame
    #//         if reference in vars_dict:
    #//             # Store the reference into local variable "name"
    #//             name=reference
    #//             # Store the value the reference is pointing to in argument "value"
    #//             value=vars_dict[reference]
    #//         # Else
    #//         else:
    #//             # Raise a "NameError"
    #//             raise NameError(f"Name \"{reference}\" is not defined")
    #//     # Else (only value)
    #//     else:
    #//         # If the given value is between the variables' frame values
    #//         if value in vars_dict.values():
    #//             # Loop for the variables' frame
    #//             for key,v in vars_dict.items():
    #//                 # If the current value is the given value
    #//                 if v is value:
    #//                     # The current key is the reference
    #//                     name=key
    #//                     # Break loop
    #//                     break
    #//         # Else
    #//         else:
    #//             # Raise a "NameError"
    #//             raise NameError(f"No reference is pointing to given value {value} ({value.__class__.__name__})")
            
    #//     # Set argument "value" as the pointer's value
    #//     self._value=value
    #//     # Store the reference in the hidden attribute "_name"
    #//     self._name=name
        
    #//     # If there is an instance's attribute to point to but it doesn't belong to the given value
    #//     if attr and attr not in dir(value):
    #//         # Raise an "AttributeError"
    #//         raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
    
    # Point to another object
    def point_to(self,value=None,reference:str|None=None,*,attr:str|None=None):
        """
        Reuses the Pointer object and makes it to point to a new object.
        
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
                    raise AttributeError(f"\"{attr}\" isn't an attribute of the name \"{self._name}\" with value {self._value} ({self._value.__class__.__name__})")
            # Else
            else:
                # Raise a "ValueError"
                raise ValueError("No argument was given")
        # Else, if both reference and value are given
        elif reference and value:
            #// if not isinstance(reference,str):
            #//     reference=set(reference)
            #//     if any(ref not in self._vars_dict for ref in reference):
            #//         raise NameError
            #//     elif any(self._vars_dict[ref] is not value for ref in reference):
            #//         raise ValueError
            #//     else:
            #//         self._name,self._value=tuple(reference),value
            #// elif reference in self._vars_dict and self._vars_dict[reference] is value:
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
                        raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
            # Else, if the reference isn't in the variables' frame
            elif reference not in self._vars_dict:
                # Raise a "NameError"
                raise NameError(f"Name \"{reference}\" is not defined")
            # Else, if the reference doesn't point to the given value
            elif self._vars_dict[reference] is not value:
                # Raise a "ValueError"
                raise ValueError(f"Name \"{reference}\" doesn't point to given value {value} ({value.__class__.__name__})")
        # Else, if only a reference is given
        elif reference:
            #// if not isinstance(reference,str):
            #//     reference=set(reference)
            #//     if any(ref not in self._vars_dict for ref in reference):
            #//         raise NameError
            #//     elif len(set(id(self._vars_dict[ref]) for ref in reference))>1:
            #//         raise ValueError
            #//     else:
            #//         self._name,self._value=tuple(reference),self._vars_dict[reference[0]]
            #// elif reference in self._vars_dict:
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
                        raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"Name \"{reference}\" is not defined")
        # Else (only value)
        else:
            # If the given value is between the variables' frame's values
            if value in self._vars_dict.values():
                # Loop for the variables' frame
                self._name,self._value=tuple(key for key,v in self._vars_dict.items() if v is value),value
                # If an instance's attribute name is given
                if attr:
                    # If the attribute belongs to the new value
                    if attr in dir(self._value):
                        # Store the attribute name into its corresponding hidden attribute
                        self._attr=attr
                    # Else
                    else:
                        # Raise an "AttributeError"
                        raise AttributeError(f"\"{attr}\" is not an attribute of {self._value.__class__.__name__} {self._value}")
            # Else
            else:
                # Raise a "NameError"
                raise NameError(f"No reference is pointing to given value {value} ({value.__class__.__name__})")
    
    #// def point_to(self,value=None,reference:str|None=None,*,attr:str|None=None):
    #//     """
    #//     Changes the address which the `Pointer` object points to.
    #//
    #//     Arguments
    #//     ---------
    #//     value : `Any`|`None`, Optional
    #//         Value to point to. If wanted class attribute, introduce just the class object.
    #//     reference : `str`|`None`, Optional
    #//         Reference pointing to the desired value. If wanted class attribute, introduce the reference for the class instance.
    #//     attr : `str`|`None`, Optional
    #//         Name of the class or instance attribute from the targeted object for the pointer to point to.
    #//         Leave empty if pointing to the object is desired instead of a single attribute.
    #//     """
    #//     # If no reference or value is given
    #//     if not value and not reference:
    #//         # If an instance's attribute name is given
    #//         if attr:
    #//             # If the attribute belongs to the pointer's value
    #//             if attr in dir(self._value):
    #//                 # Store the attribute name into its corresponding hidden attribute
    #//                 self._attr=attr
    #//             # Else
    #//             else:
    #//                 # Raise an "AttributeError"
    #//                 raise AttributeError(f"\"{attr}\" isn't an attribute of the name \"{self._name}\" with value {self._value} ({self._value.__class__.__name__})")
    #//         # Else
    #//         else:
    #//             # Raise a "ValueError"
    #//             raise ValueError("No argument was given")
    #//     # Else, if both reference and value are given
    #//     elif reference and value:
    #//         # If the reference is in the variables' frame and it points to the given value
    #//         if reference in self._vars_dict and self._vars_dict[reference] is value:
    #//             # Store both into their corresponding hidden attributes
    #//             self._name,self._value=reference,value
    #//             # If an attribute name is given
    #//             if attr:
    #//                 # If the attribute belongs to the given value
    #//                 if attr in dir(self._value):
    #//                     # Store attribute name into its corresponding hidden attribute
    #//                     self._attr=attr
    #//                 # Else
    #//                 else:
    #//                     # Raise an "AttributeError"
    #//                     raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
    #//         # Else, if the reference isn't in the variables' frame
    #//         elif reference not in self._vars_dict:
    #//             # Raise a "NameError"
    #//             raise NameError(f"Name \"{reference}\" is not defined")
    #//         # Else, if the reference doesn't point to the given value
    #//         elif self._vars_dict[reference] is not value:
    #//             # Raise a "ValueError"
    #//             raise ValueError(f"Name \"{reference}\" doesn't point to given value {value} ({value.__class__.__name__})")
    #//     # Else, if only a reference is given
    #//     elif reference:
    #//         # If the reference is in the variables' frame
    #//         if reference in self._vars_dict:
    #//             # Store the reference and the value it is pointing to into their corresponding hidden attributes
    #//             self._name,self._value=reference,self._vars_dict[reference]
    #//             # If an instance's attribute name is given
    #//             if attr:
    #//                 # If the attribute belongs to the new value
    #//                 if attr in dir(self._value):
    #//                     # Store the attribute name into its corresponding hidden attribute
    #//                     self._attr=attr
    #//                 # Else
    #//                 else:
    #//                     # Raise an "AttributeError"
    #//                     raise AttributeError(f"\"{attr}\" is not an attribute of {value} ({value.__class__.__name__})")
    #//         # Else
    #//         else:
    #//             # Raise a "NameError"
    #//             raise NameError(f"Name \"{reference}\" is not defined")
    #//     # Else (only value)
    #//     else:
    #//         # If the given value is between the variables' frame's values
    #//         if value in self._vars_dict:
    #//             # Loop for the variables' frame
    #//             for key,v in self._vars_dict.items():
    #//                 # If the current value is the given value
    #//                 if v is value:
    #//                     # The current key is the reference and the given value is set as pointer's value
    #//                     self._name,self._value=key,value
    #//                     # Break
    #//                     break
    #//             # If an instance's attribute name is given
    #//             if attr:
    #//                 # If the attribute belongs to the new value
    #//                 if attr in dir(self._value):
    #//                     # Store the attribute name into its corresponding hidden attribute
    #//                     self._attr=attr
    #//                 # Else
    #//                 else:
    #//                     # Raise an "AttributeError"
    #//                     raise AttributeError(f"\"{attr}\" is not an attribute of {self._value.__class__.__name__} {self._value}")
    #//         # Else
    #//         else:
    #//             # Raise a "NameError"
    #//             raise NameError(f"No reference is pointing to given value {value} ({value.__class__.__name__})")
    
    # Get references
    def get_refs(self)->tuple[str]:
        """
        Gets all the references pointing to the current value of the `Pointer` object.
        
        Returns
        -------
        tuple[str]
            References pointing to current pointer's value.
        """
        # Find and return all the references pointing to the pointer's value
        return tuple(key for key,v in self._vars_dict.items() if v is self._value)
    
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
        """
        # If no reference is given
        if not reference:
            # If no reference was found
            if len(self.reference)==0:
                # Delete the pointer's current value
                del self._value
                # If an attribute name was given
                if self._attr:
                    # Delete it
                    del self._attr
                # Raise a "NameError"
                raise NameError("The object has already been deleted, so the pointer no longer has access to it.")
        #// elif not isinstance(reference,str):
        #//     reference=set(reference)
        #//     if any(ref not in self._vars_dict for ref in reference):
        #//         raise NameError
        #//     elif any(self._vars_dict[ref] is not self.value for ref in reference):
        #//         raise ValueError
        #//     else:
        #//         reference=tuple(reference)
        # If the given reference is in the variables' frame but it doesn't point to current the pointer's value
        elif reference in self._vars_dict and self._vars_dict[reference] is not self.value:
            # Raise a "ValueError"
            raise ValueError(f"Name \"{reference}\" doesn't point to pointer's value {self.value} ({self.value.__class__.__name__})")
        # Else, if the given reference is not in the variables' frame
        elif reference not in self._vars_dict:
            # Raise a "NameError"
            raise NameError(f"Name \"{reference}\" is not defined")
        # Store the reference into its corresponding hidden attribute
        self._name=reference if reference else self._name
    
    #// def switch_ref(self,reference:str):
    #//     """
    #//     Allows to switch between references pointing to the same current value of the `Pointer` object.
        
    #//     Arguments
    #//     ---------
    #//     reference : `str`
    #//         Reference, pointing to the current pointer's value, to switch the pointer to.
    #//     """
    #//     # If the given reference is in the variables' frame but it doesn' point to current the pointer's value
    #//     if reference in self._vars_dict and self._vars_dict[reference] is not self.value:
    #//         # Raise a "ValueError"
    #//         raise ValueError(f"Name \"{reference}\" doesn't point to pointer's value {self._value} ({self._value.__class__.__name__})")
    #//     # Else, if the given reference is not in the variables' frame
    #//     elif reference not in self._vars_dict:
    #//         # Raise a "NameError"
    #//         raise NameError(f"Name \"{reference}\" is not defined")
    #//     # Store the reference into its corresponding hidden attribute
    #//     self._name=reference
    
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
            **Only for setter**.
            New value to set the pointer to.
        
        Returns
        -------
        Any
            **Only for getter**.
            Object or attribute value the pointer is pointing to.
            It is returned as-is, instead of a copy, so it can be manipulated thorugh its own methods.
        """
        # If an instance's attribute name is stored
        if self.attr:
            #// if not isinstance(self.reference,str):
            #//     erased=tuple(ref not in self._vars_dict for ref in self.reference)
            #//     if all(erased):
            #//         del self._value,self._attr
            #//         raise NameError
            #//     elif any(erased):
            #//         self._name=tuple(ref for ref in self.reference if ref in self._vars_dict)
            #//     del erased
            #//     num_new_values=len(set(self._vars_dict[ref] for ref in self.reference if self._vars_dict[ref] is not self._value))
            #//     if num_new_values>1:
            #//         raise Exception
            #//     elif num_new_values==1:
            #//         self._value=num_new_values[0]
            #//         for ref in self.reference:
            #//             self._vars_dict[ref]=self._value
            #// elif self.reference not in self._vars_dict:
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Get all references pointing to the current value
                self._name=self.get_refs()
                # If no reference was found
                if len(self.reference)==0:
                    # Delete the current value and the attribute's name
                    del self._value,self._attr
                    # Raise a "NameError"
                    raise NameError("The class instance has already been deleted, so the pointer no longer has access to it.")
            # If the stored reference is not in the variables' frame
            elif self.reference not in self._vars_dict:
                # Delete the pointer's value and the stored attribute name
                del self._value,self._attr
                # Raise a "NameError"
                raise NameError("The class instance has already been deleted, so the pointer no longer has access to it.")
            elif self._vars_dict[self.reference] is not self._value:
                self._value=self._vars_dict[self.reference]
                if self.attr not in dir(self._value):
                    raise AttributeError(f"The attribute \"{self._attr}\" has already been deleted, so the pointer no longer has access to it.")
            # Else, if the stored attribute name doesn't belong to the pointer's value
            elif self.attr not in dir(self._value):
                # Raise an "AttributeError"
                raise AttributeError(f"The attribute \"{self._attr}\" has already been deleted, so the pointer no longer has access to it.")
            # Return the instance attribute's value
            return getattr(self._value,self.attr)
        # Else
        else:
            #// if not isinstance(self.reference,str):
            #//     erased=tuple(ref not in self._vars_dict for ref in self.reference)
            #//     if all(erased):
            #//         del self._value
            #//         raise NameError
            #//     elif any(erased):
            #//         self._name=tuple(ref for ref in self.reference if ref in self._vars_dict)
            #//     del erased
            #//     num_new_values=len(set(self._vars_dict[ref] for ref in self.reference if self._vars_dict[ref] is not self._value))
            #//     if num_new_values>1:
            #//         raise Exception
            #//     elif num_new_values==1:
            #//         self._value=num_new_values[0]
            #//         for ref in self.reference:
            #//             self._vars_dict[ref]=self._value
            #// elif self.reference not in self._vars_dict:
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Get all references pointing to the current value
                self._name=self.get_refs()
                # If no reference was found
                if len(self.reference)==0:
                    # Delete current pointer's value
                    del self._value
                    # Raise a "NameError"
                    raise NameError("The variable has already been deleted, so the pointer no longer has access to it.")
            # If the stored reference is not in the variables' frame
            elif self.reference not in self._vars_dict:
                # Delete the pointer's hidden attribute "_value"
                del self._value
                # Raise a "NameError"
                raise NameError("The variable has already been deleted, so the pointer no longer has access to it.")
            # If the original value differs from the stored one (because it was changed)
            elif self._value is not self._vars_dict[self.reference]:
                # Update the pointer's value
                self._value=self._vars_dict[self.reference]
            # Return the pointer's value
            return self._value
    #// def value(self):
    #//     """
    #//     Gets, sets or deletes the pointer's value.
    #//     It also affects the original object if needed.
    #//     If an attribute name was originally given, the attribute value is affected instead of the given instance.
        
    #//     Arguments
    #//     ---------
    #//     value : `Any`|`None`
    #//         **Only for setter**.
    #//         New value to set the pointer to.
        
    #//     Returns
    #//     -------
    #//     Any
    #//         **Only for getter**.
    #//         Object or attribute value the pointer is pointing to.
    #//         It is returned as-is, instead of a copy, so it can be manipulated thorugh its own methods.
    #//     """
    #//     # If an instance's attribute name is stored
    #//     if self.attr:
    #//         # If the stored reference is not in the variables' frame
    #//         if self.reference not in self._vars_dict:
    #//             # Delete the pointer's value and the stored attribute name
    #//             del self._value,self.attr
    #//             # Raise a "NameError"
    #//             raise NameError("The class instance has already been deleted, so the pointer no longer has access to it.")
    #//         # Else, if the stored attribute name doesn't belong to the pointer's value
    #//         elif self.attr not in dir(self._value):
    #//             # Raise an "AttributeError"
    #//             raise AttributeError(f"The attribute \"{self._attr}\" has already been deleted, so the pointer no longer has access to it.")
    #//         # Return the instance attribute's value
    #//         return getattr(self._value,self.attr)
    #//     # Else
    #//     else:
    #//         # If the stored reference is not in the variables' frame
    #//         if self.reference not in self._vars_dict:
    #//             # Delete the pointer's hidden attribute "_value"
    #//             del self._value
    #//             # Raise a "NameError"
    #//             raise NameError("The variable has already been deleted, so the pointer no longer has access to it.")
    #//         # If the original value differs from the stored one (because it was changed)
    #//         if self._value is not self._vars_dict[self.reference]:
    #//             # Update the pointer's value
    #//             self._value=self._vars_dict[self.reference]
    #//         # Return the pointer's value
    #//         return self._value
    # Setter
    @value.setter
    def value(self,value):
        # If an attribute name is stored
        if self.attr:
            # Set the instance's attribute to the new value
            setattr(self._value,self.attr,value)
        # Else
        else:
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Loop for references
                for ref in self.reference:
                    # Set all the targeted references to the new value
                    self._vars_dict[ref]=value
            # Else, if the new pointer's value differs from the original variable
            elif value is not self._vars_dict[self.reference]:
                # Update the original variable setting it to the new value
                self._vars_dict[self.reference]=value
            # Set the pointer's value to the new value
            self._value=value
    #// def value(self,value):
    #//     # If an attribute name is stored
    #//     if self.attr:
    #//         # Set the instance' attribute to the new value
    #//         setattr(self._value,self.attr,value)
    #//     # Else
    #//     else:
    #//         # Set the pointer's value to the new value
    #//         self._value=value
    #//         # If the new pointer's value differs from the original variable
    #//         if value is not self._vars_dict[self.reference]:
    #//             # Update the original variable setting it to the new value
    #//             self._vars_dict[self.reference]=value
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
            # If a tuple is stored
            if isinstance(self.reference,tuple):
                # Get all references pointing to the current value
                self._name=self.get_refs()
                # Loop for references
                for ref in self.reference:
                    # Delete current reference from the variables' dictionary
                    del self._vars_dict[ref]
            # Else
            else:
                # Delete the corresponding variable
                del self._vars_dict[self.reference]
    
    # Reference
    @property
    # Getter
    def reference(self)->str|tuple:
        """
        Gets the reference or references the pointer is pointing to.
        
        Returns
        -------
        str|tuple
            Reference pointing to the `Pointer` instance.
        """
        # If a tuple is stored
        if isinstance(self._name,tuple):
            # Get all the references
            self._name=self.get_refs()
            # If no reference was found
            if len(self._name)==0:
                # Delete the pointer's value
                del self._value
                # Raise a "NameError"
                raise NameError("The targeted object has already been deleted, so the pointer no longer has access to it.")
        # Return the stored reference(s)
        return self._name
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
        return self._attr
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