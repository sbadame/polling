
/**
 * Given an element and some data this function will make a bar char for you!
 * element: The HTML dom element to put the svg data in
 * data: An array of tuples containing the labels and data
 *      ex) an example value could be: [['Sandro', 100], ['Chris', 200]]
 * overrides: A list of settings that you can override
 */

function graph(element, data, overrides) {
    if (overrides == undefined) {
        overrides = [];
    }
    s = {
        width: 300, //width of the graph
        height: 200, //height of the graph
        barPadding: 7, //space in between the bars
        labelPadding: 3,//The amount of space between a label and the bar
        fontSizePx: 13, //The font size used in pixels
        fontName: "Helvetica", //the font name used
        colors: ["#043095", "#B30065", "#8BD000", "#DF9400"], //First color of gradient for each bar passed in data
        colors2: ["#011A54", "#650039", "#4E7500", "#7D5400"], //Second color of gradient
        barAttr: {stroke: "#333"}, //Raphael attribute for the bars drawn.
    };

    //Combines defaults with overrides and stores the result in defaults
    $.extend(s, overrides);

    // Since the default value is dependent on other default values, we need to do this AFTER
    // we instantiate defaultSettings

    if (s.fontAttr == undefined) {
        s.fontAttr = {font: s.fontSizePx + "px " + s.fontName, fill:"#333"};
    }

    var paper = new Raphael(element, s.width, s.height);
    var barWidth = Math.min(65, (s.width - s.barPadding*(data.length - 1)) / data.length);
    var barHeightMax = s.height - 2*(s.fontSizePx + s.labelPadding);
    var largestValue = Math.max.apply(Math, data.map(function(e){return e[1];}));
    var tickSize = barHeightMax/largestValue;
    var colors = new Array("#043095", "#B30065", "#8BD000", "#DF9400");
    var colors2 = new Array("#011A54", "#650039", "#4E7500", "#7D5400");

    var x = 0;
    for (index in data) {
        var choiceLabel = data[index][0];
        var choiceValue = data[index][1];
        var barHeight = choiceValue*tickSize;
        var barY = barHeightMax-barHeight+s.labelPadding+s.fontSizePx;
        var animationTime = 1500+(200*(Math.random()-0.5));

        //Lets make bar!
        var bar = paper.rect(x, s.height-s.labelPadding-s.fontSizePx, barWidth, 0);
        bar.attr(s.barAttr).attr({gradient: "270-"+s.colors[index]+"-"+s.colors2[index]});
        bar.animate({y: barY, height: barHeight}, animationTime, '<>');

        //Choice name label
        paper.text(x + barWidth/2, s.height - s.fontSizePx/2, choiceLabel).attr(s.fontAttr);

        //Bar value
        var text = paper.text(x + barWidth/2, barY - (s.fontSizePx/2) - s.labelPadding, choiceValue).attr({opacity: 0.0}).attr(s.fontAttr);
        var fadeIn = Raphael.animation({opacity:1.0}, animationTime*0.5);
        text.animate(fadeIn.delay(animationTime));

        //Move x along
        x += barWidth + s.barPadding;
    }
}
