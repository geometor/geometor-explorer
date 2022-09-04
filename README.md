# GEOMETOR • explorer

GEOMETOR Explorer is a Python library for modelling, analyzing and rendering
complex geometric constructions using symbolic algebra. Of course, Sympy is at
the heart of it. 

**GEOMETOR Explorer** is an essential tool of the GEOMETOR Project. You can
learn more about our collaborative research project on
[geometor.com](http://geometor.com)

The purpose of **Explorer** is to find and catalogue unique instances of golden
sections within geometric constructions with algebraic proofs.  But first, an
introduction. My friends call me phi, as in φ, the Greek letter, for reasons
that will be obvious. I am not a mathematician, but I have had a career as an
architect beginning with buildings and later in developing software and
enterprise systems. But my true love has always been drafting - making beautiful
drawings.

A few years ago, I decided to indulge my interest in the golden ratio,
particularly making geometric constructions that demonstrate golden sections. I
started with hand drawings, reteaching myself geometry and algebra. I noticed
that constructing one golden section often led to other sections in the field.
It seemed to be everywhere. But the challenge of demonstrating that was
daunting. I first turned to Geogebra, which greatly expanded my knowledge
allowing me to create large geometric constructions and confirm the golden
sections, but it required a lot of manual intervention and the results were
numeric values. I felt if we were to really discover patterns, we would need to
build the model symbolically.

I set out to develop a scriptable system to generate the constructions, find
all intersection points, and then find all the golden sections. After a false
start with a browser-based solution, last January I found Sympy and Matplotlib.
I had never worked with Python before so it was a big step, but the capabilities
I have been able to pull together in less than a year are amazing to me.

The most recent video on my YouTube channel demonstrates a series of
constructions generated with GEOMETOR Explorer resulting in an incredible
numbers of golden sections uncovered.  22.187 • finding golden sections with the
new GEOMETOR Explorer

GEOMETOR on Github I have established a Github organization
(https://github.com/geometor) to be the center of all of the development and
interaction around the projects, including hosting websites and documentation.

Shifting GEOMETOR Explorer to Python has led me to shift all my content
development and publishing tools to Python, as well. This will allow me to
standardize on ReST for everything. So, the websites are in a state of flux but
I have most the infrastructure in place.

There is a lot to further develop. At the core are the GEOMETOR Explorer
libraries. The current version in the main branch is very "scripty" - grown
organically as I was learning. In the develop branch, I have started refactoring
the library into a simpler and more functional interface and adding
documentation. I also want to add more analysis capabilities to identify
harmonic ranges / symmetries. And ultimately, publish a reliable version for
anyone to use on PyPI.

Context for further development:

-   Deep Field project how many elements can we add to a geometric model?  how
    many more golden sections in the field?  generating large models is compute
    intensive - will it push Sympy to limits?
-   Euclid project create a functional hierarchy of all the constructions of
    Euclid's Elements development on parsing the heath edition Phyllotaxis
    project study golden ratio and fibonacci patterns in plant formation 3d
    modeling
-   Polynumbers project based on the lectures of Norman Wildberger introduces
    polynomials into the Explorer capabilities crazy cool renderings
-   Pappus project demonstrate Pappus Theorem with analysis leading to
    Hexagrammum Mysticum.
-   Heptadecagon project create a symbolic construction of a regular 17-sided
    figure

I hope this is enough to start a conversation. I have been wanting to step into
the Sympy community for some time. Consider it done.

I have two YouTube channels if you want to see more:

-   phi ARCHITECT channel where I talk about what I am working on
-   GEOMETOR channel generated content from the research. The most recent videos
    were generated, orchestrated, accompanied and assembled with Python.

Currently GEOMETOR Explorer is organized around three concepts that are
independent but connected - like a venn diagram.

- modeling
- analyzing
- rendering

a model is constructed from a sequence of operations with a starting condition
an analysis is generated from an identification of patterns in the model a
rendering is a visual interpretation of the model and the analysis

The model holds symbolic values and relationships of a defined algebraic
structure.  The analysis compares the model's values and relationships then
creates its own sets of symbolic values and relationships based on pattern
templates.  Rendering is like the collapse of the wave function in physics,
where the symbolic form is converted to the real form so that computers can
approximate the form with pixels. Or graphical symbols like LaTeX.

So, the analysis can be anything. For instance, I currently take all the points
on a line, sort them, then generate all the combinations of three points to
identify the golden sections. I started working on finding the harmonic ranges
as well. There are many other attributes to examine, for instance, the relation
of points on the circles, etc.

This is computationally intensive though. The number of combinations to test can
get really large. I have been experimenting with Python's multiprocessing
library to parallelize the testing.

---

The next step for GEOMETOR Explorer is to consolidate the construction logic
into a Model class, which could easily become a part of sympy.geometry. The
Model can extend from List - so it is just a container of elements. But it would
also handle:

-   deduplicating elements determine if an new element is already in the list.
-   finding intersections test new elements against previous elements for new
    points.
-   maintaining ancestral relationships points contain references to all parent
    structures.  structures contain references to all the points on them.  the
    ancestral trail of an element is its proof.
-   applying classes to elements like css, associate a list of class names to an
    element.  classes could be used in rendering and analysis.  classes could
    also be used to exclude a structure from testing intersections.
-   querying subsets provide filtered lists for specific element types or
    classes

In the work I have done so far, I have come to think of elements in 3
categories:

-   points the data of the model.  all points are derived except the given
    starting points.  points are the food for structs.
-   structs the relationships of the model (lines and circles so far).  structs
    are not a thing in the field, just a projection of a relationship of two
    points.  intersecting structs create points.
-   graphics the highlights of the model (segments, polygons, wedges).  like
    structs, but are used for highlighting a relationship of 2 or more points
    and extracting details (length, area, etc).  graphics are not tested for
    intersections by default.

---


## classical constructive geometry

**Explorer** operates under the rules of classical constructive geometry within
a planar field. Explorer provides two virtual tools for constructions - an
unmarked straight edge and a compass. Both of these tools require two points to
operate. We align the straightedge with two points to trace a line. We align the
compass with two points to trace a circle. This simple framework for the study
of geometric proportions has been with us since the ancients and is the
foundation of Euclid's Elements.

Every geometric construction within **Explorer** begins with a blank slate. The
only "givens" are the first two **starting points** on our field. Everything
else must be constructed.

The distance between these two starting points represents the unit measure of
the field - a distance of one. All other constructions are expressed in
proportion to this unit.

The intersections of lines and circles identify new points on the field -
creating opportunities for more lines and circles - and of course, more
intersection points.

Line **segments** and circular **sectors** and **arcs** are used within
**Explorer** as graphical illustrations and are not used directly in
constructions.

Lines and circles are proportions that extend from their initial points without
end. Therefore, lines are always extended beyond the screen and circles are
always drawn in full. By expressing the elements fully, we allow for more
discovery of relationships and intersections.

## cartesian grid and algebra

While following the formality of Euclid's constructive geometry, **Explorer**
incorporates two concepts that were undeveloped in Euclid's time: the cartesian
grid and algebra.

With our unit measure established by the starting points and a notion of
perpendicularity, we establish a horizontal (x) and vertical (y) scale. We use
these scales to identify the position of points as `[x y]`.

The origin is the point half-way between the starting points. In the cartesian
plane this is `[0 0]`.

As our givens, the starting points are the only points without parents and are
placed on the field with positions of `[1/2 0]` and `[-1/2 0]`

All other points are derived algebraically from the intersection of elements.

> Decimal equivalents are for applied mathematics. All calculations within
> **Explorer** are algebraic.


# How **Explorer** works

Constructions within **Explorer** are currently scripted. Lines and Circles are
created by passing Point references as parameters.

Explorer maintains an array of constructed points and elements.

Here is the script that constructs the current geometry at index.html.


---


## golden sections

Explorer examines the points on each line for golden sections. The participating
segments are highlighted in the construction.

The "Animate Segments" link on menu bar will cycle through each pair of golden
section segments highlighting the segments along with the parent elements
necessary to construct the segments.

## ancestors

Every point in the field is fully traceable - both algebraically and
geometrically - back to the starting points.

## algebra

<!-- Explorer uses the amazing javascript algebra library,
[Algebrite](http://algebrite.org/), to handle the calculations under the
construction. -->

<!-- Katex is used to render the algebraic expressions. -->


## The future...

- deep automated recursion to explore the geometric field
- analysis of golden section instances to look for patterns

# The GEOMETOR Project

The GEOMETOR Project is a collaborative effort to explore the architecture of
all that is.

Whether we look at the architecture of nature (matter) or the architecture of
logic (mind) - a resonance emerges in the form of a simple proportion. Great
philosophers and scientists throughout history, when encountering this
proportion and its many attributes, felt a reverence - giving it names like the
"Golden Ratio" and the "Divine Proportion."

The GEOMETOR Project is an effort to document the fascinating attributes of the
Golden Ratio and to seek a deeper understanding of its pervasive beauty.
