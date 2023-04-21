from PIL import Image, ImageDraw, ImageFont
import os

# Define the project root directory
PROJECT_ROOT = "geometor_explorer"

# Define the package directories and subdirectories
PACKAGE_DIRS = [
    "ui",
    "core",
    "resources",
    "ui/dialogs",
    "resources/icons"
]

# Define the font size and type for the icon characters
FONT_SIZE = 12
FONT_PATH = "/usr/share/fonts/opentype/fira/FiraSans-Regular.otf"

# Define the icons and their background colors
ICONS = [
    ("add_point", "P", (238, 252, 255)),
    ("add_line", "L", (255, 247, 236)),
    ("add_circle", "C", (255, 238, 238)),
    ("delete", "X", (240, 244, 255)),
    ("save", "S", (249, 235, 248)),
    ("open", "O", (238, 255, 246))
]

def generate_icons():
    """Generate the toolbar icons for the application."""

    # Create the icon images and save them as PNG files
    for icon_path, icon_letter, background in ICONS:
        # Create a new image with the background color
        img = Image.new("RGB", (24, 24), background)

        # Draw the icon character in black
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        w, h = draw.textsize(icon_letter, font=font)
        draw.text(((24 - w) / 2, (24 - h) / 2), icon_letter, font=font, fill=(0, 0, 0))

        # Save the image as PNG
        img.save(os.path.join(PROJECT_ROOT, "resources/icons", f"{icon_path}.png"))

generate_icons()
