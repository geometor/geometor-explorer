# GEOMETOR • explorer

Currently GEOMETOR Explorer is organized around three concepts that are independent but connected - like a venn diagram.
- modeling
- analyzing
- rendering

a model is constructed from a sequence of operations with a starting condition
an analysis is generated from an identification of patterns in the model
a rendering is a visual interpretation of the model and the analysis

The model holds symbolic values and relationships of a defined algebraic structure.
The analysis compares the model's values and relationships then creates its own sets of symbolic values and relationships based on pattern templates.
Rendering is like the collapse of the wave function in physics, where the symbolic form is converted to the real form so that computers can approximate the form with pixels. Or graphical symbols like LaTeX.

So, the analysis can be anything. For instance, I currently take all the points on a line, sort them, then generate all the combinations of three points to identify the golden sections. I started working on finding the harmonic ranges as well. There are many other attributes to examine, for instance, the relation of points on the circles, etc.

This is computationally intensive though. The number of combinations to test can get really large. I have been experimenting with Python's multiprocessing library to parallelize the testing.

~ φ
