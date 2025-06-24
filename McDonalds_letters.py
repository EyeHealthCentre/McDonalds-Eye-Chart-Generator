from PIL import Image, ImageDraw, ImageFont
import math
import random

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

# Letters used in eye charts (no ambiguous ones)
letters: list[str] = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","R","S","T","U","V","W","X","Y","Z"]*2

img: Image.Image = Image.new("L", (IMG_SIZE, IMG_SIZE), "white")
draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

def get_font(size: float) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Utility: get text width and height using font.getbbox
def get_text_dimensions(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont) -> tuple[int | float, int | float]:
    bbox: tuple[float, float, float, float] | tuple[int, int, int, int] = font.getbbox(text)
    width: int | float = bbox[2] - bbox[0]
    height: int | float = bbox[3] - bbox[1]
    return width, height

# Draw central X
font_center: ImageFont.FreeTypeFont | ImageFont.ImageFont = get_font(FONT_SIZE_SCALING_FACTOR)
text = "X"
w: int | float
h: int | float
w, h = get_text_dimensions(text, font_center)
draw.text((CENTER - w/2, CENTER - h/2), text, font=font_center, fill="black")

# Draw each ring
for ring_idx, (radius, font_size) in enumerate(zip(radii, font_sizes)):
    angle_step: float = 360 / 8  # 8 letters per ring
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont = get_font(font_size)
    letters_in_ring: list[str] = list()

    for i in range(8):
        angle_deg: float = i * angle_step
        angle_rad: float = math.radians(angle_deg)

        # Get a random letter
        letter_index: int = random.randrange(len(letters))
        while letters[letter_index] in letters_in_ring:
            letter_index = random.randrange(len(letters))
        letter: str = letters.pop(letter_index)
        letters_in_ring.append(letter)

        # Calculate position on the ring
        x: float = CENTER + radius * math.cos(angle_rad)
        y: float = CENTER + radius * math.sin(angle_rad)

        # Center the text
        w, h = get_text_dimensions(letter, font)
        draw.text((x - w/2, y - h/2), letter, font=font, fill="black")

if SAVE_AS_PDF:
    img.save("mcdonald_eye_chart.pdf")
    print("Saved McDonald eye chart as 'mcdonald_eye_chart.pdf'")
if SAVE_AS_PNG:
    img.save("mcdonald_eye_chart.png", optimize=True, compress_level=9)
    print("Saved McDonald eye chart as 'mcdonald_eye_chart.png'")
if SAVE_AS_WEBP:
    img.save("mcdonald_eye_chart.webp", lossless=True, quality=100, method=6)
    print("Saved McDonald eye chart as 'mcdonald_eye_chart.webp'")
