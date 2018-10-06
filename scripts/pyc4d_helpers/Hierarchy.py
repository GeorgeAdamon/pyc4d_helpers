import c4d
import c4d.documents as docs

global DOC
DOC = docs.GetActiveDocument()


def SelectObject(obj):
    """
    Selects the specified object in the Hierarchy.
    """
    obj.SetBit(c4d.BIT_ACTIVE)
    return

def DeselectObject(obj):
    """
    Deselects the specified object from the Hierarchy.
    """
    obj.DelBit(c4d.BIT_ACTIVE)
    return

def SelectChildren(obj, recursive = True, deselect_parent = True):
    """
    Recursively selects all the children of the specified object
    """
    if recursive:
        DOC.StartUndo()
        SelectChildren_RecursionHelper(obj,obj.GetNext())

        if deselect_parent:
            DeselectObject(obj)
            DOC.EndUndo()
    else:
        DOC.StartUndo()
        SelectChildren_Helper(obj,obj.GetNext())

        if deselect_parent:
            DeselectObject(obj)
        else:
            SelectObject(obj)

        DOC.EndUndo()
    return

def DeleteChildren(obj):
    """
    Deletes all the immediate children of the specified object.
    """
    children = obj.GetChildren()

    for child in children:
        child.Remove()

# ============== HELPER FUNCTIONS ================
def SelectChildren_RecursionHelper(obj, next):
    while obj and obj != next: #while we are not in the end of this object's hierarchy

        DOC.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj)  

        SelectObject(obj) #select the current object

        SelectChildren_RecursionHelper(obj.GetDown(),next)  #Call this same function on the first child of the current object, if it exists. This initiates a recursive chain reaction, until we reach the end of this object's hierarchy

        obj = obj.GetNext()  #Get the next object in the hierarchy

    c4d.EventAdd()

    return True

def SelectChildren_Helper(obj, next):
    obj2 = obj.GetDown()

    while obj2 and obj2 != next: #while we are not in the end of this object's hierarchy

        DOC.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj2)

        SelectObject(obj2) #select the current object

        obj2 = obj2.GetNext()  #Get the next object in the hierarchy

    c4d.EventAdd()

    return True
