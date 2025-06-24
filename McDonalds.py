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

def load_images(image_paths: list[str]) -> list[Image.Image]:
    image_objects: list[Image.Image] = []
    for path in image_paths:
        if os.path.exists(path):
            image_objects.append(Image.open(path).convert("RGBA"))
        else:
            print(f"Warning: Image not found: {path}")

    if not image_objects:
        raise ValueError("No valid image files found. Please check 'image_paths' list.")

    return image_objects

def get_font(size: float) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except IOError:
        return ImageFont.load_default()

def get_text_dimensions(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont) -> tuple[int, int] | tuple[float, float]:
    bbox: tuple[float, float, float, float] | tuple[int, int, int, int] = font.getbbox(text)
    width: int | float = bbox[2] - bbox[0]
    height: int | float = bbox[3] - bbox[1]
    return width, height

def draw_center_letter(imgdraw: ImageDraw.ImageDraw, font_size: int, text: str = "X") -> None:
    font_center: ImageFont.FreeTypeFont | ImageFont.ImageFont = get_font(font_size)
    w: int | float
    h: int | float
    w, h = get_text_dimensions(text, font_center)
    center: int = imgdraw._image.size[0] // 2
    imgdraw.text((center - w/2, center - h/2), text, font=font_center, fill="black")

def draw_letter_rings(imgdraw: ImageDraw.ImageDraw, radii: list[int], font_sizes: list[int], letters: list[str], letters_per_ring: int = 8) -> None:
    center: int = imgdraw._image.size[0] // 2
    for ring_idx, (radius, font_size) in enumerate(zip(radii, font_sizes)):
        angle_step: float = 360 / letters_per_ring
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont = get_font(font_size)
        letters_in_ring: list[str] = list()

        for i in range(letters_per_ring):
            angle_deg: float = i * angle_step
            angle_rad: float = math.radians(angle_deg)

            # Get a random letter
            letter_index: int = random.randrange(len(letters))
            while letters[letter_index] in letters_in_ring:
                letter_index = random.randrange(len(letters))
            letter: str = letters.pop(letter_index)
            letters_in_ring.append(letter)

            # Calculate position on the ring
            x: float = center + radius * math.cos(angle_rad)
            y: float = center + radius * math.sin(angle_rad)

            # Center the text
            w: int | float
            h: int | float
            w, h = get_text_dimensions(letter, font)
            imgdraw.text((x - w/2, y - h/2), letter, font=font, fill="black")

def draw_image_rings(img: Image.Image, radii: list[int], font_sizes: list[int], images: list[Image.Image], images_per_ring: int = 8) -> None:
    center: int = img.size[0] // 2
    for radius, size in zip(radii, font_sizes):
        angle_step: float = 360 / images_per_ring

        for i in range(images_per_ring):
            angle_deg: float = i * angle_step
            angle_rad: float = math.radians(angle_deg)

            # Randomly select and resize an image
            icon: Image.Image = random.choice(images)
            icon_resized: Image.Image = icon.resize((size, size), Image.Resampling.LANCZOS)

            # Compute position (centered)
            x: float = center + radius * math.cos(angle_rad) - size / 2
            y: float = center + radius * math.sin(angle_rad) - size / 2

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
