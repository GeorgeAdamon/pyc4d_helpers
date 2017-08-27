# List of all the possible datatypes of Cinema4D UserData
Retrieved from https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/index.html#c4d.GetCustomDataTypeDefault

Usage example (Boolean UserData creation):

    BaseContainer = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BOOL) #Set the UserData type
    BaseContainer[c4d.DESC_NAME] = MyBoolData #Set the UserData name
    
    userdatum = obj.AddUserData(BaseContainer) #Add the UserData to the object
    obj[userdatum] = True  #Set the UserData value
    
    c4d.EventAdd() #Notify Cinema4D
___

## UserData types
| SDK name | Common UserData name in C4D GUI |
|-----------| :---------: |
__DTYPE_BASELISTLINK__   |   _BaseList2D_ 
__DTYPE_BOOL__          |    _bool_ 
__DTYPE_BUTTON__	    |   _Button_
__DTYPE_CHILDREN__	    |   _Children_
__DTYPE_COLOR__	        |   _Color_
__DTYPE_DYNAMIC__	    |   _GV dynamic_
__DTYPE_FILENAME__	    |   _str_
__DTYPE_GROUP__	        |   _Group_
__DTYPE_LONG__	        |   _long_
__DTYPE_MATRIX__	    |   _Matrix_
__DTYPE_MULTIPLEDATA__  |   _Multiple data entry_
__DTYPE_NONE__	        |   _None_
__DTYPE_NORMAL__	    |   _Normal_
__DTYPE_POPUP__	        |   _Popup_
__DTYPE_REAL__	        |   _float_
__DTYPE_SEPARATOR__ 	|   _Separator_
__DTYPE_STATICTEXT__	|   _Static text_
__DTYPE_STRING__	    |   _str_
__DTYPE_SUBCONTAINER__	|   _BaseContainer_
__DTYPE_TEXTURE__	    |   _Texturename_
__DTYPE_TIME__	        |   _BaseTime_
__DTYPE_VECTOR__	    |   _Vector_
