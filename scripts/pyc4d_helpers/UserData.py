import pyc4d_helpers.Dictionaries as D
import c4d

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
    UserData = obj.GetUserDataContainer()
    
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
    UserData = obj.GetUserDataContainer()

    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                return ud #The actual object contained in the UserData item
    return None

def GetUserDataValue (obj, itemName):
    ud = FindUserData(obj,itemName)
    return obj[ud[0]]
 
def DestroyUserData(obj, itemName):

    if obj==None: return False
    UserData = obj.GetUserDataContainer()
    
    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                obj.RemoveUserData(ud[0]) #The actual object contained in the UserData item
                #c4d.EventAdd()

                return True
                
    return False

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
    if itemName == None: itemName = "No Name " + str(len(UserData))

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
    #c4d.EventAdd()

    return obj[item]

def CreateFloatData (obj, itemName, itemtype=c4d.CUSTOMGUI_REAL, _min=0.0, _max = 100.0, step=1,  units=c4d.DESC_UNIT_FLOAT, overwrite= False):
    if obj==None: return False

    if isinstance(itemtype,str):
        itemtype = D.FloatInterface[itemtype]
    
    if isinstance(units,str):
        units = D.FloatUnits[units]

    UserData = obj.GetUserDataContainer()
    if itemName == None: itemName = "No Name " + str(len(UserData))

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

    BaseContainer[c4d.DESC_CUSTOMGUI] = itemtype
    BaseContainer[c4d.DESC_UNIT] = units


    item = obj.AddUserData(BaseContainer)
    #c4d.EventAdd()

    return True

def CreateIntegerData (obj, itemName, itemtype=c4d.CUSTOMGUI_LONG, _min=0, _max = 100, step=1, overwrite= False):
    if obj==None: return False

    if isinstance(itemtype,str):
        itemtype = D.IntegerInterface[itemtype]
     
    UserData = obj.GetUserDataContainer()

    if itemName == None: itemName = "No Name " + str(len(UserData))

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

    BaseContainer[c4d.DESC_CUSTOMGUI] = itemtype
    BaseContainer[c4d.DESC_UNIT] = c4d.DESC_UNIT_LONG

    item = obj.AddUserData(BaseContainer)
    #c4d.EventAdd()

    return True

def SetUserData (obj, itemName, value):
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
    
    UserData = obj.GetUserDataContainer()
    
    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                obj[ud[0]] = value
                #c4d.EventAdd()
                return True
    return False

