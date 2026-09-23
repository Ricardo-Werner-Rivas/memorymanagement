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
from sys import modules

#* MAIN CLASS
# Class "Cleaner"
class Cleaner:
    #& Code comments
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
        not_delete : `list[str]`, Optional
            List of variables to never be deleted. It takes the list of global variables of the main module by default.
        excluded : `list[str]`, Optional
            List of variables to be excluded from the memory cleaning process. Empty list by default.
        flagged : `list[str]`, Optional
            List of variables to be erased from memory. Empty list by default.
        """
        if not not_delete:
            not_delete=list(vars(modules["__main__"]))
        for key,value in vars(modules["__main__"]).copy().items():
            if isinstance(value,Cleaner) and key in vars(modules["__main__"]).keys():
                del vars(modules["__main__"])[key]
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
        if exclude:
            if isinstance(exclude,str):
                exclude=[exclude]
            self._excluded.extend([var for var in exclude if var not in self._excluded])
        if include:
            if isinstance(include,str):
                include=[include]
            for var in include:
                while var in self._excluded:
                    self._excluded.remove(var)
        self._flagged=[var for var in list(vars(modules["__main__"]))if var not in self.not_delete and var not in self.excluded]
    
    # Exclude
    def exclude(self,*exclude:str):
        """
        Allows to exclude the desired references from the cleaning process.
        
        Arguments
        ---------
        exclude : `tuple[str]`
            Stream of references to be excluded.
        """
        for var in exclude:
            while var in self._flagged:
                self._flagged.remove(var)
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
        for var in include:
            if var not in self._flagged:
                self._flagged.append(var)
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
        self._flagged.extend(self.excluded)
        self._excluded.clear()
        
        if exclude:
            if isinstance(exclude,str):
                self.exclude(exclude)
            else:
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
        self._excluded.extend(self.flagged)
        self._flagged.clear()
        
        if include:
            if isinstance(include,str):
                self.include(include)
            else:
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
        if not flagged and not excluded:
            pass
        if flagged:
            self._flagged.clear()
        if excluded:
            self._excluded.clear()
    
    # Clean
    def clean(self):
        """
        Culminates the cleaning process.
        Erases all the flagged references.
        """
        for var in self._flagged:
            if var in list(vars(modules["__main__"])):
                del vars(modules["__main__"])[var]
        self._flagged.clear()
    
    #* PROPERTIES
    # Variables not to be deleted
    @property
    # Getter
    def not_delete(self):
        if not self._name or vars(modules["__main__"])[self._name] is not self:
            for key,value in vars(modules["__main__"]).items():
                if value is self:
                    self._name=key
                    self._not_delete.append(self._name)
                    break
                else:
                    self._name=None
            if not self._name:
                raise ReferenceError("'Cleaner' object is not referenced")
        elif self._name not in self._not_delete:
            self._not_delete.append(self._name)
        return self._not_delete
    #^ No setter
    #^ No deleter
    
    # Excluded variables
    @property
    # Getter
    def excluded(self):
        return self._excluded
    #^ No setter
    #^ No deleter
    
    # Flagged variables
    @property
    # Getter
    def flagged(self):
        return self._flagged
    #^ No setter
    #^ No deleter
    
    #* SCREEN DUNDER METHODS
    # __str__
    def __str__(self):
        return f"""
        Flagged: {self.flagged}
        
        Excluded: {self.excluded}
        
        Not delete: {self.not_delete}
        """
    
    # __repr__
    def __repr__(self):
        return f"{self.__class__.__name__}(not_delete={self.not_delete},excluded={self.excluded},flagged={self.flagged})"