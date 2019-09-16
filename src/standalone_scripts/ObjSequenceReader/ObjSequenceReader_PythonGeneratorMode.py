import c4d
import os
import re
import math
import random
from pyc4d_helpers import Hierarchy as hi
from pyc4d_helpers.Parsers import OBJ
from pyc4d_helpers import UserData as ud
from pyc4d_helpers import Materials as hm
from pyc4d_helpers.external import pyshull as hull
from os.path import isfile, join, dirname, basename, splitext, exists

#op[c4d.TPYTHON_FRAME] = True

minX = 1000000000000.0
minY = 1000000000000.0
minZ = 1000000000000.0

maxX = 0.0
maxY = 0.0
maxZ = 0.0

runcount = 0
prev_filename = ""

min_Frame = 10000000000
max_Frame = 0
digitCount = 0

shader = hm.CreateShader(c4d.Xvertexmap, "OBJ Vertex Colors Shader")

OutputObject = c4d.BaseObject(c4d.Onull)


# ----------------------------------------------------------------------------------------------------------------------
# UI SETUP FUNCTIONS ---------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def SetupUserData():
    """
    Setup the UI of the Python Generator object
    """
    # ------------------------------------------------------------------------------------------------------------------
    # 1 - FILE HANDLING UI ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # 1.1: UI Header
    if not ud.UserDataExists(op,"File Handling"):
        ud.CreateUserData(op,"File Handling", c4d.DTYPE_SEPARATOR)
    # 1.2: "Filename" text box
    if not ud.UserDataExists(op,"First Object FileName"):
        ud.CreateUserData(op,"First Object FileName", c4d.DTYPE_FILENAME, True)
    # 1.3: "Load All" Boolean, determines whether to load all files in the folder at once
    if not ud.UserDataExists(op,"Load All"):
        ud.CreateUserData(op,"Load All", c4d.DTYPE_BOOL)
    # 1.4
    if not ud.UserDataExists(op,"First Frame"):
        ud.CreateIntegerData(op,"First Frame", "Integer")
    # 1.5
    if not ud.UserDataExists(op,"Last Frame"):
        ud.CreateIntegerData(op,"Last Frame", "Integer")
    # 1.6
    if not ud.UserDataExists(op,"Frame Step"):
        ud.CreateIntegerData(op,"Frame Step", "Integer Slider")
        ud.SetUserDataValue(op, "Frame Step", 1)
    # 1.7
    if not ud.UserDataExists(op,"Frame Offset"):
        ud.CreateIntegerData(op,"Frame Offset", "Integer Slider")
        ud.SetUserDataValue(op, "Frame Offset", 0)
    # 1.8
    if not ud.UserDataExists(op,"After Last Frame"):
        ud.CreateDropDown(op,"After Last Frame", "Cycle", ["Freeze", "Loop", "Ping Pong", "Disappear"])
        ud.SetUserDataValue(op, "After Last Frame", 0)
    # 1.9
    if not ud.UserDataExists(op,"File Handling Message"):
        ud.CreateUserData(op,"File Handling Message", c4d.DTYPE_STATICTEXT, True)

    # ------------------------------------------------------------------------------------------------------------------
    # 2 - MESH HANDLING UI ---------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # 2.1
    if not ud.UserDataExists(op,"Mesh Handling"):
        ud.CreateUserData(op,"Mesh Handling", c4d.DTYPE_SEPARATOR)
    # 2.2
    if not ud.UserDataExists(op,"Phong Smoothing"):
        ud.CreateUserData(op,"Phong Smoothing", c4d.DTYPE_BOOL)
    # 2.3
    if not ud.UserDataExists(op,"Import Vertex Colors"):
        ud.CreateUserData(op,"Import Vertex Colors", c4d.DTYPE_BOOL)
    # 2.4
    if not ud.UserDataExists(op,"Create Test Material"):
        ud.CreateUserData(op,"Create Test Material", c4d.DTYPE_BOOL)
    # 2.5
    if not ud.UserDataExists(op,"Mesh Handling Message"):
        ud.CreateUserData(op,"Mesh Handling Message", c4d.DTYPE_STATICTEXT, True)
    # 2.6
    if not ud.UserDataExists(op,"Vertices"):
        ud.CreateUserData(op,"Vertices", c4d.DTYPE_STATICTEXT, True)
    # 2.7
    if not ud.UserDataExists(op,"Colors"):
        ud.CreateUserData(op,"Colors", c4d.DTYPE_STATICTEXT, True)
    # 2.8
    if not ud.UserDataExists(op,"Faces"):
        ud.CreateUserData(op,"Faces", c4d.DTYPE_STATICTEXT, True)

    # ------------------------------------------------------------------------------------------------------------------
    # 3 - COORDINATE HANDLING UI ---------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # 3.1
    if not ud.UserDataExists(op,"Coordinate Handling"):
        ud.CreateUserData(op,"Coordinate Handling", c4d.DTYPE_SEPARATOR)
    # 3.2
    if not ud.UserDataExists(op,"Swap Y/Z"):
        ud.CreateUserData(op,"Swap Y/Z", c4d.DTYPE_BOOL)
    # 3.3
    if not ud.UserDataExists(op,"Flip Z"):
        ud.CreateUserData(op,"Flip Z", c4d.DTYPE_BOOL)
    # 3.4
    if not ud.UserDataExists(op,"Scale"):
        ud.CreateFloatData(op,"Scale", "Float Slider", 0.0, 1000.0, 0.1)
        ud.SetUserDataValue(op, "Scale", 1)


