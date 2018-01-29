


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


  // outer two unit circles
  Circle( points[0], points[3] );
  Circle( points[1], points[2] );

  Circle( points[3], points[0] );
  Circle( points[2], points[1] );

  Line( points[25], points[26] );
  Line( points[16], points[17] );

  Line( points[27], points[32] );

  Circle( points[6], points[27] );
  Circle( points[6], points[0] );


  logSummary();

  // jump to end of animation
  // DrawTL.progress(1, false);

  DrawTL.timeScale(2).play();

  checkAllSegments();

  //animateGoldenSegments();

}


$( document ).ready(function() {
    console.log( "ready!" );
    main();
    log("main complete")
});
