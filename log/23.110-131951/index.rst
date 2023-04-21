Setting up a UI for Explorer
============================

.. post::  23.110-131951
   :tags: 
   :category: 


- Tried to use PyQt6 as the GUI toolkit but faced issues with platform plugins
- Switched to using Tkinter for GUI development
- Implemented a modular design with separate classes for the header, footer, and main window
- Added a `Construction` class to the `geometor.core` package for creating and managing geometric constructions
- Added `Element`, `Point`, `Line`, and `Circle` classes to the `geometor.core` package for representing geometric elements
- Added a `MainWindow` class to the `geometor.explorer.ui` package for displaying the construction and interacting with the user
- Added a `MainPanel` class to the `geometor.explorer.ui` package for managing the three panels of the main window: the element list, the matplotlib view, and the view controls
- Added a `Footer` class to the `geometor.explorer.ui` package for displaying the details of selected elements and the actions for editing the model
- Added a `Header` class to the `geometor.explorer.ui` package for displaying key information about the model and buttons for model actions
- Demonstrated the use of docstrings and type annotations for improving code readability and maintainability

