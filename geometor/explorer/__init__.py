"""The `geometor.explorer` package provides an interactive graphical user interface (GUI) for creating and visualizing geometric constructions.

The application is built on top of the `geometor` library, which provides a set of classes and functions for creating, analyzing, and rendering geometric models. The `geometor.explorer` package uses `PyQt6` for creating the GUI, and `matplotlib` for rendering the geometric models.

The main entry point of the application is the `main.py` module, which launches the main window of the application. The main window contains a toolbar with buttons for creating new geometric elements, a side panel for displaying the list of elements, and a properties panel for displaying the properties of selected elements.

To use the `geometor.explorer` package, import the desired modules and classes from the package and call their methods as needed. The package also includes a set of dialog boxes for adding new geometric elements, which can be accessed through the toolbar buttons.

Example usage:
```python
from geometor.explorer.ui.mainwindow import MainWindow
from geometor.core.point import Point
Create a new point object

point = Point(x=0, y=0)
```
Create the main window of the application and add the point to the construction

```
window = MainWindow(construction=[point])
window.show()
```
"""

#  As for any code to include in the `__init__.py` file, you can use it to define
#  any package-level variables, classes, or functions that are used by multiple
#  modules in the package. For example, you could define a `PROJECT_ROOT` variable
#  that points to the root directory of the project, or a `DEFAULT_FONT_SIZE`
#  constant that specifies the default font size for the GUI. However, for a small
#  project like this, it may not be necessary to define any package-level code in
#  the `__init__.py` file.

