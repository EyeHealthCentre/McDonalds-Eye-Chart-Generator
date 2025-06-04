from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

# === Configuration ===
DPI = 1200
INCHES = 12
IMG_SIZE = DPI * INCHES  # 3600x3600 px
CENTER = IMG_SIZE // 2
RADII_SCALING_FACTOR = DPI * 6
FONT_SIZE_SCALING_FACTOR = int(DPI / 6)

# Radii for the 4 rings (evenly spaced within the canvas)
radii = [int(RADII_SCALING_FACTOR*i) for i in [0.1, 0.2, 0.4, 0.8]]

# Font sizes increasing outward
font_sizes = [int(FONT_SIZE_SCALING_FACTOR*i) for i in [1, 2, 4, 8]]

# List of image file paths to randomly choose from
# Replace these with actual valid file paths on your system
image_paths = [
    r""
]

# Load and validate image paths
image_objects = []
for path in image_paths:
    if os.path.exists(path):
        image_objects.append(Image.open(path).convert("RGBA"))
    else:
        print(f"Warning: Image not found: {path}")

if not image_objects:
    raise ValueError("No valid image files found. Please check 'image_paths' list.")

# Create blank chart
img = Image.new("RGB", (IMG_SIZE, IMG_SIZE), "white")
draw = ImageDraw.Draw(img)

# Load font for the central "X"
def get_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Draw central X
font_center = get_font(FONT_SIZE_SCALING_FACTOR)
text = "X"
bbox = font_center.getbbox(text)
w = bbox[2] - bbox[0]
h = bbox[3] - bbox[1]
draw.text((CENTER - w/2, CENTER - h/2), text, font=font_center, fill="black")

# Place images in concentric rings
for radius, size in zip(radii, font_sizes):
    angle_step = 360 / 8  # 8 items per ring

    for i in range(8):
        angle_deg = i * angle_step
        angle_rad = math.radians(angle_deg)

        # Randomly select and resize an image
        icon = random.choice(image_objects)
        icon_resized = icon.resize((size, size))

        # Compute position (centered)
        x = CENTER + radius * math.cos(angle_rad) - size / 2
        y = CENTER + radius * math.sin(angle_rad) - size / 2

        # Paste with transparency
        img.paste(icon_resized, (int(x), int(y)), icon_resized)

# Save chart
img.save("mcdonald_eye_chart_images.png", optimize=True, compress_level=9)
print("Saved McDonald eye chart as 'mcdonald_eye_chart_images.png'")
img.save("mcdonald_eye_chart_images.webp", lossless=True, quality=100, method=6)
print("Saved McDonald eye chart as 'mcdonald_eye_chart_images.webp'")
img.save("mcdonald_eye_chart_images.pdf")
print("Saved McDonald eye chart as 'mcdonald_eye_chart_images.pdf'")
