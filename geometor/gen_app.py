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

# Define the file names and their docstring intros
FILE_NAMES = [
    ("__init__.py", ""),
    ("main.py", '"""The entry point of the application."""'),
    ("ui/__init__.py", '"""The user interface components."""'),
    ("ui/mainwindow.py", '"""The main window of the application."""'),
    ("ui/sidepanel.py", '"""The side panel that displays the list of elements."""'),
    ("ui/propertiespanel.py", '"""The properties panel that displays the properties of selected elements."""'),
    ("ui/dialogs/__init__.py", '"""The dialog boxes for adding new elements."""'),
    ("ui/dialogs/addpointdialog.py", '"""The dialog box for adding a new point."""'),
    ("ui/dialogs/addlinedialog.py", '"""The dialog box for adding a new line."""'),
    ("ui/dialogs/addcircledialog.py", '"""The dialog box for adding a new circle."""'),
    ("core/__init__.py", '"""The core components of the application."""'),
    ("core/construction.py", '"""The module for creating and managing the geometric construction."""'),
    ("core/element.py", '"""The base class for all geometric elements."""'),
    ("core/point.py", '"""The module for creating a point."""'),
    ("core/line.py", '"""The module for creating a line."""'),
    ("core/circle.py", '"""The module for creating a circle."""'),
    ("resources/__init__.py", '"""The resources used by the application."""'),
    ("resources/styles.qss", '"""The stylesheet for the application."""'),
    ("resources/icons/__init__.py", '"""The icons used by the toolbar buttons."""'),
    ("resources/icons/add_point.png", '"""The icon for the "Add Point" button."""'),
    ("resources/icons/add_line.png", '"""The icon for the "Add Line" button."""'),
    ("resources/icons/add_circle.png", '"""The icon for the "Add Circle" button."""'),
    ("resources/icons/delete.png", '"""The icon for the "Delete" button."""'),
    ("resources/icons/save.png", '"""The icon for the "Save" button."""'),
    ("resources/icons/open.png", '"""The icon for the "Open" button."""')
]

# Define the font size and type for the icon characters
FONT_SIZE = 12
FONT_PATH = "Calibri"

# Define the background colors and the characters for the icons
BACKGROUNDS = [
    (238, 252, 255),
    (255, 247, 236),
    (255, 238, 238),
    (240, 244, 255),
    (249, 235, 248),
    (238, 255, 246)
]
ICONS = ["P", "L", "C", "X", "S", "O"]

# Create the package directories and subdirectories
for package_dir in PACKAGE_DIRS:
    os.makedirs(os.path.join(PROJECT_ROOT, package_dir), exist_ok=True)

# Create the placeholder icons and Python files
for file_name, docstring_intro in FILE_NAMES:
    # Get the file extension
    file_ext = os.path.splitext(file_name)[1]

    # Create the file based on the extension
    if file_ext == ".png":
        # Create a new image with the background color
        i = ICONS.index(file_name.split(".")[0])  # Get the index of the current icon
        img = Image.new("RGB", (24, 24), BACKGROUNDS[i])

        # Draw the icon character in black
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        w, h = draw.textsize(ICONS[i], font=font)
        draw.text(((24 - w) / 2, (24 - h) / 2), ICONS[i], font=font, fill=(0, 0, 0))

        # Save the image as PNG
        img.save(os.path.join(PROJECT_ROOT, file_name))

    elif file_ext == ".py":
        # Create an empty Python file with the docstring intro
        with open(os.path.join(PROJECT_ROOT, file_name), "w") as f:
            f.write(docstring_intro)

    else:
        # Create an empty file without a docstring intro
        with open(os.path.join(PROJECT_ROOT, file_name), "w"):
            pass

