import c4d
import math
from pyc4d_helpers import UserData as ud
from pyc4d_helpers import Matrices as mtr

# ==========================  GLOBAL VARIABLES  ============================== #

matrices = []
fileContainsHeaders = True
filePath = ""
fileName = ""
isQuad = True
size = 1
mesh = c4d.PolygonObject(0,0)

# ==========================  CACHED FUNCTIONS  ============================== #

# The function that converts a transformation matrix from the Rhino/Grasshopper
# format, to the Cinema4D format.
Rh2C4d = mtr.RhinoMatrix_2_C4DMatrix


# ==============================  UI SETUP  ================================== #

def SetupUserData():
    #1.1: UI Header
    if not ud.UserDataExists(op,"File Handling"):
        ud.CreateUserData(op,"File Handling", c4d.DTYPE_SEPARATOR)

    #1.2: "Filename" text box
    if not ud.UserDataExists(op,"Transformation Matrices File"):
        ud.CreateUserData(op, "Transformation Matrices File", c4d.DTYPE_FILENAME)

    #1.3
    if not ud.UserDataExists(op, "Data Has Headers"):
        ud.CreateUserData(op, "Data Has Headers", c4d.DTYPE_BOOL)

    #2.1: UI Header
    if not ud.UserDataExists(op,"Display"):
        ud.CreateUserData(op,"Display", c4d.DTYPE_SEPARATOR)

    #2.2: "Object Type" text box
    if not ud.UserDataExists(op,"Display Matrices As"):
        ud.CreateDropDown (op, "Display Matrices As", c4d.CUSTOMGUI_CYCLE, ["Quad", "Triangle"])

    #2.3: "Display Size" slider
    if not ud.UserDataExists(op,"Display Size"):
        ud.CreateFloatData (op, "Display Size", "Float Slider", 0, 100, 0.01, "Meters")

    #3.1: UI Header
    if not ud.UserDataExists(op,"Pipeline"):
        ud.CreateUserData(op,"Pipeline", c4d.DTYPE_SEPARATOR)

    #3.2: "Filename" text box
    if not ud.UserDataExists(op,"Attach to Cloner"):
        ud.CreateUserData(op, "Attach to Cloner", c4d.DTYPE_BASELISTLINK )

def ReadUserData():
    global fileContainsHeaders
    global filePath
    global fileName
    global isQuad
    global size

    fileContainsHeaders = ud.GetUserDataValue(op, "Data Has Headers")
    filePath = ud.GetUserDataValue(op, "Transformation Matrices File")
    fileName = os.path.basename(filepath).split(".")[0]
    isQuad = ud.GetUserDataValue(op, "Display Matrices As") == "Quad"
    size =  ud.GetUserDataValue(op, "Display Size")

def ReadFile(filepath, headers = True, color = None):
    """
    Reads a CSV (Comma-Separated-Values) file that contains transformation 
    matrices. The 4X4_Matrix values as they come from Rhino/Grasshopper,
    should be in a 1D list of 16 elements, structured like that:
    | M00 | M01 | M02 | M03 | M10 | M11 | M12 | M13 |M20 | M21 | M22 | M23 | M30 | M31 | M32 | M33 |

    Those values correspond to a 4X4 matrix, that was originally structured like that:
    | M00 | M01 | M02 | M03 |
    | M10 | M11 | M12 | M13 |
    | M20 | M21 | M22 | M23 |
    | M30 | M31 | M32 | M33 |

    and the meaning of it was :
    | X_Direction.X | X_Direction.Y | X_Direction.Z | X_Pos |
    | Y_Direction.X | Y_Direction.Y | Y_Direction.Z | Y_Pos |
    | Z_Direction.X | Z_Direction.Y | Z_Direction.Z | Z_Pos |
    |       0       |       0       |       0       |   1   |

    where X_Direction is the direction of the X Axis (red) of the object,
    Y_Direction is the direction of the Y Axis (green) of the objects,
    Z_Direction is the direction of the Z Axis (blue) of the object,
    and X_Pos,Y_Pos,Z_Pos are the coordinates of the object in World Space

    """

    _matrices = []

    with open(filepath, 'r') as f:
        # Skip the first line because it contains headers
        if headers:
            _matrices = map( Rh2C4d, [ [float(v) for v in line.split(',')] for line in f.readlines()[1:] ] )
        else:
            _matrices = map( Rh2C4d, [ [float(v) for v in line.split(',')] for line in f.readlines() ] ) 

    return _matrices          

def SetupNames():
    global fileName
    op.SetName("Rhino Matrix Loader: " + fileName)

# ============================ UTILITY FUNCTIONS ============================= #
def Centroid(points):
    c = c4d.Vector(0,0,0)
    for p in points:
        c += p
    c = c/len(points)
    return c

def PolarToCartesian(angle, radius, plane= "XZ"):
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    if plane == "XZ":
        return c4d.Vector(x,y,0)
    elif plane == "XY":
        return c4d.Vector(x,0,z)
    else:
        return c4d.Vector(0,y,x)

def CreateRectangleVertices(size):
    a = c4d.Vector(-size,-size,0 )
    b = c4d.Vector(size,-size,0 )
    c = c4d.Vector(size,size,0 )
    d = c4d.Vector(-size,size,0)
    return a,b,c,d

def CreateTriangleVertices(size):
    a_angle = math.radians(90)
    b_angle = math.radians(210)
    c_angle = math.radians(330)

    a = PolarToCartesian(a_angle,size)
    b = PolarToCartesian(b_angle,size)
    c = PolarToCartesian(c_angle,size)
    return a,b,c

def TransformVertices(_vertices, matrix):
    return [matrix*v for v in _vertices]

# ============================ MESHING FUNCTIONS ============================= #

def GenerateMeshFromMatrices(_matrices, _size = 1, _quad = True):

    # QUAD MESH
    if _quad == 0:
        verticesPerFace = 4
        baseVertices = CreateRectangleVertices(_size)
    # TRIANGLE MESH
    else:
        verticesPerFace = 3
        baseVertices = CreateTriangleVertices(_size)

    # Setup List Counts
    matrixCount = len(_matrices)
    faceCount = matrixCount
    vertexCount = faceCount * verticesPerFace

    # Setup Mesh Lists
    mesh = c4d.PolygonObject(vertexCount, faceCount)
    vertices = [] * vertexCount
    faces = [] * faceCount


    # Iterate through the matrices and transform the vertices accordingly
    for i,m in enumerate(_matrices):
        cnt = i * verticesPerFace
        
        if _quad:
            vertices[cnt : cnt + 4] = TransformVertices(baseVertices, m)
            faces[i] = c4d.CPolygon( cnt+0, cnt+1, cnt+2, cnt+3)
        else:
            vertices[cnt : cnt + 3] = TransformVertices(baseVertices, m)
            faces[i] = c4d.CPolygon( cnt+0, cnt+1, cnt+2)

    # Translate the matrix of the mesh object to the centroid of the vertices
    centroid = Centroid(vertices)
    mesh.SetAbsPos(centroid)

    # Translate the vertices back to their original positions
    vertices = [v-centroid for v in vertices]

    # Set the mesh vertices
    mesh.SetAllPoints(verts)

    # Set the mesh faces
    for i,f in enumerate(faces):
        mesh.SetPolygon(i,f)

    # Update the object
    mesh.Message (c4d.MSG_UPDATE)

def main():
    global matrices
    global fileContainsHeaders
    global size
    global isQuad

    SetupUserData()

    ReadUserData()

    matrices = ReadFile(filePath, fileContainsHeaders)

    SetupNames()

    return GenerateMeshFromMatrices(matrices, size, isQuad)


