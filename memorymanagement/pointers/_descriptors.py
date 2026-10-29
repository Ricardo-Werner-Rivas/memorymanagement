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
# `currentframe` function from `inspect` package
from inspect import currentframe

#* ATTRIBUTE ACCESS MANAGER
# Define the attribute access manager descriptor
class AttrAccessManager:
    """
    Descriptor to block any access to the associated attribute from outside its owner class.
    The descriptor is the one storing the value of the attribute, instead of the owner class.
    
    The descriptor contains getter, setter and deleter.
    
    Methods
    -------
    __set_name__
        Stores the descriptor instance's name.
    __get__
        Checks if descriptor is called internally or externally.
        Returns the stored value if called internally.
    __set__
        Checks if descriptor is called internally or externally.
        Stores the new value if called internally.
    __delete__
        Checks if descriptor is called internally or externally.
        Deletes the stored value if called internally.
    """
    #* METHODS
    # Custom name
    def __set_name__(self,owner:type,name:str):
        # Store the variable's name
        self.name=name
    
    # Getter
    def __get__(self,instance:object,owner:type):
        # If the object calling the descriptor matches the received instance
        if currentframe().f_back.f_locals.get("self",None) is instance:
            # Return the stored value
            return self.value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the {owner.__name__} class")
    
    # Setter
    def __set__(self,instance:object,value):
        # If the object calling the descriptor matches the received instance
        if currentframe().f_back.f_locals.get("self",None) is instance:
            # Store the new value
            self.value=value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the {instance.__class__.__name__} class")
    
    # Deleter
    def __delete__(self,instance:object):
        # If the object calling the descriptor matches the received instance
        if currentframe().f_back.f_locals.get("self",None) is instance:
            # Delete the stored value
            del self.value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the {instance.__class__.__name__} class")