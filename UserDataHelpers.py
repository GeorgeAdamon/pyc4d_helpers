import c4d

def FindUserData (obj, itemName):

    """ 
    Search the UserData Collection of a Cinema4D object for a single item with the provided name.
    
    Args:
        obj (c4d.BaseObject): The Cinema4D object to examine
        itemName (string): The name of the UserData to search for
    
    Returns:
        If an item with the specified name exists, the function returns the value/object contained in that time. 
        If no item is found it returns None.
     """
    if obj==None: return
    UserData = obj.GetUserDataContainer()
    
    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                return obj[ud[0]] #The actual object contained in the UserData item
            else:
                return None
    else:
        return None

    def CreateUserData (obj, itemName, itemtype, value=None):

    """ 
    Create a new UserData item and add it to the UserDataContainer of the specified object.
    
    Args:
        obj (c4d.BaseObject): The Cinema4D object to add UserData to.
        itemName (string): The name of the UserData item to be created.
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
        value: Optional value of the UserData item
    Returns:
        True on success, False on failure
     """
    if obj==None: return False
    if itemtype==None: itemtype = c4d.NONE
    if itemName == None: itemName = "No Name"

    BaseContainer[c4d.DESC_NAME] = itemName
    BaseContainer = c4d.GetCustomDataTypeDefault(itemtype)
    
    item = obj.AddUserData(BaseContainer)
    obj[item] = value
    c4d.EventAdd()

    return True