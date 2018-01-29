# geometor-explorer
a browser-based graphics and animation engine for exploring classical constructive geometry and  documenting instances of Golden Sections.

The **GEOMETOR Explorer** is an essential tool for the GEOMETOR Project.

The purpose of **Explorer** is to find and catalogue unique instances of golden sections within geometric constructions with algebraic proofs.

**Explorer** is currently a demonstration prototype. There are significant plans for enabling user interactivity including creating lines and circles within the field, as well as analysis of the discovered golden sections.

## classical constructive geometry

**Explorer** operates under the rules of classical constructive geometry within a planar field. Explorer provides two virtual tools for constructions - an unmarked straight edge and a compass. Both of these tools require two points to operate. We align the straightedge with two points to make a line. We align the compass with two points to draw a circle. This simple framework for the study of geometric proportions has been with us since the ancients and is the foundation of Euclid's Elements.

Every geometric construction within **Explorer** begins with a blank slate. The only "givens" are the first two **starting points** on our field. Everything else must be constructed.

The distance between these two starting points represents the unit measure of the field - a distance of one. All other constructions are expressed in proportion to this unit.

The intersections of lines and circles identify new points on our field - creating opportunities for more lines and circles - and of course, more intersection points.

Line **segments** and circular **sectors** and **arcs** are used within **Explorer** as graphical illustrations and are not used directly in constructions.

Lines and circles are proportions that extend from their origins without end. Therefore, lines are always extended beyond the screen and circles are always drawn in full. By expressing the elements fully, we allow for more discovery of relationships and intersections.

## cartesian grid and algebra

While following the formality of Euclid's constructive geometry, **Explorer** incorporates two concepts that were undeveloped in Euclid's time: the cartesian grid and algebra.

With our unit measure established by the starting points and a notion of perpendicularity, we establish a horizontal (x) and vertical (y) scale. We use these scales to identify the position of points as `[x y]`.

The origin is the point half way between the starting points. In the cartesian plane this is `[0 0]`.

As our givens, the starting points are the only points without parents and are placed on the field with positions of `[1/2 0]` and `[-1/2 0]`

All other points are derived algebraically from the intersection of elements.

> Decimal equivalents are for applied mathematics. All calculations within **Explorer** are algebraic.


# How **Explorer** works

Constructions within **Explorer** are currently scripted. Lines and Circles are created by passing Point references as parameters.

Explorer maintains an array of constructed points and elements.

```js

//initial points set by X Y
Point( "-1/2", "0" );
Point( "1/2", "0" );

//baseline
Line( points[0], points[1] );

// vesica pisces
Circle( points[0], points[1] );
Circle( points[1], points[0] );

// //bisector
Line( points[4], points[5] );

// unit 2 circles from starting points
Circle( points[0], points[3] );
Circle( points[1], points[2] );

```
Elements and points are shown in the Side panel.

Each element is added to an animation timeline. The timeline plays after the construction.


## golden sections

Explorer then examines the points on each line for golden sections. The participating segments are highlighted.

The "Animate Segments" link on menu bar will cycle through each pair of golden section segments highlighting the segments allng with the parent elements necessary to 



## ancestors

Every point in the field is fully traceable - both algebraically and geometrically - back to the starting points.

**Explorer** uses

# How it works


## the drawing
-


The GEOMETOR Project is a collaborative effort to explore the architecture of all that is.

Whether we look at the architecture of nature (matter) or the architecture of logic (mind) - a resonance emerges in the form of a simple proportion. Great philosophers and scientists throughout history, when encountering this proportion and its many attributes, felt a reverence - giving it names like the "Golden Ratio" and the "Divine Proportion."


## The future

- deep recursion
- analytics
-
