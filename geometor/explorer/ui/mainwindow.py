from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QTextEdit,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create the main layout
        main_layout = QVBoxLayout()

        # Create the header widgets
        header_layout = QHBoxLayout()
        header_label = QLabel("Model Name")
        open_button = QPushButton("Open")
        save_button = QPushButton("Save")
        header_layout.addWidget(header_label)
        header_layout.addWidget(open_button)
        header_layout.addWidget(save_button)

        # Create the footer widgets
        footer_layout = QHBoxLayout()
        details_text = QTextEdit()
        add_button = QPushButton("Add Element")
        footer_layout.addWidget(details_text)
        footer_layout.addWidget(add_button)

        # Create the splitter
        splitter = QSplitter()

        # Create the element list layout
        element_list_layout = QVBoxLayout()
        element_list_layout.addWidget(QLabel("Element List"))
        splitter.addWidget(QWidget())

        # Create the view controls layout
        view_controls_layout = QVBoxLayout()
        view_controls_layout.addWidget(QLabel("View Controls"))
        splitter.addWidget(QWidget())

        # Add the header and footer layouts to the main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(splitter)
        main_layout.addLayout(footer_layout)

        # Set the main layout
        self.setLayout(main_layout)
