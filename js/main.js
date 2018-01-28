


function main() {
  log('---------------------')


  //initial points set by X Y
  Point( "-1/2", "0" );
  Point( "1/2", "0" );

  //baseline
  Line( points[0], points[1] );

  // vesic pisces
  Circle( points[0], points[1] );
  Circle( points[1], points[0] );
  //
  //
  // //bisector
  Line( points[4], points[5] );
  // //
  // // equilateral triangle
  // Line( points[0], points[4] );
  // Line( points[0], points[5] );
  // Line( points[1], points[4] );
  Line( points[1], points[5] );
  // // //
  // // //

  Circle( points[0], points[3] );
  Circle( points[1], points[2] );
  //
  //
  //
  // Circle( points[4], points[0] );
  // Circle( points[5], points[1] );
  //
  // //
  // Circle( points[3], points[0] );
  // Circle( points[2], points[1] );

  Line( points[0], points[7] );
  Circle( points[18], points[7] );


  //
  //
  // Line( points[27], points[30] );
  // Line( points[14], points[17] );
  //
  // Circle( points[6], points[0] );
  //
  // Line( points[80], points[87] );
  // Line( points[81], points[86] );
  //
  // Circle( points[80], points[118] );
  // Circle( points[80], points[119] );



  logSummary();

  checkAllSegments();

  //animateGoldenSegments();

}


$( document ).ready(function() {
    console.log( "ready!" );
    main();
});
