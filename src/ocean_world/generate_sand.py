import numpy as np
from PIL import Image

SIZE = 512

rng = np.random.default_rng(42)

# Create sandy noise
noise = rng.random((SIZE, SIZE))

# Make the noise smoother
for _ in range(6):
    noise = (
        noise
        + np.roll(noise, 1, axis=0)
        + np.roll(noise, -1, axis=0)
        + np.roll(noise, 1, axis=1)
        + np.roll(noise, -1, axis=1)
    ) / 5.0

# Normalize
noise = (noise - noise.min()) / (noise.max() - noise.min())

# Sandy colors
red = 150 + noise * 45
green = 120 + noise * 35
blue = 75 + noise * 25

sand = np.stack([red, green, blue], axis=2)
sand = np.clip(sand, 0, 255).astype(np.uint8)

# Save sand texture
Image.fromarray(sand).save(
    "heightmaps/sand_diffuse.png"
)

# Create a simple normal map
normal = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)

normal[:, :, 0] = 128
normal[:, :, 1] = 128
normal[:, :, 2] = 255

Image.fromarray(normal).save(
    "heightmaps/sand_normal.png"
)

print("Sand textures created successfully.")