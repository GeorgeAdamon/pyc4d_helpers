import c4d

def SelectObject(obj):
	obj.SetBit(c4d.BIT_ACTIVE)
	return

def DeselectObject(obj):
	obj.DelBit(c4d.BIT_ACTIVE)
	return