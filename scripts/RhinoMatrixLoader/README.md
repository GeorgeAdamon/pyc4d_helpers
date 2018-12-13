# Rhino Matrix Loader (Python Generator)
A python script that reads a .csv file with 4x4 Transformation Matrices (position, scale, rotation) exported from Rhino3d / Grasshopper3d, and generates a Cinema4D Polygon Object, whose each face represents a matrix.

This way, the user can orient native Cinema4D objects using a Cloner that maps them to the generated mesh, and use MoGraph effectors on them.

The advantages of this method, instead of exporting the objects directly from Rhino / Grasshopper as meshes, and using Cinema4d's Fracture object to convert them to Mograph clones are:
* Objects/Clones retain their original orientation information, instead of assuming the default one.
* Any type of native Cinema4d object can be used (Lights, Cameras, Fields etc) instead of the basic geometry types that Rhino can export.
* The same map can be used for different Cloners.

This script is meant to be used inside a Cinema4D Python Generator object, and expects a .csv text file where each line is a list of 16 elements, separated by comas. See the In Depth section below for details.

## Usage
* Create a Python Generator object.
* Paste the contents of the script inside the Code field.
* If all goes well, a UI with options should be created under the Python Generators "User Data" tab.
* Select the .csv file with the Transformation Matrices.
* You should see a collection of quads or triangles that represent the Transformation Matrices coming from Rhino.

## Information Regarding Rhino3d/Grasshopper3d vs Cinema4D matrices.
Cinema4D and Rhino/Grasshopper represent 4x4 Transformation Matrices in a different way.

First of all, Rhino has a Z-Up coordinate system, whereas Cinema3D has a Y-Up coordinate system. This means that a Y <--> Z swap has to be performed for every vector of the matrix.

Secondly, in Rhino/Grasshopper matrices, the scale/rotation vectors are laid out in rows, whereas in Cinema4d they are laid out in columns.

### In Depth
#### Expected structure of the csv file
More explictly, this script expects a .csv file saved from Grasshopper, where each line represents list of 16 elements, structured like this:

|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  10 |  11 |  12 |  13 |  14 |  15 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| M00 | M01 | M02 | M03 | M10 | M11 | M12 | M13 | M20 | M21 | M22 | M23 | M30 | M31 | M32 | M33 |

#### Rhino / Grasshopper Matrices
The above values correspond to a Rhino/Grasshopper 4X4 matrix, that was originally structured like that inside Rhino/Grasshopper:
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
Now in Cinema4D, the 4x4 Matrix structures its vectors vertically, and it looks like this:

|Column 0|Column 1|Column 2|Column 3|
|-----|-----|-----|-----|
|   0   |       0       |       0       |       1       |
| X_Pos | X_Direction.X | Y_Direction.X | Z_Direction.X |
| Y_Pos | X_Direction.Y | Y_Direction.Y | Z_Direction.Y |
| Z_Pos | X_Direction.Z | Y_Direction.Z | Z_Direction.Z |

and in Cinema4D terminology:

|Column 0|Column 1|Column 2|Column 3|
|-----|-----|-----|-----|
|   0   |   0   |   0   |   1   |
| off.x |  v1.x |  v2.x |  v2.x |
| off.y |  v1.y |  v2.y |  v2.y |
| off.z |  v1.z |  v2.z |  v2.z |


