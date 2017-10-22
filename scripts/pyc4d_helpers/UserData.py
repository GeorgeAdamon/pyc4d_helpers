import pyc4d_helpers.Dictionaries as D
import c4d


# ===================== USER DATA CREATION FUNCTIONS ============================================ #
def CreateUserData (obj, itemName, itemtype, overwrite=False):

    """ 
    Create a new UserData item and add it to the UserDataContainer of the specified object.

    Args:
        obj (c4d.BaseObject): The Cinema4D object to add UserData to.
        itemName (str): The name of the UserData item to be created.
        itemtype: The data type of the UserData item to be created. Available DataTypes:
            c4d.DTYPE_BASELISTLINK  (BaseList2D).
            c4d.DTYPE_BOOL  (bool).
            c4d.DTYPE_BUTTON    (Button).
            c4d.DTYPE_CHILDREN  (Children).
            c4d.DTYPE_COLOR (Color).
            c4d.DTYPE_DYNAMIC   (GV dynamic).
            c4d.DTYPE_FILENAME  (str).
            c4d.DTYPE_GROUP (Group).
            c4d.DTYPE_LONG  (long).
            c4d.DTYPE_MATRIX    (Matrix)
            c4d.DTYPE_MULTIPLEDATA  (Multiple data entry).
            c4d.DTYPE_NONE  (None).
            c4d.DTYPE_NORMAL    (Normal).
            c4d.DTYPE_POPUP (Popup).
            c4d.DTYPE_REAL  (float)
            c4d.DTYPE_SEPARATOR (Separator).
            c4d.DTYPE_STATICTEXT    (Static text).
            c4d.DTYPE_STRING    (str).
            c4d.DTYPE_SUBCONTAINER  (BaseContainer).
            c4d.DTYPE_TEXTURE   (Texturename).
            c4d.DTYPE_TIME  (BaseTime).
            c4d.DTYPE_VECTOR    (Vector).
        overwrite: Whether to overwrite any existing UserData with same name. False by default
    Returns:
        True on success, False on failure
     """
    if obj==None: return
    if itemtype==None: itemtype = c4d.NONE
    
    UserData = obj.GetUserDataContainer()
    if itemName == None: itemName = "User Data" + str(len(UserData))

    if UserDataExists(obj,itemName):
        if overwrite==False: 
            return
        else:
            DestroyUserData(obj,itemName)

    BaseContainer = c4d.GetCustomDatatypeDefault(itemtype)
    BaseContainer[c4d.DESC_NAME] = itemName
    BaseContainer[c4d.DESC_SHORT_NAME] = itemName

    if itemtype==c4d.DTYPE_BUTTON:
        BaseContainer[c4d.DESC_CUSTOMGUI] =  c4d.CUSTOMGUI_BUTTON

    if itemtype==c4d.DTYPE_SEPARATOR:
        BaseContainer[c4d.DESC_CUSTOMGUI] =  c4d.CUSTOMGUI_SEPARATOR

    item = obj.AddUserData(BaseContainer)

    return True

def CreateFloatData (obj, itemName="Float", interface=c4d.CUSTOMGUI_REAL, _min=0.0, _max = 1.0, step=0.01,  units="Real", overwrite=False):
    """
    Create a new UserData item of type "Float" and add it to the UserDataContainer of the specified object.

    Args:
        obj (c4d.BaseObject): The Cinema4D object to add UserData to.
        [optional] itemName (str): The name of the UserData item to be created. Default is "Float".
        [optional] interface (str): The type of the User Interface to implement for this User Data item. Can be "Float" , "Float Slider" or "Float Slider No EditField" . Default is "Float".
        [optional] _min (float): The minimum allowed value for this UserData item. 0.0 by default.
        [optional] _max (float): The maximum allowed value for this UserData item. 1.0 by default.
        [optional] _step (float): The step value for each UI nudge. 0.01 by default.
        [optional] units (str or int): The units in which the float value is expressed. Can be "Real", "Percent", "Degrees" or "Meters". "Real" by default.
        [optional] overwrite: Whether to overwrite any existing identical UserData. False by default.
    Returns:
        True on success, False on failure
    """

    if obj==None: return False

    if isinstance(interface,str):
        interface = D.FloatInterface[interface]
    
    if isinstance(units,str):
        units = D.FloatUnits[units]

    if UserDataExists(obj,itemName):
        if overwrite==False: 
            return False
        else:
            DestroyUserData(obj,itemName)

    BaseContainer = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    BaseContainer[c4d.DESC_NAME] = itemName
    BaseContainer[c4d.DESC_SHORT_NAME] = itemName

    BaseContainer[c4d.DESC_MIN] = _min
    BaseContainer[c4d.DESC_MAX] = _max
    BaseContainer[c4d.DESC_STEP] = step

    BaseContainer[c4d.DESC_CUSTOMGUI] = interface
    BaseContainer[c4d.DESC_UNIT] = units

    item = obj.AddUserData(BaseContainer)

    return True

