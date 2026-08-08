import numpy as np
from PIL import Image
import os

IMAGE = "heightmaps/seabed.png"
OUTPUT = "meshes/seabed.obj"

SIZE_X = 100.0
SIZE_Y = 100.0

MIN_Z = -10.0
MAX_Z = 0.0

STEP = 4

# Load heightmap
image = Image.open(IMAGE).convert("L")
heightmap = np.asarray(image, dtype=np.float32)

heightmap = heightmap[::STEP, ::STEP]
heightmap /= 255.0

rows, cols = heightmap.shape

print(f"Generating mesh: {cols} x {rows}")

vertices = []
normals = []
uvs = []

# Create vertices, normals and UV coordinates
for row in range(rows):

    y = (row / (rows - 1) - 0.5) * SIZE_Y

    for col in range(cols):

        x = (col / (cols - 1) - 0.5) * SIZE_X

        z = MIN_Z + heightmap[row, col] * (MAX_Z - MIN_Z)

        vertices.append((x, y, z))

        # Height derivatives
        left = heightmap[row, max(col - 1, 0)]
        right = heightmap[row, min(col + 1, cols - 1)]

        down = heightmap[max(row - 1, 0), col]
        up = heightmap[min(row + 1, rows - 1), col]

        dzdx = (right - left) * (MAX_Z - MIN_Z)
        dzdy = (up - down) * (MAX_Z - MIN_Z)

        nx = -dzdx
        ny = -dzdy
        nz = 2.0

        length = np.sqrt(nx * nx + ny * ny + nz * nz)

        nx /= length
        ny /= length
        nz /= length

        normals.append((nx, ny, nz))

        # Repeat the texture across the seabed
        u = col / (cols - 1) * 5.0
        v = row / (rows - 1) * 5.0

        uvs.append((u, v))


# Create faces
faces = []

for row in range(rows - 1):

    for col in range(cols - 1):

        a = row * cols + col + 1
        b = row * cols + (col + 1) + 1
        c = (row + 1) * cols + (col + 1) + 1
        d = (row + 1) * cols + col + 1

        faces.append((a, b, c))
        faces.append((a, c, d))


# Make sure output directory exists
os.makedirs("meshes", exist_ok=True)


# Write OBJ
with open(OUTPUT, "w") as file:

    file.write("# Procedural underwater seabed\n")

    # Vertices
    for x, y, z in vertices:
        file.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")

    # Texture coordinates
    for u, v in uvs:
        file.write(f"vt {u:.6f} {v:.6f}\n")

    # Normals
    for nx, ny, nz in normals:
        file.write(f"vn {nx:.6f} {ny:.6f} {nz:.6f}\n")

    # Faces
    for a, b, c in faces:
        file.write(
            f"f {a}/{a}/{a} {b}/{b}/{b} {c}/{c}/{c}\n"
        )


print()
print("Mesh generated successfully!")
print(f"Vertices:  {len(vertices)}")
print(f"UVs:       {len(uvs)}")
print(f"Normals:   {len(normals)}")
print(f"Triangles: {len(faces)}")
print(f"File:      {OUTPUT}")