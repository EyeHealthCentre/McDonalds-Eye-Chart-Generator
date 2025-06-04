from PIL import Image, ImageDraw, ImageFont
import math
import random

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

# Letters used in eye charts (no ambiguous ones)
LETTERS = 'ABCDEFGHJKLMNOPRSTUVWXYZ'

# Create image and draw object
img = Image.new("1", (IMG_SIZE, IMG_SIZE), "white")
draw = ImageDraw.Draw(img)

# Load a font (you can replace this with a path to a font you prefer)
def get_font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except IOError:
        return ImageFont.load_default()

# Utility: get text width and height using font.getbbox
def get_text_dimensions(text, font):
    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height

# Draw central X
font_center = get_font(FONT_SIZE_SCALING_FACTOR)
text = "X"
w, h = get_text_dimensions(text, font_center)
draw.text((CENTER - w/2, CENTER - h/2), text, font=font_center, fill="black")

# Draw each ring
for ring_idx, (radius, font_size) in enumerate(zip(radii, font_sizes)):
    angle_step = 360 / 8  # 8 letters per ring
    font = get_font(font_size)
    
    for i in range(8):
        angle_deg = i * angle_step
        angle_rad = math.radians(angle_deg)

        # Get a random letter
        letter = random.choice(LETTERS)
        
        # Calculate position on the ring
        x = CENTER + radius * math.cos(angle_rad)
        y = CENTER + radius * math.sin(angle_rad)
        
        # Center the text
        w, h = get_text_dimensions(letter, font)
        draw.text((x - w/2, y - h/2), letter, font=font, fill="black")

# Save image
img.save("mcdonald_eye_chart.png", optimize=True, compress_level=9)
print("Saved McDonald eye chart as 'mcdonald_eye_chart.png'")
img.save("mcdonald_eye_chart.webp", lossless=True, quality=100, method=6)
print("Saved McDonald eye chart as 'mcdonald_eye_chart.webp'")
img.save("mcdonald_eye_chart.pdf")
print("Saved McDonald eye chart as 'mcdonald_eye_chart.pdf'")
