import pyc4d_helpers.external.pyshull as hull

class OBJ:

    @staticmethod
    def ParseObj(filename, swap_yz=False, flip_z=False, scale=1.0):
        """
        Loads an OBJ file from disk.

        Args:
            filename: The full path of the OBJ file to load
            swap_yz: Indicates whether to swap the Y and Z coordinates of the vertices.
            flip_z: Flip the Z Axis
            scale: Scale of the object
        Returns:
            vertices: The 3D object's vertices, as a list of coordinate tuples in the form (X,Y,Z)
            faces: The 3D object's faces, as a list of integer tuples, pointing to the vertex indices comprising each face in the form (A,B,C) or (A,B,C,D)
            vertex_colors: The 3D object's vertex colors, as a list of color tuples in the form (R,G,B)
            
        """

        vertices = []
        vertex_normals = []
        vertex_colors = []
        vertex_texture_coords = []

        faces = []
        faces_normals = []
        faces_texture_coords = []

        for line in open(filename, "r"):

            if line.startswith('#'):
                continue  # SKIP COMMENTS

            values = line.split()

            if not values:
                continue  # SKIP EMPTY LINES

            if values[0] == 'v':  # VERTICES
                v = map(float, values[1:4])

                if swap_yz:
                    v = v[0], v[2], v[1]

                if flip_z:
                    v = v[0], v[1], -v[2]

                v = scale * v[0], scale * v[1], scale * v[2]

                vertices.append(v)

                if len(values) == 7:  # VERTEX COLORS
                    c = map(float, values[4:])
                    vertex_colors.append(c)

            elif values[0] == 'vn':  # VERTEX NORMALS
                vn = map(float, values[1:4])
                vertex_normals.append(vn)

            elif values[0] == 'vt':  # VERTEX TEXTURE COORDS
                vt = map(float, values[1:4])
                vertex_texture_coords.append(vt)

            elif values[0] == 'f':  # FACES
                face = []
                face_vertex_coords = []
                face_vertex_normals = []

                for v in values[1:]:
                    face_data = (v.split("/"))

                    if len(face_data) > 0:

                        face.append(int(face_data[0]))  # ADD FACE INDICES

                        if len(face_data) == 2:
                            face_vertex_coords.append(
                                int(face_data[1]))  # IF EXISTENT, ADD VERTEX TEXTURE COORDINATES INDICES

                        if len(face_data) == 3:
                            if face_data[1] != "":
                                face_vertex_coords.append(
                                    int(face_data[1]))  # IF EXISTENT, ADD VERTEX TEXTURE COORDINATES INDICES

                            face_vertex_normals.append(int(face_data[2]))  # IF EXISTENT, ADD VERTEX NORMALS INDICES

                if len(face) <= 4:  # TRIS OR QUADS
                    faces.append(face)

                    if len(face_vertex_normals) > 0:
                        faces_normals.append(face_vertex_normals)

                    if len(face_vertex_coords) > 0:
                        faces_texture_coords.append(face_vertex_coords)

                else:
                    pts = [vertices[i - 1] for i in face]
                    triangles = hull.PySHull(pts)
                    for t in triangles:
                        new_face = [face[t[0]], face[t[1]], face[t[2]]]
                        faces.append(new_face)

        return vertices, faces, vertex_colors, vertex_normals, vertex_texture_coords, faces_normals, faces_texture_coords

