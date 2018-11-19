import c4d

def RhinoMatrix_2_C4DMatrix (values):
    """
        Function that converts an array of 16 values coming from a Rhino.Geometry.Transform or a
        Rhino.Geometry.Matrix object (Rhinoceros/Grasshopper3d), to a c4d.Matrix (Cinema4D) object.
    """
    
    # The 4X4_Matrix values as they come from Rhino/Grasshopper, are in a 1D list of 16 elements,
    #structured like that:
    # | M00 | M01 | M02 | M03 | M10 | M11 | M12 | M13 |M20 | M21 | M22 | M23 | M30 | M31 | M32 | M33 |

    if len(values) is not 16:
        return
        
    # Those values correspond to a 4X4 matrix, that was originally structured like that:
    # | M00 | M01 | M02 | M03 |
    # | M10 | M11 | M12 | M13 |
    # | M20 | M21 | M22 | M23 |
    # | M30 | M31 | M32 | M33 |

    # and the meaning of it was :
    # | X_Direction.X | X_Direction.Y | X_Direction.Z | X_Pos |
    # | Y_Direction.X | Y_Direction.Y | Y_Direction.Z | Y_Pos |
    # | Z_Direction.X | Z_Direction.Y | Z_Direction.Z | Z_Pos |
    # |       0       |       0       |       0       |   1   |

    # where X_Direction is the direction of the X Axis (red) of the object,
    # Y_Direction is the direction of the Y Axis (green) of the objects,
    # Z_Direction is the direction of the Z Axis (blue) of the object,
    # and X_Pos,Y_Pos,Z_Pos are the coordinates of the object in World Space

    X = values[0:3]
    Y = values[4:7]
    Z = values[8:11]
    POS = [values[3], values[7], values[11]]

    #Now in Cinema4D, the 4x4 Matrix structures its vectors vertically, and it looks like this:
    # |   0   |       0       |       0       |       1       |
    # | X_Pos | X_Direction.X | Y_Direction.X | Z_Direction.X |
    # | Y_Pos | X_Direction.Y | Y_Direction.Y | Z_Direction.Y |
    # | Z_Pos | X_Direction.Z | Y_Direction.Z | Z_Direction.Z |

    # and in Cinema4D terminology:
    # |   0   |   0   |   0   |   1   |
    # | off.x |  v1.x |  v2.x |  v2.x |
    # | off.y |  v1.y |  v2.y |  v2.y |
    # | off.z |  v1.z |  v2.z |  v2.z |

    # Also in Cinema4D, the Y Axis is the Up Axis, so we need to swap Y and Z in every vector
    # On top of that, we need to flip (negate) the Z axis.
    # Thus we need to do the following remapping:

    m = c4d.Matrix()
    m.v1  = c4d.Vector( X[0]  , Z[0]  , -Y[0]    )
    m.v2  = c4d.Vector( X[1]  , Z[1]  , -Y[1]    )
    m.v3  = c4d.Vector( X[2]  , Z[2]  , -Y[2]    )
    m.off = c4d.Vector( POS[0], POS[2], -POS[1]  )

    return m
