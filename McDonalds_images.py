from PIL import Image, ImageDraw, ImageFont
import math
import random
import os

# === Configuration ===
DPI: int = 1200
INCHES: float = 12
IMG_SIZE: int = int(DPI * INCHES)
CENTER: int = IMG_SIZE // 2
RADII_SCALING_FACTOR: int = DPI * 6
FONT_SIZE_SCALING_FACTOR: int = int(DPI / 6)
SAVE_AS_PDF: bool = True
SAVE_AS_PNG: bool = True
SAVE_AS_WEBP: bool = False

# Radii for the 4 rings (evenly spaced within the canvas)
radii: list[int] = [int(RADII_SCALING_FACTOR*i) for i in [0.1, 0.2, 0.4, 0.8]]

# Font sizes increasing outward
font_sizes: list[int] = [int(FONT_SIZE_SCALING_FACTOR*i) for i in [1, 2, 4, 8]]

# List of image file paths to randomly choose from
# Replace these with actual valid file paths on your system
image_paths: list[str] = [
    r""
]

# Load and validate image paths
image_objects: list[Image.Image] = []
for path in image_paths:
    if os.path.exists(path):
        image_objects.append(Image.open(path).convert("RGBA"))
    else:
        print(f"Warning: Image not found: {path}")

if not image_objects:
    raise ValueError("No valid image files found. Please check 'image_paths' list.")

img: Image.Image = Image.new("RGB", (IMG_SIZE, IMG_SIZE), "white")
draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

def get_font(size: float) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Draw central X
font_center: ImageFont.FreeTypeFont | ImageFont.ImageFont = get_font(FONT_SIZE_SCALING_FACTOR)
text = "X"
bbox: tuple[float, float, float, float] | tuple[int, int, int, int] = font_center.getbbox(text)
w: float | int = bbox[2] - bbox[0]
h: float | int = bbox[3] - bbox[1]
draw.text((CENTER - w/2, CENTER - h/2), text, font=font_center, fill="black")

# Place images in concentric rings
for radius, size in zip(radii, font_sizes):
    angle_step: float = 360 / 8  # 8 items per ring

    for i in range(8):
        angle_deg: float = i * angle_step
        angle_rad: float = math.radians(angle_deg)

        # Randomly select and resize an image
        icon: Image.Image = random.choice(image_objects)
        icon_resized: Image.Image = icon.resize((size, size), Image.Resampling.LANCZOS)

        # Compute position (centered)
        x: float = CENTER + radius * math.cos(angle_rad) - size / 2
        y: float = CENTER + radius * math.sin(angle_rad) - size / 2

        img.paste(icon_resized, (int(x), int(y)), icon_resized)

def add_border(imgdraw: ImageDraw.ImageDraw, dpi: int, thickness_mm: float, border_colour) -> None:
    thickness_inches: float = thickness_mm / 25.4
    thickness_pixels: int = int(round(dpi * thickness_inches))
    w: int
    h: int
    w, h = imgdraw._image.size

    imgdraw.rectangle((0, 0, w, thickness_pixels-1), fill=border_colour)
    imgdraw.rectangle((0, h - thickness_pixels, w, h-1), fill=border_colour)
    imgdraw.rectangle((0, 0, thickness_pixels-1, h), fill=border_colour)
    imgdraw.rectangle((w - thickness_pixels, 0, w-1, h), fill=border_colour)

add_border(draw, DPI, 1.0, 127)

if SAVE_AS_PDF:
    img.save("mcdonald_eye_chart_images.pdf")
    print("Saved McDonald eye chart as 'mcdonald_eye_chart_images.pdf'")
if SAVE_AS_PNG:
    img.save("mcdonald_eye_chart_images.png", optimize=True, compress_level=9)
    print("Saved McDonald eye chart as 'mcdonald_eye_chart_images.png'")
if SAVE_AS_WEBP:
    img.save("mcdonald_eye_chart_images.webp", lossless=True, quality=100, method=6)
    print("Saved McDonald eye chart as 'mcdonald_eye_chart_images.webp'")
