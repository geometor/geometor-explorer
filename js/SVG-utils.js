//init panels
var pointsPanel = document.getElementById('points');
if ( !pointsPanel ) {
  console.log('pointsPanel not found');
}

var linesPanel = document.getElementById('lines');
if ( !linesPanel ) {
  console.log('linesPanel not found');
}

var circlesPanel = document.getElementById('circles');
if ( !circlesPanel ) {
  console.log('circlesPanel not found');
}

var segmentsPanel = document.getElementById('segments');
if ( !segmentsPanel ) {
  console.log('segmentsPanel not found');
}

var infoPanel = document.getElementById('info');
if ( !infoPanel ) {
  console.log('infoPanel not found');
}

var footerPanel = document.getElementById('footer');
if ( !footerPanel ) {
  console.log('footerPanel not found');
}


///////////////////////////////////////////////////////////////////////////////

function log (msg) {
  // segmentsPanel.innerHTML += msg + '\n';
  console.log(msg + '\n');
}

function logPoint (point) {
  var item = point.id + `  ( ${point.x},\t${point.y} ) \n`;
  pointsPanel.innerHTML += item;
  // ÷=console.log(item);
}

function logLine (line) {
  var item = line.id + `  [${line.points[0].id}, ${line.points[1].id}] ${line.eq} = 0 \n`;
  linesPanel.innerHTML += item;
  // console.log(item);
}

function logCircle (circle) {
  var item = circle.id + `  ( ${circle.h}, ${circle.k} )\t${circle.r}\t${circle.eq} = 0 \n`;
  circlesPanel.innerHTML += item;
  // console.log(item);
}

function logSegments (str) {
  //  var item = circle.id + `  ( ${circle.h}, ${circle.k} )\t${circle.r}\t${circle.eq} = 0 \n`;
  segmentsPanel.innerHTML += str;
  // console.log(str);
}

function footer (msg) {
  footerPanel.innerHTML += msg + '\n';
  console.log(msg + '\n');
}

function logSummary() {
  log("--------------------------");
  log("summary");
  log("");
  log("points: " + points.length);
  log("elements: " + elements.length);

}

///////////////////////////////////////////////////////////////////////////////

//pass in line coefficients to find endpoints at viewbox
function getViewboxIntersection(line) {
  //get bounds to margin for the line
  var box = D.viewbox();
  var bx1 = box.x;
  var by1 = box.y;
  var bx2 = box.x + box.width;
  var by2 = box.y + box.height;

  var x1, x2, y1, y2;

  //if vertical flip the calls around and override
  if (line.xRoot) {
    x1 = getNumber(line.getX(by1));
    if (!isNaN(x1)) {
      y1 = by1;
    } else {
      //vertical line
      x1 = bx1;
      y1 = getNumber(line.getY(bx1));
    }

    var x2 = getNumber(line.getX(by2));
    if (!isNaN(x2)) {
      y2 = by2;
    } else {
      //vertical line
      x2 = bx2;
      y2 = getNumber(line.getY(bx1));
    }
  } else {
    y1 = getNumber(line.getY(bx1));
    if (!isNaN(y1)) {
      x1 = bx1;
    } else {
      //vertical line
      y1 = by1;
      x1 = getNumber(line.getX(by1));
    }

    var y2 = getNumber(line.getY(bx2));
    if (!isNaN(y2)) {
      x2 = bx2;
    } else {
      //vertical line
      y2 = by2;
      x2 = getNumber(line.getX(by1));
    }
  }
  return [x1, y1, x2, y2];
}

