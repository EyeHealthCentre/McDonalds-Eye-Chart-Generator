from PIL import Image, ImageDraw

import McDonalds


if __name__ == "__main__":
    # Radii for the 4 rings (evenly spaced within the canvas)
    radii: list[int] = [int(McDonalds.RADII_SCALING_FACTOR*i) for i in [0.1, 0.2, 0.4, 0.8]]

    # Font sizes increasing outward
    font_sizes: list[int] = [int(McDonalds.FONT_SIZE_SCALING_FACTOR*i) for i in [1, 2, 4, 8]]

    # Letters used in eye charts (no ambiguous ones)
    letters: list[str] = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","R","S","T","U","V","W","X","Y","Z"]

    img: Image.Image = Image.new("L", (McDonalds.IMG_SIZE, McDonalds.IMG_SIZE), "white")
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    McDonalds.draw_center_letter(draw, McDonalds.FONT_SIZE_SCALING_FACTOR)
    McDonalds.draw_letter_rings(draw, radii, font_sizes)
    McDonalds.add_border(draw, McDonalds.DPI, 1.0, 127)

    if McDonalds.SAVE_AS_PDF:
        img.save("mcdonald_eye_chart.pdf")
        print("Saved McDonald eye chart as 'mcdonald_eye_chart.pdf'")
    if McDonalds.SAVE_AS_PNG:
        img.save("mcdonald_eye_chart.png", optimize=True, compress_level=9)
        print("Saved McDonald eye chart as 'mcdonald_eye_chart.png'")
    if McDonalds.SAVE_AS_WEBP:
        img.save("mcdonald_eye_chart.webp", lossless=True, quality=100, method=6)
        print("Saved McDonald eye chart as 'mcdonald_eye_chart.webp'")
