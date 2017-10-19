import c4d
import os
import re
import math
import random
from pyc4d_helpers import UserData as ud
from pyshull import pyshull as hull

minX = 1000000000000.0
minY = 1000000000000.0
minZ = 1000000000000.0

maxX = 0.0
maxY = 0.0
maxZ = 0.0

#op[c4d.TPYTHON_FRAME] = True


shader = c4d.BaseList2D(c4d.Xvertexmap)
Polygon = c4d.BaseObject(c4d.Opolygon)

### GENERATOR FUNCTIONS
def SetupUserData():
    #1
    if not ud.UserDataExists(op,"File Handling"):
        ud.CreateUserData(op,"File Handling", c4d.DTYPE_SEPARATOR, True)
    #2
    if not ud.UserDataExists(op,"First Object FileName"):
        ud.CreateUserData(op,"First Object FileName", c4d.DTYPE_FILENAME, True)
    #3
    if not ud.UserDataExists(op,"First Frame"):
        ud.CreateIntegerData(op,"First Frame", "Integer", 0,100,1)
    #4
    if not ud.UserDataExists(op,"Last Frame"):
        ud.CreateIntegerData(op,"Last Frame", "Integer", 0,100,1)
    #5
    if not ud.UserDataExists(op,"Frame Step"):
        ud.CreateIntegerData(op,"Frame Step", "Integer Slider", 1,100,1)
        ud.SetUserData(op, "Frame Step", 1)
    #6
    if not ud.UserDataExists(op,"File Handling Message"):
        ud.CreateUserData(op,"File Handling Message", c4d.DTYPE_STATICTEXT, True)
    #7
    if not ud.UserDataExists(op,"Mesh Handling"):
        ud.CreateUserData(op,"Mesh Handling", c4d.DTYPE_SEPARATOR, True)
    #8
    if not ud.UserDataExists(op,"Swap Y/Z"):
        ud.CreateUserData(op,"Swap Y/Z", c4d.DTYPE_BOOL, True)
    #9
    if not ud.UserDataExists(op,"Phong Smoothing"):
        ud.CreateUserData(op,"Phong Smoothing", c4d.DTYPE_BOOL, True)
    #10
    if not ud.UserDataExists(op,"Import Vertex Colors"):
        ud.CreateUserData(op,"Import Vertex Colors", c4d.DTYPE_BOOL, True)
    #11
    if not ud.UserDataExists(op,"Create Test Material"):
        ud.CreateUserData(op,"Create Test Material", c4d.DTYPE_BOOL, True)
    #12
    if not ud.UserDataExists(op,"Mesh Handling Message"):
        ud.CreateUserData(op,"Mesh Handling Message", c4d.DTYPE_STATICTEXT, True)


def ResolveFilename(filename):
    """
    Accepts a provided FileName pointng to the first object of the sequence to import, and figures out the apporppriate filename to load based on the current animation 
    frame.

    Args:
        filename: The filename of the first object in the OBJ sequence
    Returns:
            Path: the filename of the actual object to load.
    """

    first = ud.GetUserDataValue(op, "First Frame")
    last = ud.GetUserDataValue(op, "Last Frame")
    step = ud.GetUserDataValue(op, "Frame Step")
    
    
    frame = doc.GetTime().GetFrame(doc.GetFps())
    
    if last <= first:
        frame = max(frame,first) #open ended sequence, no max limit
    else:
        frame = max(min(frame,last),first) # Min and Max limit applied
    
    if frame%step != 0:
        frame = frame - (frame%step) #Frame skipping


    if filename == None or filename == "":
        msg = ">>> Empty Filename. Please provide a link to the FIRST item of the sequence you want to import"
        ud.SetUserData(op,"File Handling Message", msg)
        return

    if os.path.exists(filename) == False:
        msg = ">>> Invalid FileName. Please provide a link to an existing file or folder."
        ud.SetUserData(op,"File Handling Message", msg)
        return
    
    if os.path.isfile(filename):
        directory = os.path.dirname(filename) #Directory of the file
        fullname = os.path.basename(filename) #Fullname of the file, including extension
        name, extension = os.path.splitext(fullname) #Split the actual name from the extension
        
        if extension != ".obj":
            msg = ">>> Invalid FileType. Please provide an .obj file."
            ud.SetUserData(op,"File Handling Message", msg)
            return

        parts = filter(None, re.split(r'(\d+)', name)) # Split the digit and non-digit parts of the name
        
        if parts[-1].isdigit(): #if the last part is digit, use it
            digit = parts[-1]
        else:
            msg = ">>> Invalid Naming Convention. Please make sure that no other characters exist after your file numbering."
            ud.SetUserData(op,"File Handling Message", msg)
            return

        formatted_frame = str(frame).zfill(len(digit)) # Fill number with zeros if necessary
        
        if len(parts[:-1])>1:
            nonDigitName =  " ".join(parts[:-1]).replace(" ","")
        else:
            nonDigitName = parts[0]
        
        Path = os.path.join(directory, nonDigitName + formatted_frame + extension )
        
        msg = ">>> File: ' " +  nonDigitName + formatted_frame + extension + " ' succesfully located."
        ud.SetUserData(op,"File Handling Message", msg)
        return Path
    
    else:
        msg = ">>> Invalid FileType. Please provide a link to an .obj file, not to a folder."
        ud.SetUserData(op,"File Handling Message", msg)
        return

