#!/usr/bin/env python

import sys
import numpy
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt

if (__name__ == '__main__'):

    if (len(sys.argv) < 2):
        print('')
        print('\nUsage: %s f1 [f2 [f3 [...]]] ' % (sys.argv[0]))
        print('          Plot all listed files using simple defaults.')
        print('')
        exit(1)

    mpl.rcParams['figure.facecolor'] = 'white'

    fig = plt.figure()
    fig.suptitle('Reaction Data', fontsize=18.5)
    ax = fig.add_subplot(111)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel(r'Time (s)')
    ax.set_ylabel(r'Count')

    legend = False
    label = ""
    for i in range(1, len(sys.argv)):
        filename = sys.argv[i]
        if filename == "-legend":
            legend = True
        elif filename == "-no-legend":
            legend = False
        elif filename[0:3] == "-n=":
            label = filename[3:]
        else:
            print('Plotting %s' % (filename))
            if len(label) == 0:
              label = filename
            data = numpy.fromfile(sys.argv[i],sep=' ')
            x = data[0::2]
            y = data[1::2]
            ax.plot(x, y, label=label)
            label = ""

    if legend:
        ax.legend()

    plt.show()