# ----------------------------------------------------------------------------------------------------------------------
# FILE SYSTEM FUNCTIONS ------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def GetFiles(directory, filetype = ""):
    """
    Get all the files in a directory
    Args:
        directory: Directory to read files from
        filetype: Optional filetype to look for (has to include the '.' character, for example .obj
    Returns:
        A list of filenames with extensions
    """
    if not filetype:
        files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
    else:
        files = [f for f in os.listdir(directory) if isfile(join(directory, f)) and splitext(f) == filetype]

    return files

def SplitPath(path):
    """
    Split a full path into directory, filename, filename without extension & extension
    :param path: The path to split
    :return:
    """
    directory = dirname(path) #Directory of the file
    fullname = basename(path) #Fullname of the file, including extension
    name, extension = splitext(fullname) #Split the actual name from the extension

    return directory, fullname, name, extension

def ResolveFilename(filename, Frame = -1):

    """
    Accepts a provided FileName pointng to the first object of the sequence to import, and figures out the apporppriate filename to load based on the current animation 
    frame.

    Args:
        filename: The filename of the first object in the OBJ sequence
    Returns:
            Path: the filename of the actual object to load.
    """
    global runcount
    global prev_filename
    global min_Frame
    global max_Frame
    global digitCount

    # ------------------------------------------------------------------------------------------------------------------
    # FILE ERROR HANDLING ----------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    if not filename:
        msg = ">>> Empty Filename. Please provide a link to the FIRST item of the sequence you want to import"
        ud.SetUserDataValue(op, "File Handling Message", msg)
        return

    if not exists(filename):
        msg = ">>> Invalid FileName. Please provide a link to an existing file or folder."
        ud.SetUserDataValue(op, "File Handling Message", msg)
        return

    if not isfile(filename):
        msg = ">>> Invalid FileType. Please provide a link to an .obj file, not to a folder."
        ud.SetUserDataValue(op, "File Handling Message", msg)
        return

    if not splitext(filename)[1] == ".obj":
        msg = ">>> Invalid FileType. Please provide an .obj file."
        ud.SetUserDataValue(op, "File Handling Message", msg)
        return

    directory, fullname, name, extension = SplitPath(filename)
    parts = filter(None, re.split(r'(\d+)', name))  # Split the digit and non-digit parts of the name

    if parts[-1].isdigit(): #if the last part is digit, use it
        digit = parts[-1]
    else:
        msg = ">>> Invalid Naming Convention. Please make sure that no other characters exist after your file numbering."
        ud.SetUserDataValue(op, "File Handling Message", msg)
        return

    # ------------------------------------------------------------------------------------------------------------------
    # RESET RUN COUNT ON FILE CHANGE -----------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if not runcount == 0:
        if not prev_filename == filename:
            runcount = 0

    if len(parts[:-1])>1:
        nonDigitName = " ".join(parts[:-1]).replace(" ", "")
    else:
        nonDigitName = parts[0]

    if runcount == 0:
        files = GetFiles(directory, ".obj")

        _digit = 0

        for f in files:

            _d, _f, _n, _e = SplitPath(f)

            _parts = filter(None, re.split(r'(\d+)', _n)) # Split the digit and non-digit parts of the name

            if len(_parts[:-1]) > 1:
                _nonDigitName = " ".join(_parts[:-1]).replace(" ","")
            else:
                _nonDigitName = _parts[0]

            if _parts[-1].isdigit(): #if the last part is digit, use it
                _digit = _parts[-1]

            if _nonDigitName == nonDigitName:
                if int(_digit) < min_Frame:
                    min_Frame = int(digit)
                    digitCount = len(_digit)

                if int(_digit) >= max_Frame:
                    max_Frame = int(_digit)

        ud.SetUserDataValue(op, "First Frame", int(min_Frame))
        ud.SetUserDataValue(op, "Last Frame", int(max_Frame))

    if Frame <= -1:
        formatted_frame = ConstructFrame()
    else:
        formatted_frame = ConstructFrame(Frame)

    if formatted_frame != -1:
        Path = os.path.join(directory, nonDigitName + formatted_frame + extension )
        msg = ">>> File: ' " +  nonDigitName + formatted_frame + extension + " ' succesfully located."
        ud.SetUserDataValue(op,"File Handling Message", msg)
        return Path
    else:
        return -1


