var DrawTL = new TimelineLite({paused: true});
var GoldenTL = new TimelineLite({paused: true});
const MUTEOPACITY = .3;


function animateGoldenSegments(){

  var allSegments = $('.Segment');
  GoldenTL.to(allSegments, 2, {strokeOpacity:0})
  var allMarkers = $('marker');
  GoldenTL.to(allMarkers, 2, {strokeOpacity:0})


  var allElements = $('.Line, .Circle');
  GoldenTL.to(allElements, 2, {strokeOpacity: MUTEOPACITY}, "-=2")
  var allPoints = $('.Point');
  GoldenTL.to(allPoints, 2, {fillOpacity: MUTEOPACITY}, "-=4")

  var j=0;

  golden.forEach( function(segPair) {
    console.group("golden pair", j++)
    // pause before starting
    // GoldenTL.to(allElements, 1, {strokeOpacity:MUTEOPACITY}, "-=1")
    var ancestors = [];
    var segPoints = [];

    segPair.forEach( function(segment) {
      segPoints[segment.points[0].id] = segment.points[0];
      segPoints[segment.points[1].id] = segment.points[1];
    })

    console.dir(segPair);
    console.dir(segPoints);

    // segPoints.forEach( function(point)  {
    //   getPointAncestors(point, this);
    // }, ancestors)

    for ( point in segPoints ) {
      getPointAncestors(segPoints[point], ancestors);
    }

    console.group("ancestors");
    console.dir(ancestors);

    ancestors.forEach( function(element) {
      var id;
      if ( element.type === "line" ) {
        id = "#i" + element.id
      }
      if ( element.type === "circle" ) {
        id = "#c" + element.id
      }
      if (id) {
        console.log(id + "\n")
        GoldenTL.to(id, .5, {strokeOpacity:1, fillOpacity: .05}, "-=.4")
      }
    })

    segPoints.forEach( function(point) {
      GoldenTL.to("#p" + point.id, .5, {fillOpacity: 1}, "-=.25")
    })

    GoldenTL.to(segPair[0].markerStart, .5, {strokeOpacity:1}, "+=0")
            .to(segPair[0].markerEnd, .5, {strokeOpacity:1}, "-=.25")
            .to(segPair[1].markerStart, .5, {strokeOpacity:1}, "+=0")
            .to(segPair[1].markerEnd, .5, {strokeOpacity:1}, "-=.25")

    GoldenTL.to("#s" + segPair[0].id, .5, {strokeOpacity:1}, "+=0")
            .to("#s" + segPair[1].id, .5, {strokeOpacity:1}, "-=.25")
            // pause on completed image
    GoldenTL.to("#s" + segPair[0].id, .5, {strokeOpacity:0}, "+=3.0")
            .to("#s" + segPair[1].id, .5, {strokeOpacity:0}, "-=.25")

    GoldenTL.to(segPair[1].markerStart, .5, {strokeOpacity:0}, "-=.5")
            .to(segPair[1].markerEnd, .5, {strokeOpacity:0}, "-=.25")
            .to(segPair[0].markerStart, .5, {strokeOpacity:0}, "+=0")
            .to(segPair[0].markerEnd, .5, {strokeOpacity:0}, "-=.25")

    segPoints.forEach( function(point) {
      GoldenTL.to("#p" + point.id, .5, {fillOpacity: MUTEOPACITY}, "-=.25")
    })

    // unwind the ancestors
    console.log("reverse");

    ancestors.reverse().forEach( function(element) {
      var id;
      if ( element.type === "line" ) {
        id = "#i" + element.id
      }
      if ( element.type === "circle" ) {
        id = "#c" + element.id
      }
      if (id) {
        console.log(id + "\n")
        GoldenTL.to(id, .5, {strokeOpacity:MUTEOPACITY, fillOpacity: 0}, "-=.4")
      }
    })
    console.groupEnd();

    // pause between
    GoldenTL.to(allElements, 1, {strokeOpacity:MUTEOPACITY}, "+=0")
    console.groupEnd();
  });
  GoldenTL.to(allElements, 2, {strokeOpacity:1})
  GoldenTL.to(allPoints, 2, {fillOpacity:1}, "-=2")

  GoldenTL.to(allSegments, 2, {strokeOpacity:.3}, "-=2")
  GoldenTL.to(allMarkers, 0, {strokeOpacity:.3})

  GoldenTL.play();

}
