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
# modules from sys
from inspect import currentframe

#* MAIN CLASS
# Class "Cleaner"
class Cleaner:
    """
    Class for references management. It keeps track of the names of the global variables to be deleted and deletes them when ordered.
    
    The cleaning process only deletes the flagged references to objects, but doesn't directly force the garbage collector to destroy the objects they are pointing to.
    
    ## WARNING
    THERE CAN ONLY BE **ONE** CLEANER OBJECT.\n
    Initializing a new one will delete all global references to the previous one.
    
    Attributes
    ----------
    _not_delete : `list[str]`, Hidden
        List of variables to never delete from memory. These cannot be included in the process even if ordered so.
        These mainly are imports and variables needed for the system to work.
    _excluded : `list[str]`, Hidden
        List of variables excluded from the memory cleaning that can be included again if desired.
    _flagged : `list[str]`, Hidden
        List of variables to erase from memory. Variables can be put in and/or taken out through methods.
    _name : `str`, Hidden
        Name of the variable referencing the `Cleaner` object. Only for internal purposes.
    
    Methods
    -------
        **update**
            Updates the list of variables to erase from memory including all the new variables global variables not manually excluded. It also allows to incorporate previously excluded variables.
        **exclude**
            Allows you to exclude variables from the cleaning process without need to use the `instance.update()` method.
        **include**
            Allows you to include variables in the cleaning process without need to use the `instance.update()` method.
        **clean**
            Erases all the flagged references from memory.
    
    Properties
    ----------
        **not_delete**
            Returns the list of variables that shouldn't be deleted and can't be included in the cleaning process.
        **excluded**
            Returns the list of variables excluded from the cleaning process but can be included again if ordered.
        **flagged**
            Returns the list of variables to be erased from memory.
        None of this properties has setter or deleter. Those lists can only be manipulated through the class methods.
    """
    #* METHODS
    # __init__
    def __init__(self,not_delete:list[str]|None=None,excluded:list[str]=[],flagged:list[str]=[]):
        """
        Initializes the class instance.\n
        It is recommended to initialize the instance right after all global imports at the beggining of the program so no argument is needed.
        
        Arguments
        ---------
        not_delete : `list[str]`|`None`, Optional
            List of variables to never be deleted. It takes the list of global variables of the main module by default.
        excluded : `list[str]`, Optional
            List of variables to be excluded from the memory cleaning process. Empty list by default.
        flagged : `list[str]`, Optional
            List of variables to be erased from memory. Empty list by default.
        """
        # Store variables' dictionary
        self._vars_dict=currentframe().f_back.f_locals
        # If a "not_delete" list is not passed
        if not not_delete:
            # Take the list of variables' dictionay's keys
            not_delete=list(self._vars_dict)
        # Loop through the variables' dictionary
        for key,value in self._vars_dict.copy().items():
            # Delete every other "Cleaner" object
            if isinstance(value,Cleaner) and key in self._vars_dict.keys():
                del self._vars_dict[key]
        # Declare the main hidden attributes
        self._not_delete=not_delete.copy()
        self._excluded=excluded.copy()
        self._flagged=flagged.copy()
        self._name=None
    
    # Update
    def update(self,exclude:str|list[str]|tuple[str]|None=None,include:str|list[str]|tuple[str]|None=None):
        """
        Flags all the new global variables' references that were not manually excluded here or before.
        You can also include previously excluded references.
        
        Arguments
        ---------
        exclude : `str`|`list[str]`|`tuple[str]`|`None`, Optional
            Allows you to exclude a single (`str`) or multiple (`list` or `tuple`) variables.
            `None` by default.
        include : `str`|`list[str]`|`tuple[str]`|`None`, Optional
            Allows you to include a single (`str`) or multiple (`list` or `tuple`) variables. `None` by default.
        """
        # If there are variables to exclude
        if exclude:
            # If "exclude" content is a string
            if isinstance(exclude,str):
                # Make it a list
                exclude=[exclude]
            # Introduce the excluded variables into the corresponding lists
            self._excluded.extend(tuple(var for var in exclude if var not in self._excluded and var not in self._not_delete))
        # If the are excluded variables to include
        if include:
            # If "include" content is a string
            if isinstance(include,str):
                # Make it a list
                include=[include]
            # Loop for "include"
            for var in include:
                # Remove every occurrence of the variables to include from the "excluded" list
                while var in self._excluded:
                    self._excluded.remove(var)
        # Rebuild the "flagged" list
        self._flagged=[var for var in self._vars_dict if var not in self.not_delete and var not in self.excluded]
    
    # Exclude
    def exclude(self,*exclude:str):
        """
        Allows to exclude the desired references from the cleaning process.
        
        Arguments
        ---------
        exclude : `tuple[str]`
            Stream of references to be excluded.
        """
        # Loop for the variables to exclude
        for var in exclude and var not in self._not_delete:
            # Remove from the "flagged" list
            while var in self._flagged:
                self._flagged.remove(var)
            # Introduce variable into the "excluded" list
            if var not in self._excluded:
                self._excluded.append(var)
    
    # Include
    def include(self,*include:str):
        """
        Allows to include the desired references (previously excluded) in the cleaning process.
        
        Arguments
        ---------
        include : `tuple[str]`
            Stream of references to be included.
        """
        # Loop for the variables to "include"
        for var in include and var not in self.not_delete:
            # Introduce variable into the "flagged" list
            if var not in self._flagged:
                self._flagged.append(var)
            # Remove from excluded list
            while var in self._excluded:
                self._excluded.remove(var)
    
    # Include all excluded variables
    def include_all(self,*,exclude:str|list[str]|tuple[str]|None=None):
        """
        Flag all the excluded variables and clear the `excluded` list
        
        Arguments
        ---------
        exclude : `str`|`list[str]`|`tuple[str]`|`None`, Optional
            Variables not to be included into the `flagged` list
        """
        # Introduce excluded variables into the "flagged" list
        self._flagged.extend(self.excluded)
        # Clear the "excluded" list
        self._excluded.clear()
        
        # If the are exceptions
        if exclude:
            # If "exclude" content is a string
            if isinstance(exclude,str):
                # Exclude variable
                self.exclude(exclude)
            # Else
            else:
                # Exclude variables (unpacking)
                self.exclude(*exclude)
    
    # Exclude all flagged variables
    def exclude_all(self,*,include:str|list[str]|tuple[str]|None=None):
        """
        Exclude all the flagged variables and clear the `flagged` list
        
        Arguments
        ---------
        include : `str`|`list[str]`|`tuple[str]`|`None`, Optional
            Variables not to be excluded from the `flagged` list
        """
        # Introduce excluded variables into the "excluded" list
        self._excluded.extend(self.flagged)
        # Clear the "flagged" list
        self._flagged.clear()
        
        # If there are exceptions
        if include:
            # If "include" content is a string
            if isinstance(include,str):
                # Include varianle
                self.include(include)
            # Else
            else:
                # Include variables (unpacking)
                self.include(*include)
    
    # Purge flagged and excluded variables
    def purge(self,*,flagged:bool=True,excluded:bool=True):
        """
        Clears both `flagged` and `excluded` lists from the `Cleaner` object.
        
        Arguments
        ---------
        flagged : `bool`, Optional
            Wether the `flagged` list should be purged (`True`) or not (`False`). `True` by default
        excluded : `bool`, Optional
            Wether the `excluded` list should be purged (`True`) or not (`False`). `True` by default
        """
        # If there is no list to be purged
        if not flagged and not excluded:
            # Pass
            pass
        # If "flagged" is set to be purged
        if flagged:
            # Clear "flagged"
            self._flagged.clear()
        # If "excluded" is set to be purged
        if excluded:
            # Clear "excluded"
            self._excluded.clear()
    
    # Clean
    def clean(self):
        """
        Culminates the cleaning process.
        Erases all the flagged references.
        """
        # Loop for "flagged" list
        for var in self._flagged:
            # If current variable name is in the variables dictionay
            if var in self._vars_dict:
                # Delete variable
                del self._vars_dict[var]
        # Clear "flagged" list
        self._flagged.clear()
    
    #* PROPERTIES
    # Reference pointing to Cleaner object
    @property
    # Getter
    def name(self):
        # If reference is not set or it doesn't point to the "Cleaner" object
        if not self._name or self._vars_dict[self._name] is not self:
            # Loop for variables dictionary
            for key,value in self._vars_dict.items():
                # If current value is the "Cleaner" object
                if value is self:
                    # Store the reference
                    self._name=key
                    # Break
                    break
            # If reference remains empty
            if not self._name:
                # Raise a "ReferenceError"
                raise ReferenceError("\"Cleaner\" object is not referenced")
        # Return the reference
        return self._name
    
    # Variables not to be deleted
    @property
    # Getter
    def not_delete(self):
        # If reference is not in the "not_delete" list
        if self.name not in self._not_delete:
            # Add reference to the "not_delete" list
            self._not_delete.append(self.name)
        # Return a shallow copy of the "not_delete" list
        return self._not_delete.copy()
    #^ No setter
    #^ No deleter
    
    # Excluded variables
    @property
    # Getter
    def excluded(self):
        # Return a shallow copy of the "excluded" list
        return self._excluded.copy()
    #^ No setter
    #^ No deleter
    
    # Flagged variables
    @property
    # Getter
    def flagged(self):
        # Return a shallow copy of the "flagged" list
        return self._flagged.copy()
    #^ No setter
    #^ No deleter
    
    #* SCREEN DUNDER METHODS
    # __str__
    def __str__(self):
        # Return a string with the instance's components
        return f"""
        Flagged: {self.flagged}
        
        Excluded: {self.excluded}
        
        Not delete: {self.not_delete}
        """
    
    # __repr__
    def __repr__(self):
        # Return a string able to rebuild the instance if needed
        return f"{self.__class__.__name__}(not_delete={self.not_delete},excluded={self.excluded},flagged={self.flagged})"