def ParseObj(filename, swapyz=False):
    """
    Loads an OBJ file from disk.

    Args:
        filename: The full path of the OBJ file to load
        swapyz: Indicates whether to swap the Y and Z coordinates of the vertices.
    Returns:
        vertices: The 3D object's vertices, as a list of coordinate tuples in the form (X,Y,Z)
        faces: The 3D object's faces, as a list of integer tuples, pointing to the vertex indices comprising each face in the form (A,B,C) or (A,B,C,D)
        colors: The 3D object's vertex colors, as a list of color tuples in the form (R,G,B)
    """
    
    vertices = []
    colors = []
    faces = []

    for line in open(filename, "r"):
            
        if line.startswith('#'): continue #SKIP COMMENTS
            
        values = line.split()
            
        if not values: continue #SKIP EMPTY LINES
            
        if values[0] == 'v': # VERTICES
            v = map(float, values[1:4])
            if swapyz:
                v = v[0], v[2], v[1]
            vertices.append(v)
            
            if len(values) == 7: # VERTEX COLORS
                c = map(float, values[4:])
                colors.append(c)
            
        elif values[0] == 'f': # FACES
            face = []
            for v in values[1:]:
                face.append(int(v.split("//")[0]))
            if len(face)<=4:
                faces.append(face)
            else:
                pts = [vertices[i-1] for i in face]
                triangles = hull.PySHull(pts)
                for t in triangles:
                    newface =  [ face[t[0]], face[t[1]], face[t[2]]  ]
                    faces.append(newface)
    
    return vertices, faces, colors

def UpdateVertexCoordinates(Vertices):
    global Polygon
    global maxX, maxY, maxZ, minX, minY, minZ

    for i,vert in enumerate(Vertices):
        Polygon.SetPoint(i,c4d.Vector(vert[0], vert[1], vert[2]))

        if vert[1] > maxY:
            maxY = vert[1]
        
        if vert[0] > maxX:
            maxX = vert[0]

        if vert[2] > maxZ:
            maxZ = vert[2]
        
        if vert[1] < minY:
            minY = vert[1]
        
        if vert[0] < minX:
            minX = vert[0]

        if vert[2] < minZ:
            minZ = vert[2]

def UpdateVertexColors(Colors):
    global Polygon

    #VERTEX TAG FOR THE BEHIND-THE-SCENES POLYGON OBJECT
    if not Polygon.GetTag(c4d.Tvertexcolor):
        colorTag = c4d.VertexColorTag(Polygon.GetPointCount())
        Polygon.InsertTag(colorTag)
    else:
        colorTag = Polygon.GetTag(c4d.Tvertexcolor)

    data = c4d.VertexColorTag.GetDataAddressW(colorTag)


    #VERTEX TAG FOR THE PYTHON GENERATOR OBJECT
    if not op.GetTag(c4d.Tvertexcolor):
        opTag = colorTag.GetClone()
        op.InsertTag(opTag)
    else:
        opTag = op.GetTag(c4d.Tvertexcolor)

    data2= c4d.VertexColorTag.GetDataAddressW(opTag)


    for i in range(Polygon.GetPointCount()):
        if i<len(Colors):
            col = Colors[i]
        else:
            r = (Polygon.GetPoint(i)[0] - minX) /(maxX-minX)
            g = (Polygon.GetPoint(i)[1] - minY) /(maxY-minY)
            b = (Polygon.GetPoint(i)[2] - minZ) /(maxZ-minZ)

            col = c4d.Vector(r,g,b)
       
        c4d.VertexColorTag.SetColor(data, None, None, i, col)
        c4d.VertexColorTag.SetColor(data2, None, None, i, col)
    
    shader[c4d.SLA_DIRTY_VMAP_OBJECT] = colorTag

