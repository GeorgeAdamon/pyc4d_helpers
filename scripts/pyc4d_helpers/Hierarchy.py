import c4d

def SelectObject(obj):
    obj.SetBit(c4d.BIT_ACTIVE)
    return

def DeselectObject(obj):
    obj.DelBit(c4d.BIT_ACTIVE)
    return

def SelectChildren(obj, recursive = True, deselect_parent = True):
    if recursive:
        doc.StartUndo()
        SelectChildren_RecursionHelper(obj,obj.GetNext())

        if deselect_parent:
            DeselectObject(obj)
            doc.EndUndo()
    else:
        doc.StartUndo()
        SelectChildren_Helper(obj,obj.GetNext())

        if deselect_parent:
            DeselectObject(obj)

        doc.EndUndo()
    return

def SelectChildren_RecursionHelper(obj, next):
    while obj and obj != next: #while we are not in the end of this object's hierarchy

        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj)  

        SelectObject(obj) #select the current object

        SelectChildrenHelper(obj.GetDown(),next)  #Call this same function on the first child of the current object, if it exists. This initiates a recursive chain reaction, until we reach the end of this object's hierarchy

        obj = obj.GetNext()  #Get the next object in the hierarchy

    c4d.EventAdd()

    return True

def SelectChildren_Helper(obj, next):
    obj2 = obj.GetDown()

    while obj2 and obj2 != next: #while we are not in the end of this object's hierarchy

        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj2)

        SelectObject(obj2) #select the current object

        obj2 = obj2.GetNext()  #Get the next object in the hierarchy

    c4d.EventAdd()

    return True
