//http://documentup.com/wout/svg.js
//
//
//-----------------Inkscape figure raw data for drawing the chair-------------------

var originalWidth = 167.14912 //164.98347
var originalHeight = 177.74756 //182.59712
var widthHeightRatio = originalWidth/originalHeight

rawSVGbat = '<?xml version="1.0" encoding="UTF-8" standalone="no"?> <svg xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:cc="http://creativecommons.org/ns#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:svg="http://www.w3.org/2000/svg" xmlns="http://www.w3.org/2000/svg" width="31.395832mm" height="20.276472mm" viewBox="0 0 111.24507 71.845767" id="svg4486" version="1.1"> <defs id="defs4488" /> <metadata id="metadata4491"> <rdf:RDF> <cc:Work rdf:about=""> <dc:format>image/svg+xml</dc:format> <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" /> <dc:title></dc:title> </cc:Work> </rdf:RDF> </metadata> <path id="path4914-9" d="m 111.24507,23.176045 c 0,-3.476417 -0.78335,-4.635203 -4.6352,-4.635203 l -3.47642,0 0,-10.429232 C 103.13345,1.263796 101.86967,0 95.021831,0 L 8.11162,0 C 1.263796,0 0,1.263796 0,8.11161 l 0,55.622536 c 0,6.847824 1.263796,8.11162 8.11162,8.11162 l 86.910211,0 c 6.847839,0 8.111619,-1.263796 8.111619,-8.11162 l 0,-10.429212 3.47642,0 c 3.85185,0 4.6352,-1.158825 4.6352,-4.635223 z m -17.432979,-6.952815 0,39.399296 c 0,8.302737 0.433071,6.902034 -6.902034,6.902034 l -70.686951,0 c -6.609353,0 -6.902053,-1.260388 -6.902053,-6.902034 l 0,-39.399296 c 0,-7.577005 0.534617,-6.902034 6.902053,-6.902034 l 70.686951,0 c 7.242018,0.131162 7.037238,0.603741 6.902034,6.902034 z" style="fill:#000000;fill-opacity:1;stroke:none;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" /> </svg>'

//-------------------------------------------------------------------------------------

function scale(svg, factor){
    //lock dimension ratio
    svg.objects = svg.objects.scale(factor, factor)
    return svg
    }

function newCanvas(container, procHeight, procWidth){
    //container is a string representing the DOM element where the SVG will be drawn
    //procHeight is a string representing the procentual height of the DOM element which will be used to draw the canvas, defaults to 100%
    //same for procWidth
    //returns a SVG object 
    procHeight = typeof procHeight !== 'undefined' ? procHeight : '100%';
    procWidth = typeof procWidth !== 'undefined' ? procWidth : '100%';
    return SVG(container).size(procHeight, procWidth)
    }

function addChair(oricanvas){
    //canvas is a SVG object, draws a chair on the canvas
    //returns the chair as an SVG object
    //returns an object containing the references to all objects in the SVG chair drawing 
    var nested = oricanvas.nested().size(originalHeight, originalWidth)
    return {canvas:nested, objects:nested.svg(rawSVGchair)}
    }

function addBat(oricanvas){
    //canvas is a SVG object, draws a chair on the canvas
    //returns the chair as an SVG object
    //returns an object containing the references to all objects in the SVG chair drawing 
    var nested = oricanvas.nested()
    return {canvas:nested, objects:nested.svg(rawSVGbat)}
    }


function addTable(canvas){
    var nested = canvas.nested()
    return nested.circle(500).fill('none').stroke({color: '#000000', opacity: 1, width: 10})
    }      

function fillChair(chair, color){
    //fill seat of chair, chair is an object containing the references to all objects in the SVG chair drawing, color is a hexadecimal string format ex. '#FF0000'
    chair.get('zitje').style('fill:'+color+';stroke:#000000;stroke-width:13;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0')
    }
    
function getDimOfDOM(DOMid){ //returns the dimensions of the DOM element with id DOMid
    var width = document.getElementById(DOMid).clientWidth;
    var height = document.getElementById(DOMid).clientHeight;
    return {width:width, height:height} 
    }

function getDimOfCanvas(canvas){
    //returns the dimensions of the canvas
    var dim = getDimOfDOM(canvas.parent().id)
    var hperc = parseFloat(canvas.attr('height'))/100.0
    var wperc = parseFloat(canvas.attr('width'))/100.0
    var width = dim.width*wperc
    var height = dim.height*hperc
    return {width:width, height:height} 
    }

function centerOnCanvas(canvas, SVG){
    console.log(SVG)
    //canvas is the canvas where the SVG is drawn on
    twidth = SVG.objects.tbox().width
    theight = SVG.objects.tbox().height //tbox takes scale transformation into account
    nwidth = $("#"+canvas.parent().id).width()
    nheight = $("#"+canvas.parent().id).height()
    //console.log(twidth/2)
    //console.log(theight/2)
    //console.log(nwidth/2)
    //console.log(nheight/2)
    SVG.objects.center((nwidth-twidth)/2, (nheight-theight)/2)
    }

function centerOnCanvasText(canvas, text){
    //canvas is the canvas where the SVG is drawn on
    twidth = text.tbox().width
    theight = text.tbox().height //tbox takes scale transformation into account
    nwidth = $("#"+canvas.parent().id).width()
    nheight = $("#"+canvas.parent().id).height()
    //console.log(twidth/2)
    //console.log(theight/2)
    //console.log(nwidth/2)
    //console.log(nheight/2)
    text.center((nwidth-twidth)/2, (nheight-theight)/2)
    //text.dy((nheight-theight)/2)
    }

function centerOnDiv(divId, SVG){
    //divId is the id of the div conatining the SVG
    console.log(getDimOfDOM(divId).width/2)
    SVG.objects.center(getDimOfDOM(divId).width/2, getDimOfDOM(divId).height/2)
    }

//---------------------animating functions----------------------






//test code
//var canvas1 = newCanvas('canvas_container', '100%','100%')
//var chair1 = addChair(canvas1)
//chair1.canvas.transform({
//  rotation: 45,
//  x: 50,
//  y: 50
//})

//var chair2 = addChair(canvas1)
//fillChair(chair2.objects, '#FF0000')
//var table1 = addTable(canvas1)
//centerOnCanvas(canvas1, table1)
//getDimOfCanvas(canvas1)
