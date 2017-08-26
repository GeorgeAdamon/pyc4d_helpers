import c4d

def FindUserData (obj, itemName):

    """ 
    Search the UserData Collection of a Cinema4D object for a single item with the provided name.
    
    Args:
        obj: The Cinema4D object to examine
        itemName: The name of the UserData to search for
    
    Returns:
        If an item with the specified name exists, the function returns the value/object contained in that time. 
        If no item is found it returns None.
     """
    
    UserData = obj.GetUserDataContainer()
    
    if UserData:
        for ud in UserData:
            if ud[1][c4d.DESC_NAME] == itemName:
                return obj[ud[0]] #The actual object contained in the UserData item
            else:
                return None
    else:
        return None