def CreateIntegerData (obj, itemName="Integer", interface=c4d.CUSTOMGUI_LONG, _min=0, _max = 100, step=1, overwrite=False):

    """
    Create a new UserData item of type "Integer" and add it to the UserDataContainer of the specified object.

    Args:
        obj (c4d.BaseObject): The Cinema4D object to add UserData to.
        [optional] itemName (str): The name of the UserData item to be created. Default is "Integer".
        [optional] interface (str or int): The type of the User Interface to implement for this User Data item. Can be "Cycle" , "Cycle Button" , "Integer" or "Integer Slider". Default is "Integer"
        [optional] _min (float): The minimum allowed value for this UserData item. 0.0 by default.
        [optional] _max (float): The maximum allowed value for this UserData item. 1.0 by default.
        [optional] _step (float): The step value for each UI nudge. 0.01 by default.
        [optional] units (str): The units in which the float value is expressed. Can be "Real" , "Percent" , "Degrees" or "Meters". "Real" by default.
        [optional] overwrite: Whether to overwrite any existing identical UserData. False by default.
    Returns:
        True on success, False on failure
    """

    if obj==None: return False

    if isinstance(interface,str):
        interface = D.IntegerInterface[interface]
     
    UserData = obj.GetUserDataContainer()

    if UserDataExists(obj,itemName):
        if overwrite==False: 
            return False
        else:
            DestroyUserData(obj,itemName)

    BaseContainer = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    BaseContainer[c4d.DESC_NAME] = itemName
    BaseContainer[c4d.DESC_SHORT_NAME] = itemName

    BaseContainer[c4d.DESC_MIN] = _min
    BaseContainer[c4d.DESC_MAX] = _max
    BaseContainer[c4d.DESC_STEP] = step

    BaseContainer[c4d.DESC_CUSTOMGUI] = interface
    BaseContainer[c4d.DESC_UNIT] = c4d.DESC_UNIT_LONG

    item = obj.AddUserData(BaseContainer)

    return True

def CreateButton (obj, itemName="Buton", overwrite=False):

    """
    Create a new UserData item of type "Button" and add it to the UserDataContainer of the specified object.

    Args:
        obj (c4d.BaseObject): The Cinema4D object to add UserData to.
        [optional] itemName (str): The name of the UserData item to be created. Default is "Button".
        [optional] overwrite: Whether to overwrite any existing identical UserData. False by default.
    Returns:
        True on success, False on failure
    """

    if obj==None: return False

    UserData = obj.GetUserDataContainer()

    if itemName == None: itemName = "Button" + str(len(UserData))

    if UserDataExists(obj,itemName):
        if overwrite==False: 
            return False
        else:
            DestroyUserData(obj,itemName)

    BaseContainer = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BUTTON)
    BaseContainer[c4d.DESC_NAME] = itemName
    BaseContainer[c4d.DESC_SHORT_NAME] = itemName
    BaseContainer[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_BUTTON

    item = obj.AddUserData(BaseContainer)

    #Do NOT call c4d.EventAdd() if you use this function inside a Python Generator object, or inside a Python tag. Strange things will happen.
    #if not ( op.GetType() == 1023866 or op.GetType()== 1022749 ):
    #    c4d.EventAdd()

    return True


# ===================== USER DATA SEARCH FUNCTIONS ============================================== #
def GetAllUserData(obj):
    return obj.GetUserDataContainer()

def UserDataExists(obj, itemName):
    """ 
    Search the UserData Collection of a Cinema4D object for a single item with the provided name.
    
    Args:
        obj (c4d.BaseObject): The Cinema4D object to examine
        itemName (str): The name of the UserData to search for
    
    Returns:
        True if an item with the specified name exists,
        False if an item with the specified name does not exist,
        None if the object is not valid
     """
    if obj==None: return None
    UserData = GetAllUserData(obj)
    
    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                return True
    return False

def FindUserData (obj, itemName):

    """ 
    Search the UserData Collection of a Cinema4D object for a single item with the provided name, and retrieve it.
    
    Args:
        obj (c4d.BaseObject): The Cinema4D object to examine
        itemName (str): The name of the UserData to search for
    
    Returns:
        If an item with the specified name exists, the function returns the value/object contained in that time. 
        If no item is found it returns None.
     """
    if obj==None: return
    UserData = GetAllUserData(obj)

    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                return ud #The actual object contained in the UserData item
    return None


# ===================== USER DATA VALUE ASSIGNMENT FUNCTIONS ==================================== #
def GetUserDataValue (obj, itemName):
    ud = FindUserData(obj,itemName)
    return obj[ud[0]]

def SetUserDataValue (obj, itemName, value):

    """ 
    Sets the value of a UserData item of a Cinema4D object

    Args:
        obj (c4d.BaseObject): The Cinema4D object whose data to alter.
        itemName(str): The name of the UserData item to be altered.
        value: The value or object to set. 
    Returns:
        True on success,
        False on failure
    """

    if obj==None: return False
    
    UserData = GetAllUserData(obj)
    
    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                obj[ud[0]] = value

                #Do NOT call c4d.EventAdd() if you use this function inside a Python Generator object, or inside a Python tag. Strange things will happen.
                #if not ( op.GetType() == 1023866 or op.GetType()== 1022749 ):
                #    c4d.EventAdd()

                return True
    return False


# ===================== USER DATA DESTRUCTION FUNCTIONS ========================================= #
def DestroyUserData(obj, itemName):

    if obj==None: return False

    UserData = GetAllUserData(obj)
    if UserData==None: return False

    if UserData:
        for i,ud in enumerate(UserData):
            if ud[1][c4d.DESC_NAME] == itemName:
                obj.RemoveUserData(i) #The actual object contained in the UserData item
                return True

def DestroyAllUserData(obj, itemName):

    if obj==None: return False

    UserData = GetAllUserData(obj)
    if UserData==None: return False

    for i,ud in enumerate(UserData):
        obj.RemoveUserData(i)

    return True
