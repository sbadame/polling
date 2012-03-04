
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
        maxBarWidth: 80,
        yAxis: [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 300, 400, 500],
        ticksAt: [100, 50, 25, 10, 5, 1],
        tickCount: 4,
        tickWidth: 20
    };

    //Combines defaults with overrides and stores the result in defaults
    $.extend(s, overrides);

    // Since the default value is dependent on other default values, we need to do this AFTER
    // we instantiate defaultSettings
    if (s.fontAttr == undefined) {
        s.fontAttr = {font: s.fontSizePx + "px " + s.fontName, fill:"#333"};
    }

    paper = new Raphael(element, s.width, s.height);
    barWidth = Math.min(s.maxBarWidth, (s.width - s.barPadding*(data.length - 1)) / data.length);
    largestValue = Math.max.apply(Math, data.map(function(e){return e[1];}));

    //Get the yaxis that fits our graph best
    maxY = s.yAxis[0];
    i = 0;
    while (i < s.yAxis.length && largestValue > s.yAxis[i]) {
        i++;
    }
    largestValue = s.yAxis[i];
    tickIndex = 0;
    while (tickIndex < (s.ticksAt.length - s.tickCount) && s.ticksAt[tickIndex] > largestValue) {
        tickIndex++;
    }

    //Create a label for each bar along the bottom
    //We can't set the y values for the bar yet because we don't know how tall the tallest one is.
    //Once we've gone through them all we can pick out the tallest one and then apply the y position
    //to all of these labels
    tallestLabel = -1;
    x = s.tickWidth;
    barLabels = new Array();
    for (i = 0; i < data.length; i++) {
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
    labelYPos = s.height - (4+(tallestLabel/2));
    barLabels.map(function(barLabel){barLabel.attr({y: labelYPos});});

    //Start the bars at the position of the text labels and the move up by the amount of label padding
    //Since the labelYPos has Y in the middle of the text object (Raphael doesn't support setting vertical alignment
    //yet) we need to move up (subtract) one half of the height of tallest label to get where we need.
    //Also the magic constant of 4 needs to make a reappearence.
    startBarHeight = labelYPos - (4+tallestLabel/2) - s.labelPadding;
    endBarHeight = s.height - (startBarHeight + s.labelPadding + s.fontSizePx/2);
    tickSize = (startBarHeight - endBarHeight)/largestValue;

    //Draw a line across the bottom starting from x=0 to x=s.width at the bar's bottom
    bottomLine = "M {0} {1} l {2} 0".format(s.tickWidth, startBarHeight, s.width);
    paper.path(bottomLine);

    //Draw a line on the right side to the top
    rightSideLine = "M {0} 0 l 0 {1}".format(s.width, startBarHeight);
    paper.path(rightSideLine);

    maxTick = -1;
    for(tick = 0; tick <= largestValue; tick++) {
        for(tickLevel = 0; tickLevel < s.tickCount; tickLevel++) {
            if ( (tick % s.ticksAt[tickLevel+tickIndex]) === 0) {//Yes this is correct THREE equals signs. Javascript, wtf are you??
                //Draw a line up to the top from the barchat bottomline
                var height = startBarHeight-(tick*tickSize);
                var label = paper.text(0, height, tick).attr("text-anchor","start");
                //This should turn into something configurable
                if (tickLevel === 0 || tick == largestValue) {
                    label.attr("font-weight", "bold").attr("font-size",14);
                } else if (tickLevel === 1) {
                    label.attr("font-weight", "bold");
                }
                var tickLabelWidth = label.getBBox().width;
                maxTick = Math.max(maxTick, tickLabelWidth);
                //var axisLine = "M {0} {1} l {2} 0".format(tickLabelWidth, height, s.tickWidth-tickLabelWidth);
                var axisLine = "M {0} {1} l {2} 0".format(tickLabelWidth, height, s.width);
                paper.path(axisLine);
                break;
            }
        }
    }

    x = s.tickWidth; //Keep track of our x position as we loop through the data
    for (var index = 0; index < data.length; index++) {
        var choiceLabel = data[index][0];
        var choiceValue = data[index][1];
        var barHeight = choiceValue*tickSize;
        var barTop = startBarHeight - barHeight;
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

        //Keep moving x along to the next bar
        x += barWidth + s.barPadding;
    }
    //Moments like this I just love jquery... get all of the hyperlinks (generated because by the title elements in
    //raphael) and apply some css to them. I could do this in a style sheet... but not until we have a main *.css file
    //with all of our crap. Not going to add in a new sheet just for 2 properties.
    $("#canvas_container a").css("text-decoration","none").css("cursor","default");
}