//check all points ona line for Golden Ration instances
function checkSegments(line) {

  console.groupCollapsed("line: " + line.id + "");

  // clone points before sorting
  var points = line.points.slice(0);

  // sort points on the line
  points.sort( comparePoints );

  //check for golden ratio
  // const GR = "1/2 + 1/2 5^(1/2)"
  // const GRval = alg( `float(${GR})`)

  for (var i = 0; i < points.length-2; i++) {
    //get first segment point
    var pt1 = points[i];

    console.groupCollapsed("(" + pt1.id + ")");


    var cmd = `clearall
      PHI = 1/2 + 1/2 5^(1/2)
      `;
    alg(cmd);

    //loop the remaining points to set first segment
    for (var j = i+1; j < points.length-1; j++) {
      var pt2 = points[j];

      // get the length of the first segment
      cmd = `A = ${pt1.distanceTo(pt2)}
      A
      `;
      var A = alg(cmd);

      if ( checkValid(A) ){

        console.groupCollapsed(`> (${pt2.id}) : ${A} ` );

        // loop the remaining points to set second segment
        for (var k = j+1; k < points.length; k++) {
          var pt3 = points[k];

          // get the length of the second segment
          cmd = `B = ${pt2.distanceTo(pt3)}
          B
          `;
          var B = alg(cmd);

          if ( checkValid(B) ){

            // console.groupCollapsed(`>> (${pt3.id}) : ${B} = ${Bval}` );
            console.groupCollapsed(`>> (${pt3.id}) : ${B}` );

            // get the ratio fo the segments
            cmd = `R = simplify( A / B )
            R
            `;
            var ratio = alg(cmd);

            log("        * ratio: " + ratio  );

            var check = alg(` R - PHI `);
            var checkVal = alg( `float( R - PHI )`)

            log("check: " + check   );
            log("  val: " + checkVal  );

            if ( checkVal == 0 || checkVal == -1 ) {
              //Success!
              var str = `[${line.id}] : ${pt1.id}> ${A} <${pt2.id}> ${B} <${pt3.id}
        : ${ratio}\n`;
              console.warn("Golden! ", str );
              logSegments( str );
              var s1 = addSegment(pt1, pt2, line);

              var s2 = addSegment(pt2, pt3, line);
              golden.push([s1, s2]);

            }
            console.groupEnd();
          } else {
            // B not valid
          }
        } //for k
        console.groupEnd();
      } else {
        // A not valid
      }
    } // for j
    console.groupEnd();
  } // for i
  console.groupEnd();
}

// maintain single instance of a segment
function addSegment(pt1, pt2, line) {
  // look for a segment on the line with matching points
  var seg = segments.filter( function (segment) {
      if ( segment.line === line ) {
        if ( segment.points.includes(pt1) && segment.points.includes(pt2) ) {
          return true
        }
      }
    });

  if ( seg.length != 0 ) {
    return seg[0]
  } else {
    return new Segment( pt1, pt2, line )
  }

}

function getPointAncestors(point, ancestors) {
  //stop at starting points
  console.group("point: " + point.id)
  if ( point.id == "0" || point.id == "1" ) {
    // end with starting points
    console.warn("skip this point")

  } else {


    // get first two parents on point
    for (var i = 0; i <=1; i++) {

      var parent = point.parents[i];

      //don't repeat parents in array
      if (!ancestors[parent.id]) {
        console.group("parent: " + parent.id);
        ancestors[parent.id] = parent;


        if ( parent.type === "line" ) {
          getPointAncestors( parent.points[0], ancestors );
          getPointAncestors( parent.points[1], ancestors );

        }
        if ( parent.type === "circle" ) {
          // getPointAncestors( parent.center, ancestors );
          getPointAncestors( parent.points[0], ancestors );
        }


        console.groupEnd();
      } else {
        //ancestor already in list
      }
    }

  }
  console.groupEnd();

}

// call checkSegments for all lines
function checkAllSegments(){
  elements.forEach( function(element) {
    if (element.type == 'line') {
      checkSegments(element);
    }
  });
}

///////////////////////////////////////////////////////////////////////////////


function checkAllPoints() {
  log("check all points *************************")
  points.forEach( point => {
    console.group( "Point: " + point.id )
    // log( point.toString() )

    log(` xVal: ${point.xVal}`)
    log(`    x: ${point.x}`)

    let simpX = alg( `simplify( ${point.x} )` )
    log(`simpX: ${simpX}`)
    if ( simpX != point.x ) {
      console.warn(`x: ${simpX} != ${point.x}`)
    }

    log(` yVal: ${point.yVal}`)
    log(`    y: ${point.y}`)

    let simpY = alg( `simplify( ${point.y} )` )
    log(`simpY: ${simpY}`)
    if ( simpY != point.y ) {
      console.warn(`y: ${simpY} != ${point.y}`)
    }

    console.groupEnd()
  })
}

