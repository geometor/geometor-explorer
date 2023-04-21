import tkinter as tk
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

root = tk.Tk()

# Create a Matplotlib figure
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Set the tick labels to use LaTeX math expressions
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"
ax.set_xticklabels(["$\\alpha$", "$\\beta$", "$\\gamma$", "$\\delta$", "$\\epsilon$"])

# Create a list of LaTeX math expressions
expressions = [
    "\\frac{1}{2}",
    "\\sqrt{2}",
    "\\int_{0}^{\\infty} x^2 e^{-x} dx",
    "a^2 + b^2 = c^2",
    "\\sum_{n=1}^{\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}",
]

# Create a table with a single column of LaTeX math expressions
for i, expr in enumerate(expressions):
    ax.text(0, i, expr, fontsize=16, va="center")

# Create a canvas and display the figure in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

tk.mainloop()
