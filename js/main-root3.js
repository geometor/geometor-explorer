


function main() {
  log('---------------------')


  //initial points set by X Y
  Point( "-1/2", "0" );
  Point( "1/2", "0" );

  // baseline
  Line( points[0], points[1] );

  // vesic pisces
  Circle( points[0], points[1] );
  Circle( points[1], points[0] );

  // bisector
  Line( points[4], points[5] );

  // equilateral triangle
  // Line( points[0], points[4] );
  // Line( points[0], points[5] );
  Line( points[1], points[4] );
  Line( points[1], points[5] );

  // outer two unit circles
  // Circle( points[0], points[3] );
  // Circle( points[1], points[2] );

  // circumscribe triangle
  Line( points[0], points[8] );
  Circle( points[11], points[8] );
  Line( points[17], points[13] );

  // Line( points[8], points[10] );
  // Line( points[7], points[9] );
  //
  // Line( points[39], points[44] );
  // Line( points[41], points[39] );
  // Line( points[42], points[44] );

  logSummary();

  // jump to end of animation
  DrawTL.progress(1, false);

  // checkAllSegments();

  //animateGoldenSegments();

}


$( document ).ready(function() {
    console.log( "ready!" );
    main();
    log("main complete")
});
