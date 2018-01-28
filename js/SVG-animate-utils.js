function hideAllElements() {
    // hide all elelemts
    TweenLite.set($('.Point'), {
        autoAlpha: 0,
    });
    TweenLite.set($('.Line'), {
        autoAlpha: 0,
    });
    TweenLite.set($('.Circle'), {
        autoAlpha: 0,
    });
    TweenLite.set($('.Sector'), {
        autoAlpha: 0,
    });
    TweenLite.set($('.Segment'), {
        autoAlpha: 0,
    });
    TweenLite.set($('.y'), {
        autoAlpha: 0,
    });
    TweenLite.set($('.logo'), {
        autoAlpha: 0,
    });

}

function setPoint(id, position) {
    DrawTL.fromTo(
        id,
        .5, {
            autoAlpha: 0,
            scale: 10,
            transformOrigin: "50% 50%",
        }, {
            autoAlpha: 1,
            scale: 1,
        },
        position
    );
}

function setLine(id) {
    DrawTL.fromTo(
        id,
        .5,
        {
          autoAlpha: 1,
          scale: 0,
          transformOrigin: "50% 50%",
        },
        {
          autoAlpha: 1,
          scale: 1,
          transformOrigin: "50% 50%",
        }
    );
}

function setSegment(id) {

    DrawTL.fromTo(
        id,
        .5,
        {
          autoAlpha: 1,
          scale: 0,
          strokeOpacity: 1,
          transformOrigin: "50% 50%",
        },
        {
          autoAlpha: 1,
          scale: 1,
          strokeOpacity: 1,
          transformOrigin: "50% 50%",
        }
    )
    .to(
        id,
        .5,
        {
          strokeOpacity: MUTEOPACITY,
        }
    )
}

function strokeLine(id) {
    var len = $(id).get(0).getTotalLength();

    DrawTL.fromTo(
        id,
        .5, {
            scale: 1,
            autoAlpha: 0,
            strokeDasharray: len + " " + len,
            strokeDashoffset: len + 1,
            transformOrigin: "50% 50%",
        }, {
            scale: 1,
            autoAlpha: 1,
            strokeDasharray: len + " " + len,
            strokeDashoffset: 0,
            transformOrigin: "50% 50%",
        }
    );
}

function unStrokeLine(id) {
    var len = $(id).get(0).getTotalLength();

    DrawTL.fromTo(
        id,
        1, {
            scale: 1,
            autoAlpha: 1,
            strokeDasharray: len + " " + len,
            strokeDashoffset: 0,
            transformOrigin: "50% 50%",
        }, {
            scale: 1,
            autoAlpha: 0,
            strokeDasharray: len + " " + len,
            strokeDashoffset: len + 1,
            transformOrigin: "50% 50%",
        }
    );
}

function strokeLineReverse(id) {
    var len = $(id).get(0).getTotalLength();

    DrawTL.fromTo(
        id,
        .5, {
            scale: 1,
            autoAlpha: 1,
            strokeDasharray: len + " " + len,
            strokeDashoffset: -len + 1,
            transformOrigin: "50% 50%",
        }, {
            scale: 1,
            autoAlpha: 1,
            strokeDasharray: len + " " + len,
            strokeDashoffset: 0,
            transformOrigin: "50% 50%",
        }
    );
}

function strokeLineCenter(id) {
    var len = $(id).get(0).getTotalLength();

    DrawTL.fromTo(
        id,
        .5, {
            autoAlpha: 1,
            strokeDasharray: 1,
            strokeDashoffset: len / 2,
            transformOrigin: "50% 50%",
        }, {
            autoAlpha: 1,
            strokeDasharray: len,
            strokeDashoffset: 0,
            transformOrigin: "50% 50%",
        }
    );
}

function setLines(id) {
    DrawTL.staggerFrom(
        id,
        .5, {
            scale: 0,
            transformOrigin: "50% 50%",
        }, .2
    );
}

function setCircle(id) {
    DrawTL.fromTo(
        id,
        .5, {
            autoAlpha: 1,
            scale: 0,
            // fillOpacity: 1,
            transformOrigin: "50% 50%",
        }, {
            autoAlpha: 1,
            scale: 1,
            // fillOpacity: .1,
            transformOrigin: "50% 50%",
        }
    );
}

function sweepRadius(circleId, radiusId) {
    var circle = $(circleId);
    var len = $(circleId).get(0).getTotalLength();

    var cx = parseInt(circle[0].getBBox().x) + parseInt(circle[0].getBBox().width / 2);
    var cy = parseInt(circle[0].getBBox().y) + parseInt(circle[0].getBBox().height / 2);
    var center = cx + ' ' + cy;

    var timeOffset;

    // console.log(center);

    if (radiusId) {
        strokeLine(radiusId);
        DrawTL.to(radiusId, 1, {
            rotation: 360,
            svgOrigin: center
        });
        timeOffset = "-=1";
    }

    DrawTL.fromTo(
        circleId,
        1, {
            autoAlpha: 1,
            fillOpacity: 0,
            scale: 1,
            strokeDasharray: len + " " + len,
            strokeDashoffset: len
        }, {
            autoAlpha: 1,
            fillOpacity: .1,
            scale: 1,
            strokeWidth: 2,
            strokeDasharray: len + " " + len,
            strokeDashoffset: 0
        }, timeOffset
    );

    if (radiusId) {
        hideElements(radiusId);
        // unStrokeLine(radiusId);
    }
    DrawTL.to(circleId, .5, {
        strokeWidth: .5
    }, "-=1")
}

