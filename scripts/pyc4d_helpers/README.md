
# pyc4d_helpers

## Dictionaries

## Hierarchy

## Materials

## UserData
### Creation
* **CreateUserData (**_obj, itemName, itemtype, overwrite=False_**)<br/>
* **CreateFloatData (**_obj, itemName="Float", interface=c4d.CUSTOMGUI_REAL, _min=None, _max = None, step=0.01,  units="Real", overwrite=False_**)<br/>
* **CreateIntegerData (**obj, itemName="Integer", interface=c4d.CUSTOMGUI_LONG, _min=None, _max = None, step=1, overwrite=False)
* **CreateDropDown (**obj, itemName="DropDown", interface=c4d.CUSTOMGUI_CYCLE, data = ["A", "B", "C"], overwrite=False)
* **CreateButton (**obj, itemName="Buton", overwrite=False)
* **CreateFilepath(**obj, itemName = "Filepath", overwrite = False)
### Access
* #### GetAllUserData(obj)
* #### UserDataExists(obj, itemName)
* #### FindUserData (obj, itemName)
### Value Set/Get
* #### GetUserDataValue(obj, itemName)
* #### SetUserDataValue (obj, itemName, value)
### Destruction
* #### DestroyUserData(obj, itemName)
* #### DestroyAllUserData(obj)
