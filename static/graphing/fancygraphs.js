
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

    console.log("H: " + text.getBBox().height);
    text.attr("text", temp.substring(1));
}

/**
 * Another moment where I am not sure if I love or hate this language.
 * Here, I'm just going to add a function to the string class. Why?
 * Because I can.
 * It also makes creating paths in raphael infinitly easier...
 */
String.prototype.format = function() {
  var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
      });
};


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
        width: 500, //width of the graph
        height: 300, //height of the graph
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

    //Create a label for each bar along the bottom
    var tallestLabel = -1;
    var x = 0;
    var barLabels = new Array();
    for (var i = 0; i < data.length; i++) {
         //Choice name label
         barLabel = paper.text();
         wrap(barLabel, data[i][0], barWidth - 5);
         tallestLabel = Math.max(tallestLabel, barLabel.getBBox().height);
         barLabel.attr({x: x + barWidth/2, title:data[i][0]}).attr(s.fontAttr);
         x += barWidth + s.barPadding;
         barLabels[i] = barLabel;
    }
    //Raphael seems to be giving a height for the text that is slightly shorter than the actual height. This causes
    //things like y's and g's to get cut off. My solution? Add a magical '4'. Why 4? Trial and error says that it works.
    var labelYPos = s.height - (4+(tallestLabel/2));
    barLabels.map(function(barLabel){barLabel.attr({y: labelYPos});});

    var barHeightMax = s.height - 2*(tallestLabel + s.labelPadding);
    var tickSize = barHeightMax/largestValue;

    //Start the bars at the position of the text labels and the move up by the amount of label padding
    //Since the labelYPos has Y in the middle of the text object (Raphael doesn't support setting vertical alignment
    //yet) we need to move up (subtract) one half of the height of tallest label to get where we need.
    //Also the magic constant of 4 needs to make a reappearence.
    var startBarHeight = labelYPos - (4+tallestLabel/2) - s.labelPadding;

    //Draw a line across the bottom starting from x=0 to x=s.width at the bar's bottom
    var pathText = "M 0 {0} l {1} 0".format(startBarHeight, s.width);
    paper.path(pathText);

    x = 0; //Keep track of our x position as we loop through the data
    for (var index = 0; index < data.length; index++) {
        var choiceLabel = data[index][0];
        var choiceValue = data[index][1];
        var barHeight = choiceValue*tickSize;
        var barTop = startBarHeight - barHeight;
        var barY = barHeightMax-barHeight+tallestLabel;
        var animationTime = 1500+(200*(Math.random()-0.5));

        //Lets make bar!
        var bar = paper.rect(x, startBarHeight, barWidth, 0);
        bar.attr(s.barAttr).attr({gradient: "270-"+s.colors[index]+"-"+s.colors2[index]});
        var finalPos = {y: barTop, height: barHeight};
        bar.animate(finalPos, animationTime, '<>');

        //Bar value
        var text = paper.text(x + barWidth/2, 0, choiceValue); //Don't worry we'll set y soon enough...
        //Stupid vertical middle centering text... shift up the text by one half it's size again...
        text.attr({y: barTop - (s.labelPadding + text.getBBox().height/2)});
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