function hideElements(id) {
    DrawTL.staggerTo(
        id,
        1, {
            autoAlpha: 0,
            scale: 0,
            transformOrigin: "50% 50%",
        }, .1
    );

}

//can take multiple items
function zoomToElement(id, margin, scale) {

    var elements = $(id);
    var topX, topY, bottomX, bottomY;
    var start = true;
    //margin = 0;
    // console.log(elements);

    if (elements) {
      for (i = 0; i < elements.length; ++i) {
        // for (i in elements) {
            console.log("for: " + i + " : " + elements[i]);
            if (start) {
                start = false;

                // topX = parseInt(i.getBBox().x);
                topX = parseInt(elements[i].getBBox().x);
                topY = parseInt(elements[i].getBBox().y);
                bottomX = parseInt(elements[i].getBBox().width);
                bottomY = parseInt(elements[i].getBBox().height);
            } else {
                if (elements[i]) {
                    var x = parseInt(elements[i].getBBox().x);
                    var y = parseInt(elements[i].getBBox().y);
                    var wd = parseInt(elements[i].getBBox().width);
                    var ht = parseInt(elements[i].getBBox().height);

                    console.log("element: " + i + " x: " + x + " y: " + y + " w: " + wd + " h: " + ht);
                    if (x < topX) {
                        topX = x;
                    }
                    if (y < topY) {
                        topY = y;
                    }
                    if (x + wd > bottomX) {
                        bottomX = x + wd;
                    }
                    if (y + ht > bottomY) {
                        bottomY = y + ht;
                    }
                }
            }
            console.log("bounds: " + i + " : " + topX + " " + topY + " " + bottomX + " " + bottomY);

        }
    }

    console.log(topX);
    console.log(topY);
    console.log(bottomX);
    console.log(bottomY);

    var viewBox = (topX - margin) + ' ' + (topY- margin) + ' ' + (bottomX-topX+(2*margin)) + ' ' + (bottomY- topY+(2*margin));
    console.log(viewBox);

    //scale lines and points with viewbox
    DrawTL.to("#drawing", 1, {
            attr: {
                viewBox: viewBox
            }
        })
        .to(".Segment", 1, {
            strokeWidth: 2
        }, "-=1")
        .to(".Point", 1, {
            attr: {
                r: 3
            }
        }, "-=1")
        .to(".Point.g", 1, {
            attr: {
                r: 3
            }
        }, "-=1");

}

function dumpComputedStyles(id) {
    var styleList = [
        "visibility",
        "opacity",
        "stroke",
        "strokeWidth",
        "fill",
        "fillOpacity"
    ]

    var element = $(id).get(0);

    var out = "";
    var elementStyle = element.style;
    var computedStyle = window.getComputedStyle(element, null);

    for (prop in styleList) {
        var propValue = computedStyle.getPropertyValue(styleList[prop]);
        // out += "  " + styleList[prop] + " = '" + propValue + "'\n";
        out += "  " + styleList[prop] + " = '" + getStyle(element, styleList[prop]) + "'\n";
    }

    // console.log("fill: " + document.defaultView.getComputedStyle(element, null).getPropertyValue("fill"));


    console.log(id + ": " + out)

    console.log("stroke: " + element.style.stroke)

    var len = 0; //cs.length;


    // console.log(style+" : "+ cs.getPropertyValue(style));
    //
    // for (var i=0;i<len;i++) {
    //
    //   var style = cs[i];
    //   console.log(style+" : "+cs.getPropertyValue(style));
    // }
    //
}

function getStyle(oElm, strCssRule) {
    var strValue = "";
    if (document.defaultView && document.defaultView.getComputedStyle) {
        strValue = document.defaultView.getComputedStyle(oElm, "").getPropertyValue(strCssRule);
    } else if (oElm.currentStyle) {
        strCssRule = strCssRule.replace(/\-(\w)/g, function(strMatch, p1) {
            return p1.toUpperCase();
        });
        strValue = oElm.currentStyle[strCssRule];
    }
    return strValue;
}


function animateLogo() {


    strokeLine(".logo.G");
    strokeLine(".logo.E");
    strokeLine(".logo.O");
    strokeLine(".logo.M");
    strokeLine(".logo.E2");
    strokeLine(".logo.T");
    strokeLine(".logo.O2");
    strokeLine(".logo.R");


}
