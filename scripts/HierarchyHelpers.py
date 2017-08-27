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
    	SelectChildrenHelper(obj,obj.GetNext())

    	if deselect_parent:
    		DeselectObject(obj)

   		doc.EndUndo()
   	else:


def SelectChildren_RecursionHelper(obj, next):
	
	while obj and obj != next: #while we are not in the end of this object's hierarchy

        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj)

        SelectObject(obj) #select the current object

        SelectChildrenHelper(obj.GetDown(),next)  #Call this same function on the first child of the current object, if it exists. This initiates a recursive chain reaction, until we reach the end of this object's hierarchy

        obj = obj.GetNext()  #Get the next object in the hierarchy

    c4d.EventAdd()

    return True

def SelectChildren_Helper(obj, next):
	
	while obj and obj != next: #while we are not in the end of this object's hierarchy

        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SMALL,obj)

        SelectObject(obj) #select the current object

        SelectChildrenHelper(obj.GetDown(),next)  #Call this same function on the first child of the current object, if it exists. This initiates a recursive chain reaction, until we reach the end of this object's hierarchy

        obj = obj.GetNext()  #Get the next object in the hierarchy

    c4d.EventAdd()

    return True