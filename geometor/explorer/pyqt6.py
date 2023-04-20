"""The `geometor.explorer.main` module is the entry point of the application, responsible for initializing the construction, setting up the GUI components, and launching the main window of the application.

The `main()` function is the main entry point of the module, which performs the following tasks:
- Initializes a `Construction` object with some default geometric elements
- Initializes a `QApplication` object from `PyQt6`
- Creates a `MainWindow` object with the construction and shows the window
- Starts the event loop of the application

Example usage:
the application from the command line

```
python -m geometor.explorer
```
Or run the application as a script

```
python geometor/explorer/main.py
```
"""
import sys

from PyQt6.QtWidgets import QApplication
from geometor.explorer.ui.mainwindow import MainWindow

#  from geometor.explorer.core.construction import Construction
#  from geometor.explorer.core.point import Point
#  from geometor.explorer.core.line import Line
#  from geometor.explorer.core.circle import Circle


def main():
    # Initialize the construction with some default elements
    #  construction = Construction(
    #  elements=[
    #  Point(x=0, y=0),
    #  Point(x=1, y=0),
    #  Line(start=Point(x=0, y=0), end=Point(x=1, y=0)),
    #  Circle(center=Point(x=0, y=0), radius=1),
    #  ]
    #  )

    # Initialize the PyQt application
    app = QApplication(sys.argv)

    # Create the main window and show it
    #  window = MainWindow(construction=construction)
    window = MainWindow()
    window.show()

    # Start the event loop of the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