function checkLine( line ) {
  console.group( "Check Line: " + line.id )
  console.dir(line)
  var x1, y1, x2, y2
  var a, b, c

  alg( "clearall" )


  console.group( "Point: " + line.points[0].id)
    cmd = `x1 = (${line.points[0].x})
    x1`
    log( cmd )
    var x1 = alg( cmd )
    log( `   = ${x1}` )

    cmd = `y1 = (${line.points[0].y})
    y1`
    log( cmd )
    var y1 = alg( cmd )
    log( `   = ${y1}` )
  console.groupEnd()

  console.group( "Point: " + line.points[1].id)
    cmd = `x2 = (${line.points[1].x})
    x2`
    log( cmd )
    var x2 = alg( cmd )
    log( `   = ${x2}` )

    cmd = `y2 = (${line.points[1].y})
    y2`
    log( cmd )
    var y2 = alg( cmd )
    log( `   = ${y2}` )
  console.groupEnd()


  console.group( "a = y1 - y2" )
    cmd = ` a = (${y1}) - (${y2})`
    log( cmd )
    alg( cmd )
    var a = alg( "a" )
    log( `   = ${a}` )

    var a2 = alg( "a2 = simplify(a) \n a2" )
    log( `   = ${a2}` )
  console.groupEnd()

  // b = x2 - x1
  console.group( "b = x2 - x1" )
    cmd = ` b = (${x2}) - (${x1})`
    log( cmd )
    alg( cmd )
    var b = alg( "b" )
    log( `   = ${b}` )

    var b2 = alg( "b2 = simplify(b) \n b2" )
    log( `   = ${b2}` )
  console.groupEnd()

  console.group( "c = (x1 * y2) - (x2 * y1)" )

    cmd = ` c = ((${x1}) * (${y2})) - ((${x2}) * (${y1}))`
    log( cmd )
    alg( cmd )
    var c = alg( "c" )
    log( `   = ${c}` )

    var c2 = alg( "c2 = simplify(c) \n c2" )
    log( `   = ${c2}` )

  console.groupEnd()

  console.group( "eq = (a) * x + (b) * y + (c)" )

    cmd = `eq = (a) * x + (b) * y + (c) \n eq`
    var eq = alg( cmd )
    log( `   = ${eq}` )

    var eq2 = alg( "eq2 = simplify(eq) \n eq2" )
    log( `   = ${eq2}` )

    cmd = `eq3 = (a2) * x + (b2) * y + (c2) \n eq3`
    var eq3 = alg( cmd )
    log( `   = ${eq3}` )

  console.groupEnd()

  console.group( "xRoot" )

    cmd = `xRoot = roots(eq, x) \n xRoot`
    var xRoot = alg( cmd )
    log( ` x = ${ xRoot }` )

    var xRoot2 = alg( `xRoot2 = simplify(xRoot) \n xRoot2`)
    log( `   = ${ xRoot2 }` )

    log()
    log( ` x1 = ${x1}` )
    log( ` y1 = ${y1}` )
    log( ` * test y1 on xRoot`)
    cmd = `subst(y1, y, xRoot)`
    var xForY1 = alg( cmd )
    log( ` x1 for y1 = ${xForY1}` )
    if (x1 != xForY1) {
      console.warn(`x1 != xForY1`)
    }


    log()
    log( ` * test y1 on xRoot2`)
    cmd = `subst(y1, y, xRoot2)`
    var xForY1 = alg( cmd )
    log( ` x1 for y1 = ${xForY1}` )
    if (x1 != xForY1) {
      console.warn(`x1 != xForY1`)
    }


  console.groupEnd()

  console.group( "yRoot" )

    cmd = `yRoot = roots(eq, y) \n yRoot`
    var yRoot = alg( cmd )
    log( ` y = ${yRoot}` )
    log( `   = ${ alg('simplify(yRoot)') }` )

  console.groupEnd()

  console.groupEnd()
}
