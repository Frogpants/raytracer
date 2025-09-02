
def grab_obj_data(obj_path):
    vertices = []
    faces = []

    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):  # vertex
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                vertices.append([x, y, z])
            elif line.startswith('f '):  # face
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:4]]  # only vertex indices, 0-based
                faces.append(face)

    return vertices, faces

def save_list(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write(str(item) + '\n')

def flatten_list(lst):
    return [round(coord,1) for vertex in lst for coord in vertex]

verts, tris = grab_obj_data("/home/spenc/mystuff/raytracer/Generation/Data-Extraction/knight.obj")

verts = flatten_list(verts)

save_list("vertices.txt",verts)
