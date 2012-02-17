
/**
 * Returns the same text as what is in content but with new lines inserted to
 * wrap the content to fit inside of text
 */
function wrap(text, content, maxWidth) {
    var words = content.split(" ");
    var temp = "";
    var lines = 1;
    for (var i=0; i < words.length; i++) {
        text.attr("text", temp + " " + words[i]);
        if (text.getBBox().width > maxWidth - 5) {
            if (lines == 3) {
                temp += "...";
                break;
            }
            temp += "\n" + words[i];
            lines++;
        } else {
            temp += " " + words[i];
        }
    }

    text.attr("text", temp.substring(1));
}


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
        barPadding: 40, //space in between the bars
        labelPadding: 3,//The amount of space between a label and the bar
        fontSizePx: 13, //The font size used in pixels
        fontName: "Helvetica", //the font name used
        colors: ["#043095", "#B30065", "#8BD000", "#DF9400"], //First color of gradient for each bar passed in data
        colors2: ["#011A54", "#650039", "#4E7500", "#7D5400"], //Second color of gradient
        barAttr: {stroke: "#333"}, //Raphael attribute for the bars drawn.
        maxBarWidth: 80
    };

    //Combines defaults with overrides and stores the result in defaults
    $.extend(s, overrides);

    // Since the default value is dependent on other default values, we need to do this AFTER
    // we instantiate defaultSettings
    if (s.fontAttr == undefined) {
        s.fontAttr = {font: s.fontSizePx + "px " + s.fontName, fill:"#333"};
    }

    var paper = new Raphael(element, s.width, s.height);
    var barWidth = Math.min(s.maxBarWidth, (s.width - s.barPadding*(data.length - 1)) / data.length);
    var largestValue = Math.max.apply(Math, data.map(function(e){return e[1];}));
    var colors = new Array("#043095", "#B30065", "#8BD000", "#DF9400");
    var colors2 = new Array("#011A54", "#650039", "#4E7500", "#7D5400");

    var tallestLabel = -1;
    var barLabels = new Array();
    for (var i = 0; i < data.length; i++) {
         //Choice name label
         barLabels[i] = paper.text();
         wrap(barLabels[i], data[i][0], barWidth - 5);
         tallestLabel = Math.max(tallestLabel, barLabels[i].getBBox().height);
    }
    var barHeightMax = s.height - 2*(tallestLabel + s.labelPadding);
    var tickSize = barHeightMax/largestValue;

    var x = 0; //Keep track of our x position as we loop through the data
    for (var index = 0; index < data.length; index++) {
        var choiceLabel = data[index][0];
        var choiceValue = data[index][1];
        var barHeight = choiceValue*tickSize;
        var barY = barHeightMax-barHeight+tallestLabel-s.labelPadding;
        var animationTime = 1500+(200*(Math.random()-0.5));

        //Lets make bar!
        var bar = paper.rect(x, s.height-s.labelPadding-tallestLabel, barWidth, 0);
        bar.attr(s.barAttr).attr({gradient: "270-"+s.colors[index]+"-"+s.colors2[index]});
        bar.animate({y: barY, height: barHeight}, animationTime, '<>');

        barLabels[index].attr({x: x + barWidth/2, y: s.height - s.labelPadding - tallestLabel/2, title:choiceLabel}).attr(s.fontAttr);

        //Bar value
        var text = paper.text(x + barWidth/2, barY - (tallestLabel/2) - s.labelPadding, choiceValue);
        text.attr({opacity: 0.0}).attr(s.fontAttr);
        var fadeIn = Raphael.animation({opacity:1.0}, animationTime*0.5);
        text.animate(fadeIn.delay(animationTime));

        //Move x along
        x += barWidth + s.barPadding;
    }
    //Moments like this I just love jquery... get all of the hyperlinks (generated because by the title elements in
    //raphael) and apply some css to them. I could do this in a style sheet... but not until we have a main *.css file
    //with all of our crap. Not going to add in a new sheet just for 2 properties.
    $("#canvas_container a").css("text-decoration","none").css("cursor","default");
}
