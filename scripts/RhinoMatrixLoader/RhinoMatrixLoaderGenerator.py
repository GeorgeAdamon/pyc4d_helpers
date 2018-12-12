import c4d
from pyc4d_helpers import UserData as ud
from pyc4d_helpers import Matrices as mtr

# ====================== UI FUNCTIONS ======================================= #
def SetupUserData():
    #1.1: UI Header
    if not ud.UserDataExists(op,"File Handling"):
        ud.CreateUserData(op,"File Handling", c4d.DTYPE_SEPARATOR)

    #1.2: "Filename" text box
    if not ud.UserDataExists(op,"First Object FileName"):
        ud.CreateUserData(op, "Transformation Matrices File", c4d.DTYPE_FILENAME)

    #1.3
    if not ud.UserDataExists(op, "Data Has Headers"):
        ud.CreateUserData(op, "Data Has Headers", c4d.DTYPE_BOOL)

    #2.1: UI Header
    if not ud.UserDataExists(op,"Display"):
        ud.CreateUserData(op,"Display", c4d.DTYPE_SEPARATOR)

    #2.2: "Object Type" text box
    if not ud.UserDataExists(op,"Display Matrices As"):
        ud.CreateDropDown (op, "Display Matrices As", c4d.CUSTOMGUI_CYCLE, ["Rectangle", "Disc", "Guide"])

    #2.3: "Display Size" slider
    if not ud.UserDataExists(op,"Display Size"):
        ud.CreateFloatData (op, "Display Size", "Float Slider", 0, 100, 0.01, "Meters")

    #3.1: UI Header
    if not ud.UserDataExists(op,"Pipeline"):
        ud.CreateUserData(op,"Pipeline", c4d.DTYPE_SEPARATOR)

    #3.2: "Filename" text box
    if not ud.UserDataExists(op,"Attach to Cloner"):
        ud.CreateUserData(op, "Attach to Cloner", c4d.DTYPE_BASELISTLINK )


def main():
    SetupUserData()
