import numpy as np
from PIL import Image

SIZE = 513

# Create coordinates
x = np.linspace(-3, 3, SIZE)
y = np.linspace(-3, 3, SIZE)

X, Y = np.meshgrid(x, y)

# Start with a flat seabed
terrain = np.zeros((SIZE, SIZE))

# Large underwater dunes
terrain += 0.18 * np.exp(-((X + 1.5)**2 + (Y + 0.5)**2) / 1.5)
terrain += 0.12 * np.exp(-((X - 1.2)**2 + (Y - 1.0)**2) / 1.0)

# Small seabed formations
terrain += 0.08 * np.sin(X * 4) * np.cos(Y * 3)

# Normalize to 0-255
terrain -= terrain.min()
terrain /= terrain.max()

image = (terrain * 255).astype(np.uint8)

Image.fromarray(image).save(
    "heightmaps/seabed.png"
)

print("Seabed heightmap generated.")