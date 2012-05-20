#!/usr/bin/env python2.7

import matplotlib as mpl
 #Apparently doing this BEFORE we import plt makes graphing without Xserver possible
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from polls.models import Poll, Public_Poll, Private_Poll

yAxis= [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 300, 400, 500]
ticksAt= [100, 50, 25, 10, 5, 1]
tickCount = 4

def view_private(request, private_hash):
    poll = get_object_or_404(Private_Poll, private_hash=private_hash)
    return view(request, poll)

def view_public(request, poll_id):
    poll = get_object_or_404(Public_Poll, pk=poll_id)
    return view(request, poll)

def view(request, poll):

    #Our data
    data = poll.results()

    N = len(data)
    x = np.arange(1, N + 1)
    y = [num for (s, num) in data]
    labels = [s for (s, num) in data]
    width = 0.5

    max_val = max(y)
    max_yaxis = next( val for val in yAxis if val > max_val )
    yticks = range(max_yaxis+1)

    fig = plt.figure(figsize=(5,2), dpi=100)
    ax = fig.add_subplot(1,1,1)
    bar = ax.bar(x, y, width)
    plt.xticks(x + width/2.0, labels)
    ax.set_yticks(yticks)

    #Add labels to the top of bars from:
    # http://matplotlib.sourceforge.net/examples/api/barchart_demo.html
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, str(int(height)),
                    ha='center', va='bottom')

    autolabel(bar)

    #Convert graph to http response: http://www.scipy.org/Cookbook/Matplotlib/Django
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


    #plt.show()
    #fig.savefig("/tmp/a.png", bbox_inches='tight', pad_inches=0.03)