# ----------------------------------------------------------------------------------------------------------------------
# CURRENT FRAME MANIPULATOR FUNCTIONS ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def ConstructFrame(Frame = -1):

    """
        Accepts a provided FileName pointing to the first object of the sequence to import, and figures out the apporppriate filename to load based on the current animation 
        frame.

        Args:
            filename: The filename of the first object in the OBJ sequence
        Returns:
            Path: the filename of the actual object to load.
    """
    global min_Frame
    global max_Frame
    global digitCount

    if Frame <= -1:
        first = max(ud.GetUserDataValue(op, "First Frame"), min_Frame)
        last = min(ud.GetUserDataValue(op, "Last Frame"), max_Frame)

        ud.SetUserDataValue(op, "First Frame", first)
        ud.SetUserDataValue(op, "Last Frame", last)

        step = ud.GetUserDataValue(op, "Frame Step")
        offset = ud.GetUserDataValue(op, "Frame Offset")
        after = ud.GetUserDataValue(op, "After Last Frame")

        frame = doc.GetTime().GetFrame(doc.GetFps()) + offset

        if frame % step != 0:
            frame = frame - (frame%step) #Frame skipping
        
        if after == 0:
            if last <= first:
                frame = max(frame,first) #open ended sequence, no max limit
            else:
                frame = max(min(frame,last),first) # Min and Max limit applied
        elif after == 1:
            frame = frame%last

        elif after == 2:
            if (frame//last)%2 == 0:
                frame = frame%last
            else:
                frame = last - (frame%last)
        elif after == 3:
            if frame>last or frame<first:
                return -1
    else:
        frame = Frame

    formatted_frame = str(frame).zfill(digitCount) # Fill number with zeros if necessary

    return formatted_frame


def ConstructFrameRange(min_frame = 0, max_frame = 90):
    pass

# ----------------------------------------------------------------------------------------------------------------------
# UTILITY FUNCTIONS FOR MANIPULATING NORMAL TAG ------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Obtained From: http://www.plugincafe.com/forum/forum_posts.asp?TID=9752&PID=38672#38672
def float2bytes(f):
    int_value = int(math.fabs(f * 32000.0))
    high_byte = int(int_value / 256)
    low_byte = int_value - 256 * high_byte

    if f < 0:
        high_byte = 255-high_byte
        low_byte = 255-low_byte

    return (low_byte,high_byte)

def set_normals(normal_tag,polygon,normal_a,normal_b,normal_c,normal_d):

    normal_list = [normal_a, normal_b, normal_c, normal_d]
    normal_buffer = normal_tag.GetLowlevelDataAddressW()
    vector_size = 6
    component_size = 2

    for v in range(0,4):
        normal = normal_list[v]
        component = [normal.x, normal.y, normal.z]

        for c in range(0,3):
            low_byte, high_byte = float2bytes(component[c])

            normal_buffer[normal_tag.GetDataSize()*polygon+v*vector_size+c*component_size+0] = chr(low_byte)
            normal_buffer[normal_tag.GetDataSize()*polygon+v*vector_size+c*component_size+1] = chr(high_byte)


def ParseObj(filename, swapyz=False, flipz= False , scale = 1.0):
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
    vertexNormals =[]
    vertexColors = []
    vertexTextureCoords = []

    faces = []
    facesNormals = []
    facesTextureCoords = []

    for line in open(filename, "r"):
            
        if line.startswith('#'): continue #SKIP COMMENTS
            
        values = line.split()
            
        if not values: continue #SKIP EMPTY LINES
            
        if values[0] == 'v': # VERTICES
            v = map(float, values[1:4])
            
            if swapyz:
                v = v[0], v[2], v[1]
            
            if flipz:
                v = v[0], v[1], -v[2]

            v = scale*v[0], scale*v[1], scale*v[2]

            vertices.append(v)
            
            if len(values) == 7: # VERTEX COLORS
                c = map(float, values[4:])
                vertexColors.append(c)
        
        elif values[0] == 'vn': # VERTEX NORMALS
            vn = map(float, values[1:4])
            vertexNormals.append(vn)

        elif values[0] == 'vt': #VERTEX TEXTURE COORDS
            vt =  map(float, values[1:4])
            vertexTextureCoords.append(vt)
        
        elif values[0] == 'f': # FACES
            face = []
            face_vertex_coords = []
            face_vertex_normals = []

            for v in values[1:]:
                facedata = (v.split("/"))
                
                if len(facedata) > 0:
                    
                    face.append(int(facedata[0])) #ADD FACE INDICES

                    if len(facedata) == 2:
                        face_vertex_coords.append(int(facedata[1])) # IF EXISTENT, ADD VERTEX TEXTURE COORDINATES INDICES

                    if len(facedata) == 3:
                        if facedata[1] != "":
                            face_vertex_coords.append(int(facedata[1])) # IF EXISTENT, ADD VERTEX TEXTURE COORDINATES INDICES
                        
                        face_vertex_normals.append(int(facedata[2])) # IF EXISTENT, ADD VERTEX NORMALS INDICES

            if len(face)<=4: #TRIS OR QUADS
                faces.append(face)
                
                if len(face_vertex_normals)>0:
                    facesNormals.append(face_vertex_normals)

                if len(face_vertex_coords)>0:
                    facesTextureCoords.append(face_vertex_coords)

            else:
                pts = [vertices[i-1] for i in face]
                triangles = hull.PySHull(pts)
                for t in triangles:
                    newface =  [ face[t[0]], face[t[1]], face[t[2]]  ]
                    faces.append(newface)

    return vertices, faces, vertexColors, vertexNormals, vertexTextureCoords, facesNormals, facesTextureCoords

# ====================== TOP LEVEL CODE ===================================== #
def ImportToCinema(PATH):
        #global Polygon
        global OutputObject
        global runcount
        global prev_filename

        #SetupUserData()

        #PATH =  ResolveFilename(ud.GetUserDataValue(op, "First Object FileName"))
        
        if PATH != None and PATH != -1:
            
            N = os.path.basename(PATH)
            
            FaceUV = []
            # LOAD OBJ FILE
            Vertices,       \
            Faces,          \
            Colors,         \
            VertexNormals,  \
            VertexUV,       \
            FaceNormals,    \
            FaceUV = OBJ.ParseObj(PATH,
                                  ud.GetUserDataValue(op, "Swap Y/Z"),
                                  ud.GetUserDataValue(op, "Flip Z"),
                                  ud.GetUserDataValue(op, "Scale"))
            
            ud.SetUserDataValue(op, "Vertices", str(len(Vertices)))
            ud.SetUserDataValue(op, "Colors", str(len(Colors)))
            ud.SetUserDataValue(op, "Faces", str(len(Faces)))

            Polygon = c4d.BaseObject(c4d.Opolygon)
            Polygon.ResizeObject(len(Vertices),len(Faces)) #New number of points, New number of polygons
            Polygon.SetName(N)

            UpdateVertexCoordinates(Polygon, Vertices)
            UpdateFaces(Polygon, Faces) 
            
            if len(FaceUV)>0:
                UpdateUV(Polygon, FaceUV,VertexUV)
            
            if ud.GetUserDataValue(op, "Import Vertex Colors"):
                UpdateVertexColors(Polygon, Colors)
                if  ud.GetUserDataValue(op,"Create Test Material"):
                    UpdateMaterial(Polygon)

            if ud.GetUserDataValue(op, "Phong Smoothing"):
                Polygon.CreatePhongNormals()
                Polygon.SetPhong(True,True,90)
            else:
                Polygon.SetPhong(False,True,90)
            
            
            if len(Vertices)== 0 and len(Faces)== 0:
                msg = ">>> Mesh Succesfully Loaded, but has no Vertices, neither Faces. It's OK, though."
                ud.SetUserDataValue(op,"Mesh Handling Message", msg)
            elif len(Vertices)== 0:
                msg = ">>> Mesh Succesfully Loaded, but has no Vertices.  It's OK, though."
                ud.SetUserDataValue(op,"Mesh Handling Message", msg)
            elif len(Faces)== 0:
                msg = ">>> Mesh Succesfully Loaded, but has no Faces.  It's OK, though."
                ud.SetUserDataValue(op,"Mesh Handling Message", msg)
            else:
                msg = ">>> Mesh Succesfully Loaded! It should appear in the Viewport."
                ud.SetUserDataValue(op,"Mesh Handling Message", msg)
            
            runcount += 1
            prev_filename = ud.GetUserDataValue(op, "First Object FileName")

            Polygon.InsertUnder(OutputObject)

            return
        elif PATH == -1:
            msg = "Outside of Frame Range."
            ud.SetUserDataValue(op,"Mesh Handling Message", msg)
            return
        else:
            msg = "No Mesh Loaded, because of faulty Filename. Check the File Handling Message above."
            ud.SetUserDataValue(op,"Mesh Handling Message", msg)
            return

# ====================== UPDATING FUNCTIONS ================================= #
def UpdateVertexCoordinates(_Polygon, Vertices):
    #global Polygon
    global maxX, maxY, maxZ, minX, minY, minZ

    for i,vert in enumerate(Vertices):
        _Polygon.SetPoint(i,c4d.Vector(vert[0], vert[1], vert[2]))

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

def UpdateVertexColors(_Polygon, Colors):
    #global Polygon

    #VERTEX TAG FOR THE BEHIND-THE-SCENES POLYGON OBJECT
    if not _Polygon.GetTag(c4d.Tvertexcolor):
        colorTag = c4d.VertexColorTag(_Polygon.GetPointCount())
        _Polygon.InsertTag(colorTag)
    else:
        colorTag = _Polygon.GetTag(c4d.Tvertexcolor)

    data = c4d.VertexColorTag.GetDataAddressW(colorTag)


    #VERTEX TAG FOR THE PYTHON GENERATOR OBJECT
    if not op.GetTag(c4d.Tvertexcolor):
        opTag = colorTag.GetClone()
        op.InsertTag(opTag)
    else:
        opTag = op.GetTag(c4d.Tvertexcolor)

    data2= c4d.VertexColorTag.GetDataAddressW(opTag)


    for i in range(_Polygon.GetPointCount()):
        if i<len(Colors):
            r = Colors[i][0]
            g = Colors[i][1]
            b = Colors[i][2]
        else:
            r = (_Polygon.GetPoint(i)[0] - minX) /(maxX-minX)
            g = (_Polygon.GetPoint(i)[1] - minY) /(maxY-minY)
            b = (_Polygon.GetPoint(i)[2] - minZ) /(maxZ-minZ)

        col = c4d.Vector(r,g,b)
       
        c4d.VertexColorTag.SetColor(data, None, None, i, col)
        c4d.VertexColorTag.SetColor(data2, None, None, i, col)
    
    shader[c4d.SLA_DIRTY_VMAP_OBJECT] = colorTag

def UpdateFaces(_Polygon,Faces):
    #global Polygon

    for i, face in enumerate(Faces):
        if len(face)>2:
            A = face[0]-1
            B = face[1]-1
            C =face[2]-1
                
        if len(face)==3:
            _Polygon.SetPolygon(i, c4d.CPolygon(A,B,C) ) #The Polygon's index, Polygon's points
        elif len(face)==4:
            D = face[3]-1
            _Polygon.SetPolygon(i, c4d.CPolygon(A,B,C,D) )

def UpdateMaterial(_Polygon):
    #global Polygon
    global shader

    _mat = doc.SearchMaterial("OBJ Sequence Material")
    _tags = [t for t in _Polygon.GetTags() if t.GetType() == c4d.Ttexture]
    _tag = None

    for t in _tags:
        if t.GetName() == "OBJ Sequence Texture Tag":
            _tag = t
            break

    if not _mat:
        _mat = hm.CreateMaterial("OBJ Sequence Material", [c4d.CHANNEL_LUMINANCE])
        
        #_mat = c4d.Material()
        #_mat.SetName("OBJ Sequence Material")
        #_mat.SetChannelState(c4d.CHANNEL_COLOR,False)
        #_mat.SetChannelState(c4d.CHANNEL_LUMINANCE,True)

        hm.ApplyShader(shader, _mat, "Luminance")
        
        #_mat[c4d.MATERIAL_LUMINANCE_SHADER] = shader
        #_mat.InsertShader(shader)

        doc.InsertMaterial(_mat)
    
    if _tag == None:
        _tag = hm.ApplyMaterial(_Polygon, _mat, "OBJ Sequence Texture Tag", True)
        #_tag = c4d.TextureTag()
        #_tag.SetMaterial(_mat)
        #_tag.SetName("OBJ Sequence Texture Tag")
        #Polygon.InsertTag(_tag)
    
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

def UpdateUV(_Polygon,FaceUV,VertexUV):
    #global Polygon

    #UVW TAG FOR THE BEHIND-THE-SCENES POLYGON OBJECT
    if not _Polygon.GetTag(c4d.Tuvw):
        uvwTag = c4d.UVWTag(_Polygon.GetPolygonCount())
        _Polygon.InsertTag(uvwTag)
    else:
        uvwTag = _Polygon.GetTag(c4d.Tuvw)

    #UVW TAG FOR THE PYTHON GENERATOR OBJECT
    if not op.GetTag(c4d.Tuvw):
        op_uvwTag = uvwTag.GetClone()
        op.InsertTag(op_uvwTag)
    else:
        op_uvwTag = op.GetTag(c4d.Tuvw)

    for i in range(_Polygon.GetPolygonCount()):

        a = FaceUV[i][0]-1
        
        ca = VertexUV[a]

        va = c4d.Vector(ca[0],1-ca[1],0)

        b = FaceUV[i][1]-1
        cb = VertexUV[b]
        
        vb = c4d.Vector(cb[0],1-cb[1],0)

        c = FaceUV[i][2]-1
        cc = VertexUV[c]
        vc = c4d.Vector(cc[0],1-cc[1],0)
        

        d = FaceUV[i][2]-1
        
        if len(FaceUV[i])>3:
            d = FaceUV[i][3]-1
        
        cd = VertexUV[d]
        vd = c4d.Vector(cd[0],1-cd[1],0)

        uvwTag.SetSlow(i,va,vb,vc,vd)
        op_uvwTag.SetSlow(i,va,vb,vc,vd)


#prev        = type("", (), {})()     # create a new empty type and instantiate it
#prev.frame  = 0
#prev.cache  = None           

def main():
    global OutputObject
    global runcount
    global min_Frame
    global max_Frame

    op.SetName("--- OBJ Sequence Reader by George Adamon ---")
    
    SetupUserData()

    OutputObject = c4d.BaseObject(c4d.Onull)

    multifile = ud.GetUserDataValue(op, "Load All")
    if not multifile:
        currentPath = ResolveFilename(ud.GetUserDataValue(op, "First Object FileName"))
        ImportToCinema(currentPath)
    else:
        for i in range(min_Frame, max_Frame):
            currentPath = ResolveFilename(ud.GetUserDataValue(op, "First Object FileName"), i)
            ImportToCinema(currentPath)

    print str.format("The generator has run {0} times.", runcount)
    return OutputObject
    #frame   = doc.GetTime().GetFrame(doc.GetFps())
    #if frame != prev.frame:
    #    prev.frame  = frame
    #    ImportToCinema()
    
