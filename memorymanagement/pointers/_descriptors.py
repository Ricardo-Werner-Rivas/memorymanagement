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
    def __set_name__(self,owner,name):
        # Store the variable's name
        self.name=name
    
    # Getter
    def __get__(self,instance,owner):
        # If there is no instance
        if instance is None:
            # The descriptor instance is returned
            return self
        # Get the object calling the descriptor
        caller=currentframe().f_back.f_locals.get("self",None)
        # If it matches the received instance
        if caller is instance:
            # Return the stored value
            return self.value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the class")
    
    # Setter
    def __set__(self,instance,value):
        # Get the object calling the descriptor
        caller=currentframe().f_back.f_locals.get("self",None)
        # If it matches the received instance
        if caller is instance:
            # Store the new value
            self.value=value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the class")
    
    # Deleter
    def __delete__(self,instance):
        # Get the object calling the descriptor
        caller=currentframe().f_back.f_locals.get("self",None)
        # If it matches the received instance
        if caller is instance:
            # Delete the stored value
            del self.value
        # Else
        else:
            # Raise an `AttributeError`
            raise AttributeError(f"Attribute \"{self.name}\" is not accessible outside the class")