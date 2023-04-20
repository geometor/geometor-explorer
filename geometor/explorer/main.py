import tkinter as tk
from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("GEOMETOR Explorer")

        # Create the header
        self.header_frame = ttk.Frame(self.master, padding=(10, 10, 10, 0))
        self.header_frame.pack(fill="x")

        # Create the main window
        self.main_frame = ttk.Frame(self.master, padding=(10, 10))
        self.main_frame.pack(fill="both", expand=True)

        # Create the left panel
        self.left_panel = ttk.Frame(self.main_frame, width=200, padding=(0, 0, 10, 0))
        self.left_panel.pack(side="left", fill="y")

        # Create the center panel
        self.center_panel = ttk.Frame(self.main_frame)
        self.center_panel.pack(side="left", fill="both", expand=True)

        # Create the right panel
        self.right_panel = ttk.Frame(self.main_frame, width=200, padding=(10, 0, 0, 0))
        self.right_panel.pack(side="left", fill="y")

        # Create the footer
        self.footer_frame = ttk.Frame(self.master, padding=(10, 0, 10, 10))
        self.footer_frame.pack(fill="x")

        # Create the header widgets
        ttk.Label(
            self.header_frame, text="GEOMETOR Explorer", font=("TkDefaultFont", 16)
        ).pack(side="left", padx=(0, 10))
        ttk.Button(self.header_frame, text="Open", command=self.open_model).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(self.header_frame, text="Save", command=self.save_model).pack(
            side="left", padx=(0, 10)
        )

        # Create the left panel widgets
        ttk.Label(self.left_panel, text="Element List").pack()

        # Create the center panel widgets
        ttk.Label(self.center_panel, text="Matplotlib View").pack()

        # Create the right panel widgets
        ttk.Label(self.right_panel, text="View Controls").pack()

        # Create the footer widgets
        ttk.Label(self.footer_frame, text="Selected Element Details").pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(self.footer_frame, text="Add Line", command=self.add_line).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(self.footer_frame, text="Add Circle", command=self.add_circle).pack(
            side="left", padx=(0, 10)
        )
        ttk.Button(self.footer_frame, text="Add Point", command=self.add_point).pack(
            side="left", padx=(0, 10)
        )

    def open_model(self):
        print("Open model")

    def save_model(self):
        print("Save model")

    def add_line(self):
        print("Add line")

    def add_circle(self):
        print("Add circle")

    def add_point(self):
        print("Add point")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