def UpdateFaces(Faces):
    global Polygon

    for i, face in enumerate(Faces):
        if len(face)>2:
            A = face[0]-1
            B = face[1]-1
            C =face[2]-1
                
        if len(face)==3:
            Polygon.SetPolygon(i, c4d.CPolygon(A,B,C) ) #The Polygon's index, Polygon's points
        elif len(face)==4:
            D = face[3]-1
            Polygon.SetPolygon(i, c4d.CPolygon(A,B,C,D) )

def UpdateMaterial():
    global Polygon
    global shader

    _mat = doc.SearchMaterial("OBJ Sequence Material")
    _tags = [t for t in Polygon.GetTags() if t.GetType() == c4d.Ttexture]
    _tag = None

    for t in _tags:
        if t.GetName() == "OBJ Sequence Texture Tag":
            _tag = t
            break

    if not _mat:
        _mat = c4d.Material()
        _mat.SetName("OBJ Sequence Material")
        _mat.SetChannelState(c4d.CHANNEL_COLOR,False)
        _mat.SetChannelState(c4d.CHANNEL_LUMINANCE,True)

        
        _mat[c4d.MATERIAL_LUMINANCE_SHADER] = shader
        _mat.InsertShader(shader)
        doc.InsertMaterial(_mat)
    
    if _tag == None:
        _tag = c4d.TextureTag()
        _tag.SetMaterial(_mat)
        _tag.SetName("OBJ Sequence Texture Tag")
        Polygon.InsertTag(_tag)
    
    _optags = [t for t in op.GetTags() if t.GetType() == c4d.Ttexture]
    _optag = None

    for t in _optags:
        if t.GetName() == "OBJ Sequence Texture Tag":
            _optag = t
            break
    
    if _optag==None:
        _optag = _tag.GetClone()
        _optag.SetName("OBJ Sequence Texture Tag")
        op.InsertTag(_optag)
    else:
        _optag = _tag.GetClone()
        _optag.SetName("OBJ Sequence Texture Tag")

def ImportToCinema():
        global Polygon
        SetupUserData()

        PATH =  ResolveFilename(ud.GetUserDataValue(op, "First Object FileName"))
        
        N = os.path.basename(PATH)
        
        if PATH != None:
            Vertices, Faces, Colors = ParseObj(PATH, ud.GetUserDataValue(op, "Swap Y/Z")) #LOAD OBJ FILE
            
            Polygon = c4d.BaseObject(c4d.Opolygon)
            Polygon.ResizeObject(len(Vertices),len(Faces)) #New number of points, New number of polygons
            Polygon.SetName(N)

            UpdateVertexCoordinates(Vertices)
            UpdateFaces(Faces)

            if ud.GetUserDataValue(op, "Import Vertex Colors"):
                UpdateVertexColors(Colors)
                if  ud.GetUserDataValue(op,"Create Test Material"):
                    UpdateMaterial()

            if ud.GetUserDataValue(op, "Phong Smoothing"):
                Polygon.CreatePhongNormals()
                Polygon.SetPhong(True,True,90)
            else:
                Polygon.SetPhong(False,True,90)
            
            
            if len(Vertices)== 0 and len(Faces)== 0:
                msg = ">>> Mesh Succesfully Loaded, but has no Vertices, neither Faces. It's OK, though."
                ud.SetUserData(op,"Mesh Handling Message", msg)
            elif len(Vertices)== 0:
                msg = ">>> Mesh Succesfully Loaded, but has no Vertices.  It's OK, though."
                ud.SetUserData(op,"Mesh Handling Message", msg)
            elif len(Faces)== 0:
                msg = ">>> Mesh Succesfully Loaded, but has no Faces.  It's OK, though."
                ud.SetUserData(op,"Mesh Handling Message", msg)
            else:
                msg = ">>> Mesh Succesfully Loaded! It should appear in the Viewport."
                ud.SetUserData(op,"Mesh Handling Message", msg)
            
            return Polygon
        else:
            msg = "No Mesh Loaded, because of faulty Filename. Check the File Handling Message above."
            ud.SetUserData(op,"Mesh Handling Message", msg)
            return

#prev        = type("", (), {})()     # create a new empty type and instantiate it
#prev.frame  = 0
#prev.cache  = None           

def main():
    op.SetName("--- OBJ Sequence Reader by George Adamon ---")
    return ImportToCinema()
    

    #frame   = doc.GetTime().GetFrame(doc.GetFps())
    #if frame != prev.frame:
    #    prev.frame  = frame
    #    ImportToCinema()
    