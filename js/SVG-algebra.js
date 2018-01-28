// initialize Algebra.js
// const Fraction = algebra.Fraction;
// const Expression = algebra.Expression;
// const Equation = algebra.Equation;


function testAlgebrite() {


  var cmd = `A = 1/2 y - 1/4 3^(1/2) - 1/2 3^(1/2) x
B = 5/4 + x + x^2 + y^2
C = A - B
C
  `;
  var result = Algebrite.run( cmd );
  result = Algebrite.run( 'C' );
  log('C: ' + result);

  result = Algebrite.run( 'simplify(C)' );
  log('simplify(C): ' + result);
  //
  // result = Algebrite.run( 'expand(C)' );
  // log('expand(C): ' + result);

  result = Algebrite.run( "roots(C, x)" );
  log('roots(C, x): ' + result);

  var latex = Algebrite.run( 'printlatex(roots(C, x))' );
  katex.render(latex, footerPanel);

  result = Algebrite.run( "roots(C, y)" );
  log('roots(C, y): ' + result);

}

///////////////////////////////////////////////////////////////////////////////

// shortcut for Algebrite.run
function alg( cmd ) {
  //TODO: put in error checking
  // log("ALG!!!!!!!!!!!")
  return Algebrite.run( cmd.toString() );
}

// check if algebraic value can be converted to a decimal float number
function checkNumber( val ) {
  var num = alg( `float(${val})` );
  if ( isNaN( num ) ) {
    log( `*** checkNumber: "${val}" is not a Number.` );
    stop;
    return false;
  }
  return true;
}

// check if algebraic value then return decimal float value
function getNumber( val ) {
  var num = parseFloat(alg( `float(${val})` ));
  if ( isNaN( num ) ) {
    log( `*** getNumber: "${val}" is not a Number.` );
    stop;
    return false;
  }
  return num;
}

// check if Alg string has has i or stop
function checkValid(str) {
  let valid = true;
  if ( str.indexOf("Stop:") !== -1  ) {
    console.error(`value: (${str}) contains 'Stop'`);
    valid = false;
  }
  if ( str.indexOf("i") !== -1   ) {
    console.error(`value: (${str}) contains 'i'`);
    valid = false;
  }
  if ( str.indexOf("nil") !== -1   ) {
    console.error(`value: (${str}) contains 'nil'`);
    valid = false;
  }

  return valid;
}

///////////////////////////////////////////////////////////////////////////////
function testAlgebraJS() {
  var exp1 = new Expression("5/4 + x + x^2 + y^2");
  var exp2 = new Expression("0")
  // var exp1 = algebra.parse("1 / x");
  // var exp2 = algebra.parse("x / (1 + x)")
  var eq = new Equation(exp1, exp2);
  log("exp1: " + exp1.toString());
  log("exp2: " + exp2.toString());
  log(" eq:" + eq.toString());
  log("x = " + eq.solveFor("x"));
  // log("y = " + eq.solveFor("y"));

  // exp1 = exp1.multiply("x")
  // exp2 = exp2.multiply("x")
  // eq = new Equation(exp1, exp2);
  // log(eq.toString());
  // log(eq.solveFor("x"));
}
