# Rhino Matrix Loader (Python Generator)
A python script that reads a .csv file with [4x4 Transformation Matrices](https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_Transform.htm) (position, scale, rotation) exported from Rhino3d / Grasshopper3d, and generates a [Cinema4D Polygon Object](https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/c4d/C4DAtom/GeListNode/BaseList2D/BaseObject/PointObject/PolygonObject/index.html), whose each face represents a matrix.

This way, the user can orient native Cinema4D objects using a Cloner that maps them to the generated mesh, and use MoGraph effectors on them.

The advantages of this method, instead of exporting the objects directly from Rhino / Grasshopper as meshes, and using Cinema4d's Fracture object to convert them to Mograph clones are:
* Objects/Clones retain their original orientation information, instead of assuming the default one.
* Any type of native Cinema4d object can be used (Lights, Cameras, Fields etc) instead of just the basic geometry types that Rhino can export.
* The same map can be used for different Cloners.
* The file size of the transformation matrices is orders of magnitude smaller, compared to an exported file containing the full geometry.

This script is meant to be used inside a Cinema4D Python Generator object, and expects a .csv text file where each line is a list of 16 elements, separated by comas. See the [In Depth](https://github.com/GeorgeAdamon/pyc4d_helpers/blob/master/scripts/RhinoMatrixLoader/README.md#expected-structure-of-the-csv-file) section below for details.

## Usage
* Create a Python Generator object.
* Paste the contents of the script inside the Code field.
* If all goes well, a UI with options should be created under the Python Generators "User Data" tab.
* Select the .csv file with the Transformation Matrices.
* You should see a collection of quads or triangles that represent the Transformation Matrices coming from Rhino.

## Information Regarding [Rhino3d/Grasshopper3d](https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_Transform.htm) vs [Cinema4D](https://developers.maxon.net/docs/Cinema4DPythonSDK/html/misc/matrixfundamental.html) Transformation Matrices.
Cinema4D and Rhino/Grasshopper represent 4x4 Transformation Matrices in an annoyingly different way.

First of all, Rhino has a Z-Up coordinate system, whereas Cinema3D has a Y-Up coordinate system. This means that a Y <--> Z swap has to be performed for every vector of the matrix.

Secondly, in Rhino/Grasshopper matrices, the scale/rotation vectors are laid out in rows, whereas in Cinema4d they are laid out in columns.

### In Depth
#### Expected structure of the csv file
More explictly, this script expects a .csv file saved from Grasshopper, where each line represents list of 16 elements, structured like this:

|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  10 |  11 |  12 |  13 |  14 |  15 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| M00 | M01 | M02 | M03 | M10 | M11 | M12 | M13 | M20 | M21 | M22 | M23 | M30 | M31 | M32 | M33 |

Example (with optional header):
```
m00,m01,m02,m03,m10,m11,m12,m13,m20,m21,m22,m23,m30,m31,m32,m33
0.642553,-0.680954,0.351321,5896.23,0.705004,0.705004,0.0770605,6376.33,-0.300158,0.198167,0.933078,5275.23,0.0,0.0,0.0,1.0
0.442325,-0.309475,-0.841768,5939.91,-0.573272,-0.819365,-1.80217e-13,6375.29,-0.689715,0.482562,-0.539839,5262.12,0.0,0.0,0.0,1.0
0.636328,-0.770095,0.045173,5920.85,-0.765131,-0.63752,-0.090235,6302.94,0.0982882,0.0228558,-0.994896,5268.35,0.0,0.0,0.0,1.0
0.739983,-0.473658,0.477571,5870.72,-0.657811,-0.657811,0.366838,6257.80,0.140395,-0.585605,-0.798346,5272.14,0.0,0.0,0.0,1.0
0.312936,-0.916166,-0.250423,5860.01,0.357999,0.357999,-0.862365,6273.24,0.87972,0.180214,0.440017,5267.71,0.0,0.0,0.0,1.0
-0.526488,0.702613,-0.478691,5869.59,-0.684326,-0.684326,-0.251785,6278.27,-0.504488,0.195018,0.841106,5250.89,0.0,0.0,0.0,1.0
0.616493,-0.321057,0.718929,5884.64,0.461897,0.886934,-5.57887e-14,6216.52,-0.637642,0.332071,0.695084,5246.32,0.0,0.0,0.0,1.0
0.824675,-0.530596,0.195907,5765.35,-0.479792,-0.839669,-0.254471,6194.11,0.299519,0.115861,-0.947029,5237.77,0.0,0.0,0.0,1.0
```
#### Rhino / Grasshopper Matrices
The above values correspond to a [Rhino/Grasshopper 4X4 Matrix](https://developer.rhino3d.com/api/RhinoCommon/html/T_Rhino_Geometry_Transform.htm), that was originally structured like that inside Rhino/Grasshopper:

|Column 0|Column 1|Column 2|Column 3|
|-----|-----|-----|-----|
| M00 | M01 | M02 | M03 |
| M10 | M11 | M12 | M13 |
| M20 | M21 | M22 | M23 |
| M30 | M31 | M32 | M33 |

and the meaning of it was :

|Column 0|Column 1|Column 2|Column 3|
|-----|-----|-----|-----|
| X_Direction.X | X_Direction.Y | X_Direction.Z | X_Pos |
| Y_Direction.X | Y_Direction.Y | Y_Direction.Z | Y_Pos |
| Z_Direction.X | Z_Direction.Y | Z_Direction.Z | Z_Pos |
|       0       |       0       |       0       |   1   |

where X_Direction is the direction of the X Axis (red) of the object, Y_Direction is the direction of the Y Axis (green) of the objects, Z_Direction is the direction of the Z Axis (blue) of the object, and X_Pos, Y_Pos, Z_Pos are the coordinates of the object in World Space.

#### Cinema4d Matrices
On the other hand, the [Cinema4D 4x4 Matrix](https://developers.maxon.net/docs/Cinema4DPythonSDK/html/misc/matrixfundamental.html) structures its vectors vertically, and it looks like this:

|Column 0|Column 1|Column 2|Column 3|
|-----|-----|-----|-----|
|   1   |       0       |       0       |       0       |
| X_Pos | X_Direction.X | Y_Direction.X | Z_Direction.X |
| Y_Pos | X_Direction.Y | Y_Direction.Y | Z_Direction.Y |
| Z_Pos | X_Direction.Z | Y_Direction.Z | Z_Direction.Z |

and in Cinema4D terminology:

|Column 0|Column 1|Column 2|Column 3|
|-----|-----|-----|-----|
|   1   |   0   |   0   |   0   |
| off.x |  v1.x |  v2.x |  v2.x |
| off.y |  v1.y |  v2.y |  v2.y |
| off.z |  v1.z |  v2.z |  v2.z |

#### Finally
Thus, the main swizzling that is taking place is:

``` 
m = c4d.Matrix()
m.v1  = c4d.Vector( X[0]  , Z[0]  , Y[0]    )
m.v2  = c4d.Vector( X[1]  , Z[1]  , Y[1]    )
m.v3  = c4d.Vector( X[2]  , Z[2]  , Y[2]    )
m.off = c4d.Vector( POS[0], POS[2], POS[1]  )
```

